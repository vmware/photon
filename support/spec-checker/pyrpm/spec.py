#!/usr/bin/env python3

import re

from abc import ABCMeta, abstractmethod

"""
Taken from: https://github.com/bkircher/python-rpm-spec

https://github.com/bkircher/python-rpm-spec/blob/main/LICENSE

Python module for parsing RPM spec files.

RPMs are build from a package's sources along with a spec file. The spec file controls how the RPM
is built. This module allows you to parse spec files and gives you simple access to various bits of
information that is contained in the spec file.

Current status: This module does not parse everything of a spec file. Only the pieces I needed. So
there is probably still plenty of stuff missing. However, it should not be terribly complicated to
add support for the missing pieces.
"""

__all__ = ["Spec", "replace_macros", "Package"]

_macro_pattern = re.compile(r"%{(\S+?)\}")
_DEFAULT_ARCHES = ["x86_64", "aarch64"]


def replace_macros(string, spec, arch=None, visited=None):
    assert isinstance(spec, Spec)
    if visited is None:
        visited = set()

    def _is_conditional(macro):
        return macro.startswith("?") or macro.startswith("!")

    def _test_conditional(macro):
        if macro[0] == "?":
            return True
        if macro[0] == "!":
            return False
        raise ValueError("Given string is not a conditional macro")

    def _macro_repl(match):
        macro_name = match.group(1)
        if _is_conditional(macro_name):
            parts = macro_name[1:].split(sep=":", maxsplit=1)
            macro_key = parts[0]
            default_value = parts[1] if len(parts) == 2 else ""
            if _test_conditional(macro_name):
                if (
                    arch
                    and arch in spec.macros_by_arch
                    and macro_key in spec.macros_by_arch[arch]
                ):
                    if macro_key in visited:
                        return default_value
                    visited.add(macro_key)
                    result = replace_macros(
                        spec.macros_by_arch[arch][macro_key],
                        spec,
                        arch,
                        visited.copy(),
                    )
                    visited.remove(macro_key)
                    return result
                if macro_key in spec.macros:
                    if macro_key in visited:
                        return default_value
                    visited.add(macro_key)
                    result = replace_macros(
                        spec.macros[macro_key], spec, arch, visited.copy()
                    )
                    visited.remove(macro_key)
                    return result
                if (
                    hasattr(spec, macro_key)
                    and getattr(spec, macro_key) is not None
                ):
                    return str(getattr(spec, macro_key))
                return default_value
            else:
                if arch and (
                    arch not in spec.macros_by_arch
                    or macro_key not in spec.macros_by_arch[arch]
                ):
                    return default_value
                if macro_key not in spec.macros and (
                    not hasattr(spec, macro_key)
                    or getattr(spec, macro_key) is None
                ):
                    return default_value
                return ""
        if (
            arch
            and arch in spec.macros_by_arch
            and macro_name in spec.macros_by_arch[arch]
        ):
            if macro_name in visited:
                return ""
            visited.add(macro_name)
            result = replace_macros(
                spec.macros_by_arch[arch][macro_name],
                spec,
                arch,
                visited.copy(),
            )
            visited.remove(macro_name)
            return result
        if macro_name in spec.macros:
            if macro_name in visited:
                return ""
            visited.add(macro_name)
            result = replace_macros(
                spec.macros[macro_name], spec, arch, visited.copy()
            )
            visited.remove(macro_name)
            return result
        if macro_name == "_arch" and arch:
            return arch
        if hasattr(spec, macro_name) and getattr(spec, macro_name) is not None:
            return str(getattr(spec, macro_name))
        return match.string[match.start() : match.end()]

    while True:
        result = re.sub(_macro_pattern, _macro_repl, string)
        if result == string:
            break
        string = result
    return result


class _Tag:
    __metaclass__ = ABCMeta

    def __init__(self, name, pattern_obj, attr_type):
        self.name = name
        self.pattern_obj = pattern_obj
        self.attr_type = attr_type

    def test(self, line):
        return re.search(self.pattern_obj, line)

    def update(self, spec_obj, context, match_obj, line):
        assert spec_obj
        assert context
        assert match_obj
        assert line
        return self.update_impl(spec_obj, context, match_obj, line)

    @abstractmethod
    def update_impl(self, spec_obj, context, match_obj, line):
        pass

    @staticmethod
    def current_target(spec_obj, context):
        target_obj = spec_obj
        if context["current_subpackage"] is not None:
            target_obj = context["current_subpackage"]
        return target_obj


