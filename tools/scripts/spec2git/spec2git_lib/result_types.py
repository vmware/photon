"""
Result and location types for spec2git operations

These types represent the results of various operations and locations of sources.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List, Dict
from enum import Enum


class SourceType(Enum):
    """Type of source location"""
    LOCAL = "local"
    GIT = "git"
    ARCHIVE = "archive"
    URL = "url"


@dataclass
class SourceLocation:
    """Base class for source locations"""
    source_type: SourceType
    source_num: int
    source_name: str


@dataclass
class LocalSourceLocation(SourceLocation):
    """Source file available locally"""
    local_path: Path

    def __init__(self, source_num: int, source_name: str, local_path: Path):
        super().__init__(SourceType.LOCAL, source_num, source_name)
        self.local_path = local_path


@dataclass
class GitSourceLocation(SourceLocation):
    """Source from git repository"""
    repo_url: str
    commit_id: str

    def __init__(self, source_num: int, source_name: str, repo_url: str, commit_id: str):
        super().__init__(SourceType.GIT, source_num, source_name)
        self.repo_url = repo_url
        self.commit_id = commit_id


@dataclass
class ArchiveSourceLocation(SourceLocation):
    """Source archive (may need download)"""
    url: Optional[str]
    local_path: Optional[Path]
    checksum: Optional[str]

    def __init__(self, source_num: int, source_name: str,
                 url: Optional[str] = None,
                 local_path: Optional[Path] = None,
                 checksum: Optional[str] = None):
        super().__init__(SourceType.ARCHIVE, source_num, source_name)
        self.url = url
        self.local_path = local_path
        self.checksum = checksum


@dataclass
class ExtractionResult:
    """Result of source extraction"""
    success: bool
    extracted_dir: Optional[Path]
    files_extracted: int
    error: Optional[str] = None


@dataclass
class PatchMetadata:
    """Metadata extracted from a patch file"""
    subject: str
    author_name: Optional[str] = None
    author_email: Optional[str] = None
    date: Optional[str] = None
    description: Optional[str] = None


@dataclass
class PatchResult:
    """Result of patch application"""
    success: bool
    patch_num: int
    patch_name: str
    commit_hash: Optional[str] = None
    files_changed: int = 0
    error: Optional[str] = None
    metadata: Optional[PatchMetadata] = None


@dataclass
class ConversionResult:
    """Result of complete conversion"""
    success: bool
    git_repo_path: Optional[Path] = None
    patches_applied: int = 0
    sources_downloaded: int = 0
    error: Optional[str] = None
    warnings: List[str] = None
    output_dir: Optional[Path] = None
    git_roots: Optional[set[str]] = None

    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []

