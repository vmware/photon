#!/usr/bin/env python3

import sys
import logging
import tempfile
import subprocess
import argparse
import os
import yaml
import os.path
import shutil
from pathlib import Path

from filecmp import dircmp, DEFAULT_IGNORES

yaml.emitter.Emitter.prepare_tag = lambda self, tag: ""

SOURCE_SUPPLIER = "Organization: Broadcom, Inc."


class SpdxInfo(object):
    def __init__(
        self,
        supplier,
        license_declared,
        license_concluded,
        home_page,
        short_summary,
        detailed_description,
    ):
        self.package = {
            "supplier": supplier,
            "license_declared": license_declared,
            "license_concluded": license_concluded,
            "home_page": home_page,
            "short_summary": short_summary,
            "detailed_description": detailed_description,
        }


class SourceSchematic(object):
    def __init__(self, source_uid, sources_url, archive_name, archive_spdx: SpdxInfo):
        self.schema_id = "1.1"
        self.spdx_templates = {"spdx": archive_spdx}
        self.outputs = {}
        self.outputs[source_uid] = {
            "url_base": sources_url,
            "manifest": [{"$(env:PHOTON_SOURCES_PATH)": {"include": [archive_name]}}],
            "manifest_root": "./",
            "merge_spdx_template": "spdx",
        }


class Source(object):
    def __init__(
        self,
        archive,
        archive_type,
        archive_sha512sum,
        spdx: SpdxInfo,
        name=None,
        version="unknown",
        skip_validation=False,
    ):
        self.archive = archive
        self.archive_sha512sum = archive_sha512sum
        self.name = name if name else archive
        self.version = version
        self.archive_type = archive_type
        self.spdx = spdx
        self.skip_validation = skip_validation


class UpstreamSource(Source):
    def __init__(
        self,
        archive,
        archive_sha512sum,
        spdx: SpdxInfo,
        version="unknown",
        name=None,
        url=None,
        repo_url=None,
        commit_id=None,
        skip_list=list(),
        missing=list(),
        skip_validation=False,
    ):
        Source.__init__(
            self,
            archive=archive,
            archive_type="upstream",
            archive_sha512sum=archive_sha512sum,
            name=name,
            version=version,
            spdx=spdx,
            skip_validation=skip_validation,
        )
        self.url = url
        self.repo_url = repo_url
        self.commit_id = commit_id
        self.skip_list = skip_list
        self.missing = missing


class CustomSource(Source):
    def __init__(
        self,
        archive,
        spdx: SpdxInfo,
        archive_sha512sum="",
        version="unknown",
        name=None,
        env: dict = {},
        script: list[str] = [],
        skip_validation=False,
    ):
        Source.__init__(
            self,
            archive=archive,
            archive_type="custom",
            archive_sha512sum=archive_sha512sum,
            name=name,
            version=version,
            spdx=spdx,
            skip_validation=skip_validation,
        )
        self.script = script
        self.script = script
        self.env = env