class _NameValue(_Tag):
    def __init__(self, name, pattern_obj, attr_type=None):
        super(_NameValue, self).__init__(
            name, pattern_obj, attr_type if attr_type else str
        )

    def update_impl(self, spec_obj, context, match_obj, line):
        if self.name == "changelog":
            context["current_subpackage"] = None

        target_obj = _Tag.current_target(spec_obj, context)
        value = match_obj.group(1)

        if self.name == "name":
            spec_obj.packages = []
            spec_obj.packages.append(Package(value))

        if self.name in ["description", "changelog"]:
            context["multiline"] = self.name
        else:
            setattr(target_obj, self.name, self.attr_type(value))

        return spec_obj, context


class _SetterMacroDef(_Tag):
    def __init__(self, name, pattern_obj):
        super(_SetterMacroDef, self).__init__(name, pattern_obj, str)

    def get_namespace(self, spec_obj, context):
        raise NotImplementedError()

    def update_impl(self, spec_obj, context, match_obj, line):
        name, value = match_obj.groups()
        setattr(self.get_namespace(spec_obj, context), name, str(value))
        return spec_obj, context


class _GlobalMacroDef(_SetterMacroDef):
    def get_namespace(self, spec_obj, context):
        return spec_obj


class _LocalMacroDef(_SetterMacroDef):
    def get_namespace(self, spec_obj, context):
        return context["current_subpackage"]


class _MacroDef(_Tag):
    def __init__(self, name, pattern_obj):
        super(_MacroDef, self).__init__(name, pattern_obj, str)

    def update_impl(self, spec_obj, context, match_obj, line):
        name, value = match_obj.groups()
        resolved_value = replace_macros(value, spec=spec_obj)
        if context.get("current_arch"):
            for arch in context["current_arch"]:
                if arch not in spec_obj.macros_by_arch:
                    spec_obj.macros_by_arch[arch] = {}
                spec_obj.macros_by_arch[arch][name] = resolved_value
        else:
            spec_obj.macros[name] = resolved_value
            if name not in _tag_names:
                setattr(spec_obj, name, resolved_value)
        return spec_obj, context


class _List(_Tag):
    def __init__(self, name, pattern_obj):
        super(_List, self).__init__(name, pattern_obj, list)

    def update_impl(self, spec_obj, context, match_obj, line):
        target_obj = _Tag.current_target(spec_obj, context)

        if not hasattr(target_obj, self.name):
            if self.name == "build_requires":
                setattr(target_obj, self.name, False)
            else:
                setattr(target_obj, self.name, list())

        if self.name == "build_requires":
            setattr(target_obj, self.name, True)
        elif self.name == "packages":
            value = match_obj.group(1)
            if value == "-n":
                subpackage_name = line.rsplit(" ", 1)[-1].rstrip()
            else:
                subpackage_name = f"{spec_obj.name}-{value}"
            package = Package(subpackage_name)
            context["current_subpackage"] = package
            package.is_subpackage = True
            spec_obj.packages.append(package)
        else:
            value = match_obj.group(1)
            getattr(target_obj, self.name).append(value)

        return spec_obj, context


class _ListAndDict(_Tag):
    def __init__(self, name, pattern_obj):
        super(_ListAndDict, self).__init__(name, pattern_obj, list)

    def update_impl(self, spec_obj, context, match_obj, line):
        source_name, value = match_obj.groups()
        dictionary = getattr(spec_obj, f"{self.name}_dict")
        macro_names = [m.group(1) for m in re.finditer(_macro_pattern, value)]
        has_multi_value_macro = (
            any(macro in spec_obj.multi_value_macros for macro in macro_names)
            or "%{_arch}" in value
        )

        if has_multi_value_macro and not context.get("current_arch"):
            for arch in _DEFAULT_ARCHES:
                if arch not in dictionary:
                    dictionary[arch] = {}
                resolved_value = replace_macros(
                    value, spec=spec_obj, arch=arch
                )
                dictionary[arch][source_name] = value
                target_obj = _Tag.current_target(spec_obj, context)
                getattr(target_obj, self.name).append(resolved_value)
        else:
            if context.get("current_arch"):
                for arch in context["current_arch"]:
                    if arch not in dictionary:
                        dictionary[arch] = {}
                    resolved_value = replace_macros(
                        value, spec=spec_obj, arch=arch
                    )
                    dictionary[arch][source_name] = value
                    target_obj = _Tag.current_target(spec_obj, context)
                    getattr(target_obj, self.name).append(resolved_value)
            else:
                if "global" not in dictionary:
                    dictionary["global"] = {}
                resolved_value = replace_macros(value, spec=spec_obj)
                dictionary["global"][source_name] = value
                target_obj = _Tag.current_target(spec_obj, context)
                getattr(target_obj, self.name).append(resolved_value)

        return spec_obj, context


