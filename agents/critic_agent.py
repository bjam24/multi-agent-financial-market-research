import re
from typing import Any

FORBIDDEN_TERMS = {
    "buy",
    "sell",
    "hold",
    "strong buy",
    "price target",
}


def check_forbidden_terms(report: str) -> list[str]:
    """
    Flag potentially advisory language for compliance review.
    """

    issues: list[str] = []
    report_lower = report.lower()

    for term in FORBIDDEN_TERMS:
        pattern = rf"\b{re.escape(term)}\b"

        if re.search(pattern, report_lower):
            issues.append(
                f"Report contains potentially advisory language: '{term}'"
            )

    return issues


def critic_agent(report: str) -> dict[str, Any]:
    """
    Validate generated report against basic quality and compliance rules.
    """

    report_lower = report.lower()

    issues: list[str] = []

    issues.extend(check_forbidden_terms(report))

    if "financial advice" not in report_lower:
        issues.append("Missing financial advice disclaimer")

    if "risk" not in report_lower:
        issues.append("Missing risk section")

    if "confidence" not in report_lower:
        issues.append("Missing confidence score section")

    if len(report.strip()) < 500:
        issues.append("Report may be too short for a complete analysis")

    return {
        "agent": "critic_agent",
        "status": "passed" if not issues else "needs_review",
        "issues": issues,
        "metadata": {
            "method": "rule_based_compliance_validation",
            "checks": [
                "advisory_language",
                "disclaimer",
                "risk_section",
                "confidence_section",
                "report_length",
            ],
        },
    }