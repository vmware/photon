"""
Exceptions for spec2git_lib module
"""


class SpecParseError(Exception):
    """Exception raised for spec file parsing errors"""
    pass


class PatchApplicationError(Exception):
    """Exception raised for patch application errors"""
    pass


class PatchConflictError(PatchApplicationError):
    """Exception raised when a patch conflict occurs and manual resolution is needed"""
    pass


class ValidationError(Exception):
    """Exception raised for input validation errors"""
    pass


class PrepExecutionError(SpecParseError):
    """Base class for %prep section execution errors"""
    pass


class PrepCommandFailure(PrepExecutionError):
    """Exception raised when a command in %prep section fails"""

    def __init__(self, command: str, exit_code: int, stderr: str):
        self.command = command
        self.exit_code = exit_code
        self.stderr = stderr
        super().__init__(
            f"Prep command failed (exit code {exit_code}):\n"
            f"Command: {command}\n"
            f"Error: {stderr}"
        )


class PrepTimeoutError(PrepExecutionError):
    """Exception raised when prep execution exceeds timeout"""
    pass


class PrepSecurityError(PrepExecutionError):
    """Exception raised when a potentially dangerous command is detected"""
    pass

