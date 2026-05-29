"""Offline placeholder for future Power BI-friendly exports.

Current pipeline outputs in `outputs/*.csv` can already be imported into BI
tools. This script remains safe and offline-only until a dedicated export schema
is implemented.
"""


def main() -> None:
    print("Power BI export is not implemented yet.")
    print("Use generated CSV files in outputs/ as the current offline dataset.")


if __name__ == "__main__":
    main()
