from typing import Any

FORBIDDEN_TERMS = {"buy", "sell", "hold", "strong buy", "price target"}


def check_forbidden_terms(report: str) -> list[str]:
    """
    Validate report content against basic compliance rules
    """
    issues = []
    report_lower = report.lower()

    for term in FORBIDDEN_TERMS:
        if term in report_lower:
            issues.append(
                f"Report contains advisory language: '{term}'"
            )

    return issues


def critic_agent(report: str) -> dict[str, Any]:
    """
    Validate generated report against basic compliance and quality rules.
    """

    issues = []
    issues.extend(check_forbidden_terms(report))
    report_lower = report.lower()

    if "financial advice" not in report_lower:
        issues.append("Missing financial disclaimer")

    if "risk" not in report_lower:
        issues.append("Missing risk section")

    return {
        "agent": "critic_agent",
        "status": "passed" if not issues else "needs_review",
        "issues": issues,
    }