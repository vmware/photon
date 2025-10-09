"""
Unit tests for GitOperations

Tests git operations in isolation with mocked subprocess calls.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import subprocess

from spec2git_lib.git_operations import GitOperations, extract_patch_metadata
from common.exceptions import SpecParseError


class TestGitOperations:
    """Test GitOperations class"""

    def test_init(self, tmp_path):
        """Test initialization"""
        git_ops = GitOperations(tmp_path)
        assert git_ops.repo_path == tmp_path
        assert git_ops.default_timeout == 60

    @patch('subprocess.run')
    def test_run_command_success(self, mock_run, tmp_path):
        """Test successful command execution"""
        mock_run.return_value = Mock(returncode=0, stdout="output", stderr="")

        git_ops = GitOperations(tmp_path)
        result = git_ops.run_command(['git', 'status'])

        assert result.returncode == 0
        assert result.stdout == "output"
        mock_run.assert_called_once()

    @patch('subprocess.run')
    def test_run_command_failure(self, mock_run, tmp_path):
        """Test failed command raises error"""
        mock_run.return_value = Mock(returncode=1, stdout="", stderr="error")

        git_ops = GitOperations(tmp_path)
        with pytest.raises(SpecParseError, match="Git command failed"):
            git_ops.run_command(['git', 'status'], check=True)

    @patch('subprocess.run')
    def test_run_command_timeout(self, mock_run, tmp_path):
        """Test timeout raises error"""
        mock_run.side_effect = subprocess.TimeoutExpired(['git', 'status'], 60)

        git_ops = GitOperations(tmp_path)
        with pytest.raises(SpecParseError, match="timed out"):
            git_ops.run_command(['git', 'status'])

    @patch('subprocess.run')
    def test_init_repository(self, mock_run, tmp_path):
        """Test repository initialization"""
        mock_run.return_value = Mock(returncode=0, stdout="", stderr="")

        git_ops = GitOperations(tmp_path)
        git_ops.init_repository()

        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert 'git' in args
        assert 'init' in args

    @patch('subprocess.run')
    def test_add_all(self, mock_run, tmp_path):
        """Test staging all changes"""
        mock_run.return_value = Mock(returncode=0, stdout="", stderr="")

        git_ops = GitOperations(tmp_path)
        git_ops.add_all()

        args = mock_run.call_args[0][0]
        assert 'git' in args
        assert 'add' in args
        assert '.' in args

    @patch('subprocess.run')
    def test_commit_with_author(self, mock_run, tmp_path):
        """Test commit with author information"""
        mock_run.return_value = Mock(returncode=0, stdout="", stderr="")

        git_ops = GitOperations(tmp_path)
        git_ops.commit("Test message", author_name="John Doe", author_email="john@example.com")

        args = mock_run.call_args[0][0]
        assert 'commit' in args
        assert '--author' in args
        assert 'John Doe <john@example.com>' in args

    @patch('subprocess.run')
    def test_commit_allow_empty(self, mock_run, tmp_path):
        """Test commit with allow_empty flag"""
        mock_run.return_value = Mock(returncode=0, stdout="", stderr="")

        git_ops = GitOperations(tmp_path)
        git_ops.commit("Empty commit", allow_empty=True)

        args = mock_run.call_args[0][0]
        assert '--allow-empty' in args

    @patch('subprocess.run')
    def test_get_commits_after(self, mock_run, tmp_path):
        """Test getting commits after a base"""
        mock_run.return_value = Mock(
            returncode=0,
            stdout="abc123\ndef456\nghi789\n",
            stderr=""
        )

        git_ops = GitOperations(tmp_path)
        commits = git_ops.get_commits_after("base123")

        assert len(commits) == 3
        assert commits[0] == "abc123"
        assert commits[1] == "def456"
        assert commits[2] == "ghi789"

    @patch('subprocess.run')
    def test_get_commits_after_empty(self, mock_run, tmp_path):
        """Test getting commits with no results"""
        mock_run.return_value = Mock(returncode=0, stdout="", stderr="")

        git_ops = GitOperations(tmp_path)
        commits = git_ops.get_commits_after("base123")

        assert commits == []

    @patch('subprocess.run')
    def test_get_commit_hash(self, mock_run, tmp_path):
        """Test resolving reference to hash"""
        mock_run.return_value = Mock(returncode=0, stdout="abc123def456\n", stderr="")

        git_ops = GitOperations(tmp_path)
        commit_hash = git_ops.get_commit_hash("HEAD")

        assert commit_hash == "abc123def456"

    @patch('subprocess.run')
    def test_format_patch(self, mock_run, tmp_path):
        """Test generating patch content"""
        patch_content = "From abc123\nSubject: Test patch\n\ndiff --git\n"
        mock_run.return_value = Mock(returncode=0, stdout=patch_content, stderr="")

        git_ops = GitOperations(tmp_path)
        result = git_ops.format_patch("abc123")

        assert result == patch_content

    @patch('subprocess.run')
    def test_get_commit_subject(self, mock_run, tmp_path):
        """Test getting commit subject"""
        mock_run.return_value = Mock(returncode=0, stdout="Fix critical bug\n", stderr="")

        git_ops = GitOperations(tmp_path)
        subject = git_ops.get_commit_subject("abc123")

        assert subject == "Fix critical bug"

    @patch('subprocess.run')
    def test_get_commit_author(self, mock_run, tmp_path):
        """Test getting commit author"""
        mock_run.side_effect = [
            Mock(returncode=0, stdout="John Doe\n", stderr=""),
            Mock(returncode=0, stdout="john@example.com\n", stderr="")
        ]

        git_ops = GitOperations(tmp_path)
        name, email = git_ops.get_commit_author("abc123")

        assert name == "John Doe"
        assert email == "john@example.com"

    @patch('subprocess.run')
    def test_get_config_exists(self, mock_run, tmp_path):
        """Test getting existing config value"""
        mock_run.return_value = Mock(returncode=0, stdout="John Doe\n", stderr="")

        git_ops = GitOperations(tmp_path)
        value = git_ops.get_config("user.name")

        assert value == "John Doe"

    @patch('subprocess.run')
    def test_get_config_not_exists(self, mock_run, tmp_path):
        """Test getting non-existent config"""
        mock_run.return_value = Mock(returncode=1, stdout="", stderr="")

        git_ops = GitOperations(tmp_path)
        value = git_ops.get_config("nonexistent.key")

        assert value is None

    @patch('subprocess.run')
    def test_search_log_found(self, mock_run, tmp_path):
        """Test searching log with match"""
        mock_run.return_value = Mock(returncode=0, stdout="abc123\n", stderr="")

        git_ops = GitOperations(tmp_path)
        result = git_ops.search_log("Initial commit")

        assert result == "abc123"

    @patch('subprocess.run')
    def test_search_log_not_found(self, mock_run, tmp_path):
        """Test searching log with no match"""
        mock_run.return_value = Mock(returncode=1, stdout="", stderr="")

        git_ops = GitOperations(tmp_path)
        result = git_ops.search_log("Nonexistent pattern")

        assert result is None

    @patch('subprocess.run')
    def test_get_status(self, mock_run, tmp_path):
        """Test getting repository status"""
        mock_run.return_value = Mock(returncode=0, stdout=" M file.txt\n", stderr="")

        git_ops = GitOperations(tmp_path)
        status = git_ops.get_status()

        assert " M file.txt" in status

    @patch('subprocess.run')
    def test_reset_hard(self, mock_run, tmp_path):
        """Test hard reset"""
        mock_run.return_value = Mock(returncode=0, stdout="", stderr="")

        git_ops = GitOperations(tmp_path)
        git_ops.reset_hard()

        args = mock_run.call_args[0][0]
        assert 'reset' in args
        assert '--hard' in args

    @patch('subprocess.run')
    def test_clean(self, mock_run, tmp_path):
        """Test cleaning untracked files"""
        mock_run.return_value = Mock(returncode=0, stdout="", stderr="")

        git_ops = GitOperations(tmp_path)
        git_ops.clean()

        args = mock_run.call_args[0][0]
        assert 'clean' in args
        assert '-fd' in args

    def test_repository_exists(self, tmp_path):
        """Test checking if repository exists"""
        git_ops = GitOperations(tmp_path)

        # Should not exist initially
        assert not git_ops.repository_exists()

        # Create .git directory
        (tmp_path / '.git').mkdir()
        assert git_ops.repository_exists()


class TestExtractPatchMetadata:
    """Test patch metadata extraction"""

    def test_extract_basic_metadata(self):
        """Test extracting basic commit info"""
        patch = """From abc123 Mon Sep 17 00:00:00 2001
