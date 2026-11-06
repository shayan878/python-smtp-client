# SMTP Client

A dependency-free educational SMTP submission client built with Python sockets. It demonstrates SMTP greeting, EHLO, STARTTLS, AUTH PLAIN, envelope delivery, DATA framing, and QUIT without delegating protocol handling to smtplib.

## Features
- Explicit SMTP command/response handling, including multi-line replies.
- STARTTLS with certificate and hostname verification; no plaintext fallback.
- AUTH PLAIN only after TLS is active.
- Correct envelope sender/recipient commands and DATA dot-stuffing.
- Environment-based secrets and command-line interface.
- Local unit tests; tests do not send real email.

## Install

```bash
git clone https://github.com/shayan878/SMTP.git
cd SMTP
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
```

## Configure and send

Set SMTP_HOST (default smtp.gmail.com), SMTP_PORT (default 587), SMTP_USERNAME, SMTP_PASSWORD, and SMTP_FROM in your shell. Use a provider-specific application password where required. Then run:

```bash
smtp-send --to recipient@example.com --subject 'SMTP test' --body 'Hello.'
```

Use multiple addresses after --to, --body-file for a UTF-8 text file, or omit both body options to read from standard input. SMTP_TO may also contain comma-separated recipients.

## Development

```bash
pytest
ruff check .
ruff format --check .
```

## Scope and limitations

This is an educational submission client, not a mail-transfer agent. It supports plain-text email and STARTTLS plus AUTH PLAIN. OAuth2, SMTPUTF8 envelope addresses, attachments, HTML alternatives, and provider-specific extensions are not implemented. A server's 250 response confirms submission acceptance, not inbox delivery. See docs/protocol.md and docs/security.md.
