"""Command-line interface for the SMTP client."""

import argparse
import os
import sys
from pathlib import Path

from .client import SMTPClient, SMTPError
from .message import build_message


def main() -> int:
    parser = argparse.ArgumentParser(description="Send plain-text email over SMTP.")
    parser.add_argument("--from", dest="sender", default=os.getenv("SMTP_FROM"))
    parser.add_argument("--to", nargs="+", dest="recipients")
    parser.add_argument("--subject", default="SMTP client message")
    body = parser.add_mutually_exclusive_group()
    body.add_argument("--body")
    body.add_argument("--body-file", type=Path)
    args = parser.parse_args()
    username, password = os.getenv("SMTP_USERNAME"), os.getenv("SMTP_PASSWORD")
    recipients = args.recipients or [x.strip() for x in os.getenv("SMTP_TO", "").split(",") if x.strip()]
    if not args.sender or not recipients or not username or not password:
        parser.error("Set SMTP_FROM, SMTP_USERNAME, SMTP_PASSWORD and --to/SMTP_TO.")
    try:
        content = args.body_file.read_text(encoding="utf-8") if args.body_file else args.body if args.body is not None else sys.stdin.read()
        message = build_message(args.sender, recipients, args.subject, content)
        client = SMTPClient(os.getenv("SMTP_HOST", "smtp.gmail.com"), int(os.getenv("SMTP_PORT", "587")), float(os.getenv("SMTP_TIMEOUT", "15")))
        try:
            client.connect()
            client.authenticate(username, password)
            response = client.send_message(args.sender, recipients, message)
            client.quit()
        except Exception:
            client.close()
            raise
    except (OSError, SMTPError, ValueError) as exc:
        print(f"SMTP delivery failed: {exc}", file=sys.stderr)
        return 1
    print(f"SMTP server accepted the message: {response.code} {response.message}")
    return 0
