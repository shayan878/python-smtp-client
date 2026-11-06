"""Educational SMTP submission client implemented with Python sockets."""

from __future__ import annotations

import base64
import socket
import ssl
from dataclasses import dataclass
from email.message import EmailMessage
from email.policy import SMTP as SMTP_POLICY
from typing import Iterable


@dataclass(frozen=True)
class SMTPResponse:
    """A complete SMTP reply, including continuation lines."""

    code: int
    lines: tuple[str, ...]

    @property
    def message(self) -> str:
        return " ".join(line[4:] for line in self.lines)


class SMTPError(RuntimeError):
    """Raised when an SMTP operation fails."""


class SMTPClient:
    """Minimal SMTP submission client requiring STARTTLS by default."""

    def __init__(self, host: str, port: int = 587, timeout: float = 15.0) -> None:
        if not host or not 1 <= port <= 65535 or timeout <= 0:
            raise ValueError("Provide a host, valid port, and positive timeout.")
        self.host, self.port, self.timeout = host, port, timeout
        self._context = ssl.create_default_context()
        self._socket: socket.socket | ssl.SSLSocket | None = None
        self._reader = None
        self._tls = False

    def connect(self) -> SMTPResponse:
        """Connect, greet, negotiate STARTTLS, and issue EHLO again."""
        if self._socket is not None:
            raise SMTPError("Already connected.")
        raw = socket.create_connection((self.host, self.port), self.timeout)
        self._socket, self._reader = raw, raw.makefile("rb")
        try:
            self._expect(self._read(), {220}, "greeting")
            hostname = socket.getfqdn() or "localhost"
            hello = self._command(f"EHLO {hostname}", {250})
            if "STARTTLS" not in " ".join(hello.lines).upper():
                raise SMTPError("Server does not advertise STARTTLS.")
            self._command("STARTTLS", {220})
            self._reader.close()
            self._socket = self._context.wrap_socket(raw, server_hostname=self.host)
            self._reader = self._socket.makefile("rb")
            self._tls = True
            return self._command(f"EHLO {hostname}", {250})
        except Exception:
            self.close()
            raise

    def authenticate(self, username: str, password: str) -> SMTPResponse:
        """Authenticate using AUTH PLAIN only after TLS is active."""
        if not self._tls:
            raise SMTPError("Refusing to send credentials without TLS.")
        if not username or not password:
            raise ValueError("Username and password must not be empty.")
        token = base64.b64encode(b"\0" + username.encode() + b"\0" + password.encode()).decode("ascii")
        return self._command(f"AUTH PLAIN {token}", {235})

    def send_message(self, sender: str, recipients: Iterable[str], message: EmailMessage) -> SMTPResponse:
        """Submit an email using SMTP envelope commands and DATA."""
        self._validate_address(sender)
        targets = list(recipients)
        if not targets:
            raise ValueError("At least one recipient is required.")
        for target in targets:
            self._validate_address(target)
        self._command(f"MAIL FROM:<{sender}>", {250})
        for target in targets:
            self._command(f"RCPT TO:<{target}>", {250, 251})
        self._command("DATA", {354})
        payload = message.as_bytes(policy=SMTP_POLICY)
        if not payload.endswith(b"\r\n"):
            payload += b"\r\n"
        payload = b"\r\n".join(b"." + line if line.startswith(b".") else line for line in payload.split(b"\r\n"))
        self._require_socket().sendall(payload + b".\r\n")
        response = self._read()
        self._expect(response, {250}, "message submission")
        return response

    def quit(self) -> SMTPResponse:
        """Send QUIT and close the connection."""
        try:
            return self._command("QUIT", {221})
        finally:
            self.close()

    def close(self) -> None:
        """Close reader and socket safely."""
        reader, connection = self._reader, self._socket
        self._reader = self._socket = None
        self._tls = False
        if reader is not None:
            try:
                reader.close()
            except OSError:
                pass
        if connection is not None:
            try:
                connection.close()
            except OSError:
                pass

    def _command(self, command: str, expected: set[int]) -> SMTPResponse:
        if "\r" in command or "\n" in command:
            raise ValueError("SMTP command contains a line break.")
        self._require_socket().sendall(command.encode("ascii") + b"\r\n")
        response = self._read()
        self._expect(response, expected, command.split(" ", 1)[0])
        return response

    def _read(self) -> SMTPResponse:
        if self._reader is None:
            raise SMTPError("Not connected.")
        raw = self._reader.readline()
        if not raw:
            raise SMTPError("SMTP server closed the connection.")
        lines = [raw.decode("utf-8", "replace").rstrip("\r\n")]
        code, separator = self._parse(lines[0])
        while separator == "-":
            raw = self._reader.readline()
            if not raw:
                raise SMTPError("SMTP server closed a multi-line reply.")
            line = raw.decode("utf-8", "replace").rstrip("\r\n")
            next_code, separator = self._parse(line)
            if next_code != code:
                raise SMTPError("Inconsistent SMTP status codes.")
            lines.append(line)
        return SMTPResponse(code, tuple(lines))

    @staticmethod
    def _parse(line: str) -> tuple[int, str]:
        if len(line) < 4 or not line[:3].isdigit() or line[3] not in " -":
            raise SMTPError(f"Malformed SMTP reply: {line!r}")
        return int(line[:3]), line[3]

    @staticmethod
    def _expect(response: SMTPResponse, expected: set[int], operation: str) -> None:
        if response.code not in expected:
            raise SMTPError(f"{operation} failed: SMTP {response.code} {response.message}")

    @staticmethod
    def _validate_address(address: str) -> None:
        if not address or "@" not in address or any(c.isspace() or c in "<>\r\n" for c in address):
            raise ValueError(f"Invalid SMTP envelope address: {address!r}")
        try:
            address.encode("ascii")
        except UnicodeEncodeError as exc:
            raise ValueError("SMTPUTF8 envelope addresses are not supported.") from exc

    def _require_socket(self) -> socket.socket | ssl.SSLSocket:
        if self._socket is None:
            raise SMTPError("Not connected.")
        return self._socket
