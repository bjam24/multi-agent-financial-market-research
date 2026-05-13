import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPORTS_DIR = Path("storage/reports")


def save_report(
    ticker: str,
    workflow_result: dict[str, Any],
) -> dict[str, Any]:
    """
    Persist generated research report as JSON and Markdown files.
    """

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    normalized_ticker = ticker.upper()

    base_filename = f"{normalized_ticker}_{timestamp}"

    json_path = REPORTS_DIR / f"{base_filename}.json"
    markdown_path = REPORTS_DIR / f"{base_filename}.md"

    payload = {
        "ticker": normalized_ticker,
        "created_at": timestamp,
        "result": workflow_result,
    }

    with json_path.open("w", encoding="utf-8") as file:
        json.dump(
            payload,
            file,
            indent=2,
            ensure_ascii=False,
        )

    with markdown_path.open("w", encoding="utf-8") as file:
        file.write(
            workflow_result.get("report", "")
        )

    return {
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
    }


def list_reports() -> list[dict[str, Any]]:
    """
    Return saved markdown reports sorted by newest first.
    """

    REPORTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    reports = []

    for file in REPORTS_DIR.glob("*.md"):

        reports.append(
            {
                "filename": file.name,
                "path": str(file),
                "created_at": file.stat().st_mtime,
            }
        )

    return sorted(
        reports,
        key=lambda item: item["created_at"],
        reverse=True,
    )


def read_report(filename: str) -> dict[str, Any]:
    """
    Read a saved markdown report.
    """

    report_path = REPORTS_DIR / filename

    if not report_path.exists():

        raise FileNotFoundError(
            f"Report not found: {filename}"
        )

    return {
        "filename": filename,
        "content": report_path.read_text(
            encoding="utf-8"
        ),
    }