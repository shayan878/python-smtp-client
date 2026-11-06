"""Educational SMTP submission client."""

from .client import SMTPClient, SMTPError, SMTPResponse
from .message import build_message

__all__ = ["SMTPClient", "SMTPError", "SMTPResponse", "build_message"]
