# Security considerations

- Never hard-code credentials or commit passwords, application passwords, or tokens.
- If a credential was ever committed, revoke or rotate it. Replacing a file does not remove secrets from Git history, forks, caches, or existing clones.
- The client requires STARTTLS and validates certificates and hostnames with Python's default SSL context. It does not downgrade to plaintext.
- AUTH PLAIN is Base64-encoded, not encrypted by itself; TLS supplies confidentiality.
- Environment variables avoid source-code literals but may still be visible to privileged local users. Prefer a secrets manager in deployed environments.
- This educational client is not a hardened mail-transfer service. A 250 response confirms submission acceptance, not inbox delivery.
