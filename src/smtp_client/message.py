"""Plain-text email message construction."""

from email.message import EmailMessage


def build_message(sender: str, recipients: list[str], subject: str, body: str) -> EmailMessage:
    """Build a standard plain-text email message."""
    if not sender or not recipients:
        raise ValueError("A sender and at least one recipient are required.")
    message = EmailMessage()
    message["From"] = sender
    message["To"] = ", ".join(recipients)
    message["Subject"] = subject
    message.set_content(body)
    return message
