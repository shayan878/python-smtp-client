import pytest

from smtp_client.client import SMTPClient, SMTPError


def test_multiline_reply_parser() -> None:
    assert SMTPClient._parse("250-STARTTLS") == (250, "-")
    assert SMTPClient._parse("250 OK") == (250, " ")


def test_authentication_requires_tls() -> None:
    with pytest.raises(SMTPError, match="without TLS"):
        SMTPClient("localhost").authenticate("user", "secret")


def test_malformed_reply_is_rejected() -> None:
    with pytest.raises(SMTPError, match="Malformed"):
        SMTPClient._parse("not an SMTP response")


def test_invalid_address_is_rejected() -> None:
    with pytest.raises(ValueError, match="Invalid SMTP envelope"):
        SMTPClient._validate_address("sender@example.com\r\nDATA")