class _IfArch(_Tag):
    def __init__(self, name, pattern_obj):
        super(_IfArch, self).__init__(name, pattern_obj, str)

    def update_impl(self, spec_obj, context, match_obj, line):
        arches = match_obj.group(1).split()
        context["current_arch"] = arches
        return spec_obj, context


class _Else(_Tag):
    def __init__(self, name, pattern_obj):
        super(_Else, self).__init__(name, pattern_obj, str)

    def update_impl(self, spec_obj, context, match_obj, line):
        if context.get("current_arch"):
            else_arches = [
                a for a in _DEFAULT_ARCHES if a not in context["current_arch"]
            ]
            context["current_arch"] = else_arches
        return spec_obj, context


class _EndIfArch(_Tag):
    def __init__(self, name, pattern_obj):
        super(_EndIfArch, self).__init__(name, pattern_obj, str)

    def update_impl(self, spec_obj, context, match_obj, line):
        context.pop("current_arch", None)
        return spec_obj, context


def re_tag_compile(tag):
    return re.compile(tag, re.IGNORECASE)


class _DummyMacroDef(_Tag):
    def __init__(self, name, pattern_obj):
        super(_DummyMacroDef, self).__init__(name, pattern_obj, str)

    def update_impl(self, spec_obj, context, match_obj, line):
        context["line_processor"] = None
        return spec_obj, context


_tags = [
    _NameValue("name", re_tag_compile(r"^Name\s*:\s*(\S+)")),
    _NameValue("version", re_tag_compile(r"^Version\s*:\s*(\S+)")),
    _NameValue("release", re_tag_compile(r"^Release\s*:\s*(\S+)")),
    _NameValue("vendor", re_tag_compile(r"^Vendor\s*:\s*(.+)")),
    _NameValue("distribution", re_tag_compile(r"^distribution\s*:\s*(\S+)")),
    _NameValue("summary", re_tag_compile(r"^Summary\s*:\s*(.+)")),
    _NameValue("description", re_tag_compile(r"^%description\s*(\S*)")),
    _NameValue("changelog", re_tag_compile(r"^%changelog\s*(\S*)")),
    _NameValue("license", re_tag_compile(r"^License\s*:\s*(.+)")),
    _NameValue("group", re_tag_compile(r"^Group\s*:\s*(.+)")),
    _NameValue("url", re_tag_compile(r"^URL\s*:\s*(\S+)")),
    _NameValue("buildarch", re_tag_compile(r"^BuildArch\s*:\s*(\S+)")),
    _ListAndDict("sources", re_tag_compile(r"^(Source\d*\s*):\s*(.+)")),
    _ListAndDict("patches", re_tag_compile(r"^(Patch\d*\s*:\s*(\S+))")),
    _List("build_requires", re_tag_compile(r"^BuildRequires\s*:\s*(.+)")),
    _List("packages", re_tag_compile(r"^%package\s+(\S+)")),
    _MacroDef("define", re_tag_compile(r"^%define\s+(\S+)\s+(.+)")),
    _MacroDef("global", re_tag_compile(r"^%global\s+(\S+)\s+(.+)")),
    _IfArch("ifarch", re_tag_compile(r"^%ifarch\s+(.+)")),
    _Else("else", re_tag_compile(r"^%else\s*$")),
    _EndIfArch("endif", re_tag_compile(r"^%endif")),
]

_tag_names = [tag.name for tag in _tags]


class Package:
    def __init__(self, name):
        assert isinstance(name, str)
        for tag in _tags:
            if tag.name == "build_requires":
                setattr(self, tag.name, False)
            elif tag.name in ["description"]:
                setattr(self, tag.name, None)
            elif tag.attr_type is list:
                setattr(self, tag.name, tag.attr_type())
        self.name = name
        self.is_subpackage = False

    def __repr__(self):
        return f"Package('{self.name}')"


