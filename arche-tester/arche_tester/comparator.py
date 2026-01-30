"""Comparator for version degradation analysis.

Compares test results against baseline.
"""

from datetime import datetime
from pathlib import Path

import yaml
from rich.console import Console
from rich.table import Table

from arche_tester.models import (
    Conformity,
    Degradation,
    VersionAnalysis,
    VersionComparison,
)

console = Console()


class VersionComparator:
    """Compares versions against baseline for degradation."""

    def __init__(self, data_path: Path) -> None:
        """Initialize comparator.

        Args:
            data_path: Path to data directory.
        """
        self._data_path = data_path

    def load_analysis(self, version: str) -> VersionAnalysis:
        """Load analysis for a version."""
        analysis_file = (
            self._data_path / "versions" / version / "analysis.yaml"
        )
        content = analysis_file.read_text()
        data = yaml.safe_load(content)
        return VersionAnalysis.model_validate(data)

    def compare(
        self,
        baseline_version: str,
        current_version: str,
    ) -> VersionComparison:
        """Compare current version against baseline.

        Args:
            baseline_version: Baseline version (e.g., "0.1.0").
            current_version: Current version (e.g., "0.2.0").

        Returns:
            Comparison with degradation analysis.
        """
        baseline = self.load_analysis(baseline_version)
        current = self.load_analysis(current_version)

        # Create lookup for baseline results
        baseline_lookup: dict[str, Conformity] = {
            analysis.test_id: analysis.conformity
            for analysis in baseline.analyses
        }

        degradations: list[Degradation] = []
        degradation_count = 0

        for analysis in current.analyses:
            baseline_conformity = baseline_lookup.get(
                analysis.test_id,
                Conformity.PASS,
            )
            current_conformity = analysis.conformity

            # Check for degradation (was better, now worse)
            degraded = self._is_degraded(
                baseline=baseline_conformity,
                current=current_conformity,
            )

            if degraded:
                degradation_count += 1

            degradations.append(
                Degradation(
                    test_id=analysis.test_id,
                    baseline_conformity=baseline_conformity,
                    current_conformity=current_conformity,
                    degraded=degraded,
                )
            )

        # Calculate degradation percentage
        degradation_pct = current.pass_rate - baseline.pass_rate

        # Generate summary
        if degradation_pct >= 0:
            summary = f"No degradation. Pass rate {'improved' if degradation_pct > 0 else 'stable'}."
        elif degradation_pct > -5:
            summary = f"Minor degradation ({degradation_pct:.1f}%). Acceptable."
        elif degradation_pct > -10:
            summary = f"Moderate degradation ({degradation_pct:.1f}%). Review changes."
        else:
            summary = f"Significant degradation ({degradation_pct:.1f}%). Consider reverting."

        result = VersionComparison(
            baseline_version=baseline_version,
            current_version=current_version,
            timestamp=datetime.now().isoformat(),
            baseline_pass_rate=baseline.pass_rate,
            current_pass_rate=current.pass_rate,
            degradation_pct=degradation_pct,
            degradations=degradations,
            summary=summary,
        )

        # Save comparison
        self._save_comparison(
            baseline_version=baseline_version,
            current_version=current_version,
            comparison=result,
        )

        # Print summary
        self._print_summary(result)

        return result

    def _is_degraded(
        self,
        baseline: Conformity,
        current: Conformity,
    ) -> bool:
        """Check if current is worse than baseline."""
        conformity_order = {
            Conformity.PASS: 2,
            Conformity.PARTIAL: 1,
            Conformity.FAIL: 0,
        }
        return conformity_order[current] < conformity_order[baseline]

    def _save_comparison(
        self,
        baseline_version: str,
        current_version: str,
        comparison: VersionComparison,
    ) -> None:
        """Save comparison to YAML file."""
        comparison_dir = (
            self._data_path
            / "comparisons"
            / f"{baseline_version}-{current_version}"
        )
        comparison_dir.mkdir(parents=True, exist_ok=True)

        output_file = comparison_dir / "degradation.yaml"
        data = comparison.model_dump(mode="json")

        with output_file.open("w") as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

        console.print(f"[green]Comparison saved: {output_file}[/green]")

    def _print_summary(self, comparison: VersionComparison) -> None:
        """Print comparison summary table."""
        table = Table(
            title=f"Comparison: v{comparison.baseline_version} → v{comparison.current_version}"
        )

        table.add_column("Metric", style="cyan")
        table.add_column("Baseline", justify="right")
        table.add_column("Current", justify="right")
        table.add_column("Δ", justify="right")

        # Pass rate row
        delta = comparison.degradation_pct
        delta_style = "green" if delta >= 0 else "red"
        delta_str = f"[{delta_style}]{delta:+.1f}%[/{delta_style}]"

        table.add_row(
            "Pass Rate",
            f"{comparison.baseline_pass_rate:.1f}%",
            f"{comparison.current_pass_rate:.1f}%",
            delta_str,
        )

        # Degradations count
        degraded_count = sum(1 for d in comparison.degradations if d.degraded)
        table.add_row(
            "Degraded Tests",
            "-",
            f"[red]{degraded_count}[/red]" if degraded_count > 0 else "0",
            "",
        )

        console.print(table)
        console.print(f"\n[bold]Summary:[/bold] {comparison.summary}")

    def generate_report(
        self,
        baseline_version: str,
        current_version: str,
        phase: int,
    ) -> Path:
        """Generate markdown report for a phase.

        Args:
            baseline_version: Baseline version.
            current_version: Phase version.
            phase: Phase number (1, 2, or 3).

        Returns:
            Path to generated report.
        """
        comparison = self.compare(
            baseline_version=baseline_version,
            current_version=current_version,
        )

        report_content = f"""# Phase {phase} Report

## Version Comparison

- **Baseline**: v{comparison.baseline_version}
- **Current**: v{comparison.current_version}
- **Timestamp**: {comparison.timestamp}

## Results

| Metric | Baseline | Current | Change |
|--------|----------|---------|--------|
| Pass Rate | {comparison.baseline_pass_rate:.1f}% | {comparison.current_pass_rate:.1f}% | {comparison.degradation_pct:+.1f}% |

## Summary

{comparison.summary}

## Degraded Tests

"""
        degraded_tests = [d for d in comparison.degradations if d.degraded]
        if degraded_tests:
            report_content += "| Test ID | Baseline | Current |\n"
            report_content += "|---------|----------|----------|\n"
            for d in degraded_tests:
                report_content += f"| {d.test_id} | {d.baseline_conformity.value} | {d.current_conformity.value} |\n"
        else:
            report_content += "No degraded tests.\n"

        report_content += """
## Recommendation

"""
        if comparison.degradation_pct >= 0:
            report_content += "✅ **Proceed** - No degradation detected.\n"
        elif comparison.degradation_pct > -5:
            report_content += "✅ **Proceed with caution** - Minor degradation acceptable.\n"
        elif comparison.degradation_pct > -10:
            report_content += "⚠️ **Review changes** - Moderate degradation detected.\n"
        else:
            report_content += "❌ **Consider reverting** - Significant degradation detected.\n"

        # Save report
        report_dir = self._data_path / "reports"
        report_dir.mkdir(parents=True, exist_ok=True)
        report_file = report_dir / f"phase-{phase}-report.md"
        report_file.write_text(report_content)

        console.print(f"[green]Report saved: {report_file}[/green]")

        return report_file


__all__ = ["VersionComparator"]
