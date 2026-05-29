"""Offline sample data helper.

The project currently keeps curated sample inputs under `data/input/`.
This script is intentionally non-destructive: it does not overwrite sample files
or call external services. Use the main pipeline to regenerate outputs.
"""


def main() -> None:
    print("Sample source files are maintained in data/input/.")
    print("Run `PYTHONPATH=src python3 -m compliance_security_dashboard.main`.")


if __name__ == "__main__":
    main()