class Spec:
    def __init__(self):
        for tag in _tags:
            if tag.name == "build_requires":
                setattr(self, tag.name, False)
            elif tag.attr_type is list:
                setattr(self, tag.name, tag.attr_type())
            else:
                setattr(self, tag.name, None)
        self.sources_dict = {}
        self.patches_dict = {}
        self.macros = {}
        self.macros_by_arch = {}
        self.name = None
        self.packages = []
        self.multi_value_macros = set()

    def resolve_macros(self, arches=None):
        arches = arches or list(self.macros_by_arch.keys()) or _DEFAULT_ARCHES

        # Identify multi-value macros
        for arch in self.macros_by_arch:
            for macro in self.macros_by_arch[arch]:
                if macro not in self.multi_value_macros:
                    for other_arch in self.macros_by_arch:
                        if (
                            other_arch != arch
                            and macro in self.macros_by_arch[other_arch]
                            and self.macros_by_arch[arch][macro]
                            != self.macros_by_arch[other_arch][macro]
                        ):
                            self.multi_value_macros.add(macro)

        # Resolve arch-specific macros
        for arch in arches:
            if arch in self.macros_by_arch:
                resolved_macros = {
                    name: replace_macros(value, spec=self, arch=arch)
                    for name, value in self.macros_by_arch[arch].items()
                }
                self.macros_by_arch[arch] = resolved_macros

        # Resolve global macros
        self.macros = {
            name: replace_macros(value, spec=self)
            for name, value in self.macros.items()
        }

        # Resolve sources_dict
        self.sources_dict = {
            key: {
                source_name: replace_macros(
                    value, spec=self, arch=key if key != "global" else None
                )
                for source_name, value in self.sources_dict[key].items()
            }
            for key in self.sources_dict
        }

        # Resolve patches_dict
        self.patches_dict = {
            key: {
                patch_name: replace_macros(
                    value, spec=self, arch=key if key != "global" else None
                )
                for patch_name, value in self.patches_dict[key].items()
            }
            for key in self.patches_dict
        }

        # Resolve sources
        resolved_sources = []
        for source in self.sources:
            macro_names = [
                m.group(1) for m in re.finditer(_macro_pattern, source)
            ]
            has_multi_value_macro = (
                any(macro in self.multi_value_macros for macro in macro_names)
                or "%{_arch}" in source
            )
            if has_multi_value_macro:
                resolved_sources.extend(
                    replace_macros(source, spec=self, arch=arch)
                    for arch in arches
                )
            else:
                resolved_sources.append(replace_macros(source, spec=self))
        self.sources = resolved_sources

        # Resolve patches
        resolved_patches = []
        for patch in self.patches:
            macro_names = [
                m.group(1) for m in re.finditer(_macro_pattern, patch)
            ]
            has_multi_value_macro = (
                any(macro in self.multi_value_macros for macro in macro_names)
                or "%{_arch}" in patch
            )
            if has_multi_value_macro:
                resolved_patches.extend(
                    replace_macros(patch, spec=self, arch=arch)
                    for arch in arches
                )
            else:
                resolved_patches.append(replace_macros(patch, spec=self))
        self.patches = resolved_patches

    def packages_dict(self):
        assert self.packages
        return dict(
            zip([package.name for package in self.packages], self.packages)
        )

    @classmethod
    def from_file(cls, filename, macros={}):
        spec = cls()
        for name, value in macros.items():
            spec.macros[name] = value
        with open(filename, "r") as f:
            parse_context = {"current_subpackage": None, "current_arch": None}
            for line in f:
                spec, parse_context = _parse(spec, parse_context, line)
        spec.resolve_macros()
        return spec

    @classmethod
    def from_string(cls, string, macros={}):
        spec = cls()
        for name, value in macros.items():
            spec.macros[name] = value
        parse_context = {"current_subpackage": None, "current_arch": None}
        for line in string.splitlines():
            spec, parse_context = _parse(spec, parse_context, line)
        spec.resolve_macros()
        return spec


def _parse(spec_obj, context, line):
    if not line or line.startswith("#"):
        return spec_obj, context
    for tag in _tags:
        match = tag.test(line)
        if match:
            if "multiline" in context:
                context.pop("multiline", None)
            return tag.update(spec_obj, context, match, line)
    if "multiline" in context:
        target_obj = _Tag.current_target(spec_obj, context)
        previous_txt = getattr(target_obj, context["multiline"], "")
        if previous_txt is None:
            previous_txt = ""
        setattr(target_obj, context["multiline"], str(previous_txt) + line)
    return spec_obj, context


if __name__ == "__main__":
    pass