From: John Doe <john@example.com>
Date: Mon, 17 Sep 2024 12:00:00 +0000
Subject: [PATCH] Fix critical bug

This patch fixes a critical bug in the system.

---
 file.c | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
"""
        message, name, email = extract_patch_metadata(patch)

        assert "Fix critical bug" in message
        assert name == "John Doe"
        assert email == "john@example.com"

    def test_extract_without_bracket_prefix(self):
        """Test subject without [PATCH] prefix"""
        patch = """From abc123
From: Jane Smith <jane@example.com>
Subject: Fix memory leak

Description here.

---
diff --git
"""
        message, name, email = extract_patch_metadata(patch)

        assert message.startswith("Fix memory leak")
        assert name == "Jane Smith"
        assert email == "jane@example.com"

    def test_extract_email_only(self):
        """Test extracting email without name"""
        patch = """From: user@example.com
Subject: Quick fix

---
diff --git
"""
        message, name, email = extract_patch_metadata(patch)

        assert "Quick fix" in message
        assert email == "user@example.com"

    def test_extract_with_description(self):
        """Test extracting with multi-line description"""
        patch = """From abc123
From: Dev <dev@example.com>
Subject: Major refactoring

This is a longer description
that spans multiple lines.

It has multiple paragraphs.

---
diff --git
"""
        message, name, email = extract_patch_metadata(patch)

        assert "Major refactoring" in message
        assert "longer description" in message
        assert "multiple paragraphs" in message

    def test_extract_no_metadata(self):
        """Test with minimal patch"""
        patch = """diff --git a/file.c b/file.c
--- a/file.c
+++ b/file.c
"""
        message, name, email = extract_patch_metadata(patch)

        # Should return defaults
        assert message == "Imported patch"
        assert name is None
        assert email is None




