# Contributing

Use Python 3.10 or newer. Install development dependencies with python -m pip install -e '.[dev]'. Before submitting a pull request, run pytest, ruff check ., and ruff format --check ..

Protocol changes should include tests that do not contact real mail servers or send messages to real recipients. Never commit credentials, application passwords, access tokens, or recipient data. Avoid logging authentication material or message bodies.
