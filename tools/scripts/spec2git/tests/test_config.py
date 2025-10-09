"""
Unit tests for configuration management

Tests the configuration system.
"""

import pytest
import os
from common.config import Spec2GitConfig, get_config, set_config, reset_config


class TestSpec2GitConfig:
    """Test configuration management"""

    def test_default_config_values(self):
        """Test default configuration values"""
        config = Spec2GitConfig()

        assert config.default_subprocess_timeout == 60
        assert config.chunk_size == 8192
        assert config.default_strip_level == 1
        assert config.diff_similarity_threshold == 0.70

    def test_config_from_environment(self, monkeypatch):
        """Test configuration from environment variables"""
        monkeypatch.setenv('SPEC2GIT_SUBPROCESS_TIMEOUT', '120')
        monkeypatch.setenv('SPEC2GIT_CHUNK_SIZE', '16384')

        config = Spec2GitConfig.from_environment()

        assert config.default_subprocess_timeout == 120
        assert config.chunk_size == 16384

    def test_invalid_env_values_ignored(self, monkeypatch):
        """Invalid environment values should be ignored and use defaults"""
        monkeypatch.setenv('SPEC2GIT_SUBPROCESS_TIMEOUT', 'invalid')
        monkeypatch.setenv('SPEC2GIT_CHUNK_SIZE', 'not_a_number')

        config = Spec2GitConfig.from_environment()

        # Should fall back to defaults
        assert config.default_subprocess_timeout == 60
        assert config.chunk_size == 8192

    def test_get_config_singleton(self):
        """get_config should return a singleton instance"""
        reset_config()
        config1 = get_config()
        config2 = get_config()

        assert config1 is config2

    def test_set_config(self):
        """Test setting custom configuration"""
        custom_config = Spec2GitConfig()
        custom_config.default_subprocess_timeout = 999

        set_config(custom_config)
        retrieved = get_config()

        assert retrieved.default_subprocess_timeout == 999

        # Clean up
        reset_config()

    def test_reset_config(self):
        """Test resetting configuration"""
        custom_config = Spec2GitConfig()
        custom_config.default_subprocess_timeout = 999
        set_config(custom_config)

        reset_config()
        retrieved = get_config()

        # Should be back to default
        assert retrieved.default_subprocess_timeout == 60




