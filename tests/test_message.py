import pytest

from smtp_client.message import build_message


def test_message_headers_and_body() -> None:
    message = build_message("a@example.com", ["b@example.com"], "Subject", "Hello")
    assert message["From"] == "a@example.com"
    assert message["To"] == "b@example.com"
    assert message["Subject"] == "Subject"
    assert message.get_content() == "Hello\n"


def test_recipients_required() -> None:
    with pytest.raises(ValueError):
        build_message("a@example.com", [], "Subject", "Body")


def test_header_injection_rejected() -> None:
    with pytest.raises(ValueError):
        build_message("a@example.com", ["b@example.com"], "Hi\r\nBcc: x@y.com", "Body")
