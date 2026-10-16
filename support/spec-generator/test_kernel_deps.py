import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


module_spec = importlib.util.spec_from_file_location(
    "kernel_deps", Path(__file__).with_name("create-kernel-deps-specs-from-template.py")
)
module = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(module)


class KernelDepsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.specs = self.root / "SPECS"
        self.flavours = ["linux", "linux-esx", "linux-rt"]
        self.package = "kernels-drivers-intel-ice"
        for label, condition in [("", ">= 92"), ("91", "<= 91")]:
            directory = self.specs / label / "ice"
            directory.mkdir(parents=True)
            (directory / f"{self.package}.spec.in").write_text(
                f"%global build_if %{{photon_subrelease}} {condition}\n"
                "Version: %{PKG_VERSION}\nKernel: %{KERNEL_VERSION}-%{KERNEL_RELEASE}\n"
                f"Template: {label or 'base'}\n"
            )
            for flavour in self.flavours:
                (directory / f"{flavour}.spec").write_text(
                    f"%global build_if %{{photon_subrelease}} {condition}\n"
                    "Version: 6.12.111\nRelease: 3%{?dist}\n"
                )
        self.mapping = {
            "2.3.10": {"subrelease_max": 91, "flavours": ["linux", "linux-esx"],
                       "kernel_versions": ["v6.12"]},
            "2.6.7": {"subrelease_min": 92, "flavours": ["linux", "linux-esx"],
                      "kernel_versions": ["v6.12"]},
        }

    def generate(self, subrelease, mapping=None, config=False):
        matrix = self.root / "kernel-deps.json"
        matrix.write_text(json.dumps({
            "linux_flavour": self.flavours,
            "linux_dep_package": {self.package:
                self.mapping if mapping is None else mapping
            },
        }))
        with patch.dict(os.environ, {}, clear=True):
            if config:
                (self.root / "build-config.json").write_text(json.dumps({
                    "photon-build-param": {"photon-subrelease": subrelease}
                }))
            elif subrelease is not None:
                os.environ["PHOTON_SUBRELEASE"] = str(subrelease)
            module.main(str(matrix), [str(self.specs)])
        return sorted(self.specs.rglob("*drivers-intel-ice-*.spec"))

    def test_subrelease_boundaries_no_rt_and_stale_cleanup(self):
        for subrelease in [90, 91, 92, 93, 91]:
            with self.subTest(subrelease=subrelease):
                files = self.generate(subrelease)
                version = "2.3.10" if subrelease <= 91 else "2.6.7"
                label = "91" if subrelease <= 91 else "base"
                self.assertEqual(len(files), 2)
                self.assertEqual({p.name for p in files}, {
                    f"{flavour}-drivers-intel-ice-{version}-6.12.111.spec"
                    for flavour in ("linux", "linux-esx")
                })
                for path in files:
                    self.assertIn(f"Version: {version}\n", path.read_text())
                    self.assertIn(f"Template: {label}\n", path.read_text())

    def test_legacy_format_and_deduplication(self):
        files = self.generate(92, {"v6.12": {
            flavour: ["2.3.10", "2.6.7", "2.3.10"] for flavour in self.flavours
        }})
        self.assertEqual(len(files), 6)

    def test_legacy_format_without_subrelease_bounds(self):
        files = self.generate(91, {"v6.12": {"linux": ["2.3.10"]}})
        self.assertEqual(len(files), 1)
        self.assertIn("Version: 2.3.10\n", files[0].read_text())

    def test_config_fallback(self):
        files = self.generate(91, config=True)
        self.assertTrue(all("2.3.10" in p.name for p in files))
        self.assertEqual(len(files), 2)

    def test_environment_overrides_config(self):
        self.generate(91, config=True)
        files = self.generate(92)
        self.assertEqual(len(files), 2)
        self.assertTrue(all("2.6.7" in p.name for p in files))

    def test_conditional_versions_require_subrelease(self):
        with self.assertRaisesRegex(ValueError, "require a Photon subrelease"):
            self.generate(None)

    def test_invalid_ranges_fail(self):
        for entry in [{"subrelease_min": "92"},
                      {"subrelease_min": 92, "subrelease_max": 91}]:
            with self.subTest(entry=entry):
                with self.assertRaisesRegex(ValueError, "Invalid subrelease range"):
                    self.generate(92, {"2.6.7": {**self.mapping["2.6.7"], **entry}})

    def test_unmatched_range_generates_nothing(self):
        self.assertEqual(self.generate(92, {"2.3.10": self.mapping["2.3.10"]}), [])

    def test_shared_template_inherits_each_kernels_build_if(self):
        # A broad template must not broaden the selected kernel's scope.
        (self.specs / "91/ice" / f"{self.package}.spec.in").unlink()
        template = self.specs / "ice" / f"{self.package}.spec.in"
        template.write_text(template.read_text().replace(">= 92", ">= 91"))
        for flavour in self.flavours:
            kernel = self.specs / "91/ice" / f"{flavour}.spec"
            kernel.write_text(kernel.read_text().replace("<= 91", "== 91"))
        for subrelease, version in [(91, "2.3.10"), (92, "2.6.7")]:
            files = self.generate(subrelease)
            self.assertEqual(len(files), 2)
            condition = "== 91" if subrelease == 91 else ">= 92"
            for path in files:
                self.assertIn(f"Version: {version}\n", path.read_text())
                self.assertIn(f"%global build_if %{{photon_subrelease}} {condition}\n",
                              path.read_text())

    def test_build_if_placeholder_define_and_missing_gate(self):
        template = self.specs / "ice" / f"{self.package}.spec.in"
        original = template.read_text()
        for gate in ["%global build_if %{BUILD_FOR}",
                     "%define build_if %{photon_subrelease} >= 91", ""]:
            with self.subTest(gate=gate):
                template.write_text(original.replace(
                    "%global build_if %{photon_subrelease} >= 92", gate))
                files = self.generate(92)
                self.assertEqual(len(files), 2)
                for path in files:
                    self.assertEqual(path.read_text().count("%global build_if"), 1)
                    self.assertIn("%global build_if %{photon_subrelease} >= 92\n",
                                  path.read_text())

    def test_kernel_updates_change_output_without_changing_template(self):
        for flavour in self.flavours:
            kernel = self.specs / "91/ice" / f"{flavour}.spec"
            kernel.write_text(kernel.read_text().replace("<= 91", "== 91")
                              .replace("6.12.111", "6.12.120")
                              .replace("Release: 3", "Release: 9"))
        files = self.generate(91)
        self.assertEqual(len(files), 2)
        for path in files:
            self.assertIn("6.12.120.spec", path.name)
            self.assertIn("Kernel: 6.12.120-9%{?dist}\n", path.read_text())
            self.assertIn("%global build_if %{photon_subrelease} == 91\n",
                          path.read_text())

    def test_inactive_template_still_skipped(self):
        (self.specs / "91/ice" / f"{self.package}.spec.in").unlink()
        self.assertEqual(self.generate(91), [])

    def test_stale_non_intel_specs_removed_when_switching_subreleases(self):
        previous_package = self.package
        self.package = "kernels-drivers-bcm-bnxt_en"
        for directory in [self.specs / "ice", self.specs / "91/ice"]:
            (directory / f"{previous_package}.spec.in").rename(
                directory / f"{self.package}.spec.in")
        handwritten = self.specs / "ice" / f"{self.package}.spec"
        handwritten.write_text("hand-written spec\n")
        self.generate(91)
        self.generate(92)
        files = list(self.specs.rglob("*drivers-bcm-bnxt_en-*.spec"))
        self.assertEqual(len(files), 2)
        self.assertTrue(all("-2.6.7-" in path.name for path in files))
        self.assertTrue(handwritten.exists())

    def test_non_contiguous_subreleases(self):
        mapping = {
            "2.3.10": {"subreleases": [90, 92], "flavours": ["linux", "linux-esx"],
                       "kernel_versions": ["v6.12"]},
            "2.6.7": {"subreleases": [91], "flavours": ["linux", "linux-esx"],
                      "kernel_versions": ["v6.12"]},
        }
        for subrelease, version in [(90, "2.3.10"), (91, "2.6.7"), (92, "2.3.10")]:
            files = self.generate(subrelease, mapping)
            self.assertEqual(len(files), 2)
            self.assertTrue(all(f"-{version}-" in p.name for p in files))

    def test_kernel_series_filter(self):
        rule = {**self.mapping["2.6.7"], "kernel_versions": ["v6.1"]}
        self.assertEqual(self.generate(92, {"2.6.7": rule}), [])

    def test_invalid_subrelease_lists_fail(self):
        for value in [None, "91", ["91"], [True]]:
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError, "Invalid subrelease list"):
                    self.generate(91, {"2.3.10": {
                        **self.mapping["2.3.10"], "subreleases": value
                    }})

    def test_explicit_subreleases_require_known_subrelease(self):
        with self.assertRaisesRegex(ValueError, "require a Photon subrelease"):
            self.generate(None, {"2.6.7": {
                "subreleases": [91], "flavours": ["linux"],
                "kernel_versions": ["v6.12"]
            }})

    def test_separate_version_for_each_subrelease(self):
        mapping = {version: {
            "subrelease_min": subrelease, "subrelease_max": subrelease,
            "flavours": ["linux", "linux-esx"], "kernel_versions": ["v6.12"]
        } for subrelease, version in [(90, "2.3.10"), (91, "2.9.10"), (92, "2.6.7")]}
        for subrelease, version in [(90, "2.3.10"), (91, "2.9.10"), (92, "2.6.7")]:
            files = self.generate(subrelease, mapping)
            self.assertEqual(len(files), 2)
            self.assertTrue(all(f"-{version}-" in p.name for p in files))

    def test_optional_bounds(self):
        rule = {"flavours": ["linux"], "kernel_versions": ["v6.12"]}
        self.assertEqual(len(self.generate(92, {"2.6.7": rule})), 1)

    def test_legacy_and_version_indexed_entries_during_migration(self):
        mapping = {"v6.1": {"linux": ["1.13.7"]}, **self.mapping}
        files = self.generate(92, mapping)
        self.assertEqual(len(files), 2)
        self.assertTrue(all("-2.6.7-" in path.name for path in files))


if __name__ == "__main__":
    unittest.main()
