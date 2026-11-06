"""Compatibility entry point for the refactored SMTP client."""

from smtp_client.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
