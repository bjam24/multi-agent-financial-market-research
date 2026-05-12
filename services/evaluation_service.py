from typing import Any


def evaluate_report(
    report: str,
    critique: dict[str, Any],
) -> dict[str, Any]:
    """
    Evaluate generated report quality.
    """

    score = 100
    issues = []

    if len(report) < 500:
        score -= 15
        issues.append("Report is too short")

    required_sections = [
        "Market Summary",
        "Sentiment Analysis",
        "Risk Analysis",
        "Disclaimer",
    ]

    for section in required_sections:

        if section not in report:
            score -= 10
            issues.append(
                f"Missing section: {section}"
            )

    critique_issues = critique.get(
        "issues",
        [],
    )

    score -= len(critique_issues) * 5

    if score < 0:
        score = 0

    return {
        "score": score,
        "passed": score >= 70,
        "issues": issues,
        "critic_issues": critique_issues,
    }