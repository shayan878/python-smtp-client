# SMTP protocol sequence

The client opens TCP, reads the 220 greeting, sends EHLO and parses the complete multi-line 250 response, requires STARTTLS, upgrades the connection with certificate verification, and sends EHLO again inside TLS. It then authenticates with AUTH PLAIN, submits MAIL FROM and one or more RCPT TO commands, sends DATA, and terminates message content with the SMTP dot terminator before QUIT.

A hyphen after the three-digit response code indicates a continuation line; a space marks the final line. A recipient may be accepted with 250 or 251. DATA begins after 354; successful submission is acknowledged with 250. DATA lines beginning with a period are dot-stuffed.

The current scope is STARTTLS plus AUTH PLAIN and plain-text messages. SMTPUTF8, OAuth2, attachments, and provider-specific extensions are not implemented.