class SourceArchiveHelper(object):
    def __init__(self, argv):
        logging.getLogger().setLevel(logging.INFO)
        parser = argparse.ArgumentParser(
            description="Tool to help with source code archive metadata",
            usage="""photon_source_archive_helper <command> [<args>]

Commands
    custom_source  generates a new yaml file or appends a new section to existing file to represent a custom source
    upstream_source  generates a new yaml file or appends a new section to existing file to represent a upstream source
    build generates one or more schematic files for a source archive yaml
""",
        )
        parser.add_argument("command", help="generate or validate a source yaml file")
        args = parser.parse_args(argv[1:2])
        self.argv = argv
        getattr(self, args.command)()

    def _writeYaml(self, sourceInfo, outputFile):
        outputFilePath = Path(outputFile)
        if not outputFilePath.is_file():
            outputFilePath.parent.mkdir(exist_ok=True, parents=True)
            with open(outputFilePath, "w") as file:
                file.write("sources: []")

        conf = yaml.safe_load(outputFilePath.read_text())
        if conf is None:
            conf = {}
        if "sources" not in conf:
            conf["sources"] = []

        with open(
            outputFilePath,
            "w",
        ) as f:
            sources_list = conf["sources"]
            if isinstance(sources_list, list):
                sources_list.append(sourceInfo)
                yaml.dump(
                    conf,
                    f,
                    sort_keys=False,
                    default_flow_style=False,
                    width=float("inf"),
                )
                print(f"Written to file {outputFilePath} successfully")

    def _add_source_args(self, parser):
        parser.add_argument("--name", required=True)
        parser.add_argument("--version", required=True)
        parser.add_argument("--archive", required=True)
        parser.add_argument("--license", required=True)
        parser.add_argument("--archive-sha512sum", required=True)
        parser.add_argument("--home", required=True, default="")
        parser.add_argument("--summary", required=True, default="")
        parser.add_argument("--description", required=True, default="")
        parser.add_argument("--output", required=True)

    def upstream_source(self):
        parser = argparse.ArgumentParser(description="Generate yaml")
        self._add_source_args(parser)
        parser.add_argument("upstream_source", help="generate source yaml file")
        parser.add_argument("--url", required=True)
        parser.add_argument("--repo-url", required=True)
        parser.add_argument("--commit-id", required=True)
        parser.add_argument("--sources", required=True)

        args = parser.parse_args(self.argv[1:])

        spdxInfo = SpdxInfo(
            supplier=SOURCE_SUPPLIER,
            license_declared=args.license,
            license_concluded=args.license,
            home_page=args.home,
            short_summary=args.summary,
            detailed_description=args.description,
        )
        source = UpstreamSource(
            name=args.name,
            version=args.version,
            archive=args.archive,
            archive_sha512sum=args.archive_sha512sum,
            url=args.url,
            repo_url=args.repo_url,
            commit_id=args.commit_id,
            skip_list=[],
            missing=[],
            spdx=spdxInfo,
        )
        archive, diff_list, missing_list = self._verifySingleSource(source, args.sources)
        source.skip_list = diff_list
        source.missing = missing_list
        self._writeYaml(source, args.output)

    def custom_source(self):
        parser = argparse.ArgumentParser(description="Generate yaml")
        parser.add_argument("custom_source", help="generate source yaml file")
        self._add_source_args(parser)
        args = parser.parse_args(self.argv[1:])

        spdxInfo = SpdxInfo(
            supplier=SOURCE_SUPPLIER,
            license_declared=args.license,
            license_concluded=args.license,
            home_page=args.home,
            short_summary=args.summary,
            detailed_description=args.description,
        )
        source = CustomSource(
            name=args.name,
            version=args.version,
            archive=args.archive,
            spdx=spdxInfo,
        )
        self._writeYaml(source, args.output)

    def _download_source(self, srcdir, downloadedFile, sourceFileUrl):
        self._run(
            srcdir, f"curl -k -L -o {downloadedFile} -f {sourceFileUrl}".split()
        )

    def build(self):
        parser = argparse.ArgumentParser(description="build")
        parser.add_argument("yaml")
        parser.add_argument("--sources-url", required=True)
        parser.add_argument("--outdir", required=True)
        parser.add_argument("--sources", required=True)
        args = parser.parse_args(self.argv[2:])
        sourcesLocation = args.sources
        sourcesURLBase = args.sources_url
        outdir = args.outdir
        if args.yaml:
            files = self._load(args.yaml)
            for sourceFile in files:
                if sourceFile.archive_type == "custom":
                    self._generateArchive(sourceFile, sourcesLocation)
                elif (
                    sourceFile.archive_type == "upstream"
                    and not sourceFile.skip_validation
                ):
                    archive, diff_list, missing_list = self._verifySingleSource(sourceFile, sourcesLocation)
                    if diff_list or missing_list:
                        logging.error(
                            f"source {sourceFile.name} files do not match with provided commit id."
                        )
                        logging.info(
                            f"diff_list: {diff_list}, hint: add them to skip_list to stop comparing."
                        )
                        logging.info(
                            f"missing: {missing_list}, hint: add them to missing list if appropriate."
                        )
                        # clean downloaded source
                        shutil.rmtree(
                            archive, ignore_errors=False
                        )
                        sys.exit(1)
                    else:
                        logging.info(f"source {sourceFile.name} validated succesfuly.")
                else:
                    logging.warning(
                        f"source {sourceFile.name} has unknown type {sourceFile.archive_type}"
                    )
                    downloadedFile = f"{sourcesLocation}/{sourceFile.archive}"
                    sourceFileUrl = f"{sourcesURLBase}/{sourceFile.archive}"
                    self._download_source(sourcesLocation,downloadedFile, sourceFileUrl)
                self._writeSchematic(
                    outdir, sourceFile, sourcesLocation, sourcesURLBase
                )

    def _generateArchive(self, sourceFile, sourcesLocation):
        tmpdir = tempfile.mkdtemp()
        script = sourceFile.script
        generator_script_file = open(os.path.join(tmpdir, "source_generator.sh"), "w")
        for line in script:
            generator_script_file.write(line)
        generator_script_file.close()
        logging.error(f"Archive {sourceFile.archive} being generated in {tmpdir}.")
        self._run(tmpdir, "bash source_generator.sh".split())
        generated_archive = os.path.join(tmpdir, sourceFile.archive)
        if os.path.isfile(generated_archive):
            shutil.copyfile(
                generated_archive, os.path.join(sourcesLocation, sourceFile.archive)
            )
        else:
            logging.error(f"Archive {sourceFile.archive} not generated in {tmpdir}.")

    def _writeSchematic(
        self,
        outdir,
        sourceFile: Source,
        sourcesLocation,
        sourcesURLBase,
    ):
        source_schematic = SourceSchematic(
            source_uid=self._source_uid(
                sourceFile.archive, sourceFile.archive_sha512sum
            ),
            sources_url=sourcesURLBase,
            archive_name=sourceFile.archive,
            archive_spdx=sourceFile.spdx,
        )
        source_dir = sourceFile.name
        source_dir_path = os.path.join(outdir, source_dir)
        if not os.path.exists(source_dir_path):
            os.makedirs(source_dir_path)
        schematic_file_path = os.path.join(
            source_dir_path, f"{sourceFile.archive}.schematic.yaml"
        )
        with open(
            schematic_file_path,
            "w",
        ) as f:
            yaml.dump(
                source_schematic,
                f,
                sort_keys=False,
                default_flow_style=False,
                width=float("inf"),
            )
            print(f"Written to file {schematic_file_path} successfully")

    def _load(self, configPath):
        files = []
        with open(configPath, "rb") as configFile:
            config = yaml.safe_load(configFile)
            sources = []
            sources = config.get("sources", [])
            if not sources:
                logging.error("missing sources in package configuration")
                sys.exit(1)

            for source in sources:
                # processing one source entry
                if source and type(source) is dict:
                    archive = source.get("archive")
                    archive_sha512sum = source.get("archive_sha512sum")
                    archive_type = source.get("archive_type", "unknown")

                    name = source.get("name")
                    version = source.get("version", "")

                    source_spdx = source["spdx"]["package"]
                    spdxInfo = SpdxInfo(
                        supplier=SOURCE_SUPPLIER,
                        license_declared=source_spdx["license_declared"],
                        license_concluded=source_spdx["license_concluded"],
                        home_page=source_spdx["home_page"],
                        short_summary=source_spdx["short_summary"],
                        detailed_description=source_spdx["detailed_description"],
                    )
                    if archive_type == "custom":
                        env = {}
                        script = source.get("script", [])
                        env = source.get("env", {})
                        source = CustomSource(
                            name=name,
                            version=version,
                            archive=archive,
                            archive_sha512sum=archive_sha512sum,
                            script=script,
                            env=env,
                            spdx=spdxInfo,
                        )
                    elif archive_type == "upstream":
                        url = source.get("url")
                        repo_url = source.get("repo_url")
                        commit_id = source.get("commit_id")
                        skip_list = DEFAULT_IGNORES + source.get("skip_list", [])
                        missing = source.get("missing", [])

                        source = UpstreamSource(
                            name=name,
                            version=version,
                            archive=archive,
                            archive_sha512sum=archive_sha512sum,
                            url=url,
                            repo_url=repo_url,
                            commit_id=commit_id,
                            skip_list=skip_list,
                            missing=missing,
                            spdx=spdxInfo,
                        )
                    else:
                        source = Source(
                            name=name,
                            version=version,
                            archive=archive,
                            archive_sha512sum=archive_sha512sum,
                            archive_type=archive_type,
                            spdx=spdxInfo,
                        )

                    files.append(source)
        return files

    def _verifySingleSource(self, sourceFile, sourcesLocation):
        with tempfile.TemporaryDirectory() as tmpdir:
            extractedDir = f"{tmpdir}/extracted"
            repoDir = f"{tmpdir}/repo"
            projectDir = f"{repoDir}/{sourceFile.name}"
            downloadedFile = f"{sourcesLocation}/{sourceFile.archive}"
            extractedProject = f"{tmpdir}/extracted/{sourceFile.name}"
            os.mkdir(repoDir)
            os.mkdir(projectDir)
            os.mkdir(extractedDir)
            # Download and extract source
            self._download_source(tmpdir, downloadedFile, sourceFile.url)
            # Extract the source
            self._run(extractedDir, f"tar -xf {downloadedFile}".split())
            self._run(projectDir, "git init .".split())
            self._run(
                projectDir, f"git remote add origin {sourceFile.repo_url}".split()
            )
            self._run(
                projectDir,
                f"git -c advice.detachedHead=false fetch --depth 1 origin {sourceFile.commit_id}".split(),
            )
            self._run(
                projectDir,
                "git -c advice.detachedHead=false checkout FETCH_HEAD".split(),
            )
            # Compare both the trees
            logging.info(f"skip {sourceFile.skip_list}, missing {sourceFile.missing}")
            treediff = dircmp(
                projectDir,
                extractedProject,
                ignore=sourceFile.skip_list + sourceFile.missing,
            )
            fileDiff, missing = self._detectTreeDiff(treediff)
            return downloadedFile, fileDiff, missing

    def _detectTreeDiff(self, treediff):
        fileDiff = set()
        missing = set()
        if treediff.diff_files:
            fileDiff = fileDiff.union(set(treediff.diff_files))
            logging.warning(
                "diff %s found in %s and %s"
                % (treediff.diff_files, treediff.left, treediff.right)
            )

        if treediff.left_only:
            missing = missing.union(set(treediff.left_only))
            logging.warning(
                "left only %s found in %s and %s"
                % (treediff.left_only, treediff.left, treediff.right)
            )

        if treediff.right_only:
            missing = missing.union(set(treediff.right_only))
            logging.warning(
                "right only files %s found in %s and %s"
                % (treediff.right_only, treediff.left, treediff.right)
            )

        for subTreeDiff in treediff.subdirs.values():
            subTreeFileDiff, subTreeMissing = self._detectTreeDiff(subTreeDiff)
            fileDiff = fileDiff.union(subTreeFileDiff)
            missing = missing.union(subTreeMissing)

        return fileDiff, missing

    def _source_uid(self, archive_name, build_id):
        return f"uid.obj.comp.fileset(org='photon.source',name='{archive_name}',build_id='{build_id}')"

    def _run(self, cwd, cmd):
        subprocess.run(
            args=cmd,
            cwd=cwd,
            check=True,
            stderr=sys.stderr,
            stdout=sys.stderr,
            stdin=subprocess.DEVNULL,
        )


if __name__ == "__main__":
    argv = sys.argv.copy()
    helper = SourceArchiveHelper(argv)
