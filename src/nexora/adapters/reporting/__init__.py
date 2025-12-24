"""
Reporting adapters for generating various types of reports and outputs.
"""

from pathlib import Path
from typing import Any
from uuid import uuid4

from nexora.application.ports import ReportingPort
from nexora.core.exceptions import ReportingException
from nexora.core.logger import get_logger
from nexora.domain.entities import Report

logger = get_logger(__name__)


class MarkdownReportingAdapter(ReportingPort):
    """
    Reporting adapter for generating Markdown formatted reports.

    Produces clean, readable Markdown documents with sections and formatting.
    """

    def __init__(self) -> None:
        """Initialize the Markdown reporting adapter."""
        logger.info("MarkdownReportingAdapter initialized")

    def generate_report(
        self,
        title: str,
        content: dict[str, Any],
        report_type: str,
        output_format: str = "markdown",
    ) -> Report:
        """
        Generate a Markdown formatted report.

        Args:
            title: Report title
            content: Content to include in report
            report_type: Type of report
            output_format: Output format (should be 'markdown')

        Returns:
            Generated report

        Raises:
            ReportingException: If report generation fails
        """
        try:
            # Build Markdown content
            markdown_content = self._build_markdown(title, content)

            report = Report(
                report_id=uuid4(),
                title=title,
                report_type=report_type,
                content=markdown_content,
                format="markdown",
            )

            report.metadata = {
                "content_sections": len(content),
                "character_count": len(markdown_content),
            }

            logger.info(f"Generated Markdown report: {title}")
            return report

        except Exception as e:
            raise ReportingException(
                f"Failed to generate Markdown report: {title}",
                details={"title": title, "report_type": report_type},
                original_exception=e,
            )

    def export_report(self, report: Report, output_path: str) -> str:
        """
        Export a report to a Markdown file.

        Args:
            report: Report to export
            output_path: Path to export to

        Returns:
            Path to exported report

        Raises:
            ReportingException: If export fails
        """
        try:
            path = Path(output_path)
            path.parent.mkdir(parents=True, exist_ok=True)

            with open(path, "w", encoding="utf-8") as f:
                f.write(report.content)

            logger.info(f"Exported report to {output_path}")
            return str(path.absolute())

        except Exception as e:
            raise ReportingException(
                f"Failed to export report to {output_path}",
                details={"report_id": str(report.report_id), "output_path": output_path},
                original_exception=e,
            )

    def _build_markdown(self, title: str, content: dict[str, Any]) -> str:
        """Build Markdown formatted content."""
        lines = [
            f"# {title}",
            "",
            f"**Report ID:** {uuid4()}",
            "",
        ]

        for section, data in content.items():
            lines.append(f"## {section.replace('_', ' ').title()}")
            lines.append("")

            if isinstance(data, dict):
                for key, value in data.items():
                    lines.append(f"- **{key}:** {value}")
            elif isinstance(data, list):
                for item in data:
                    lines.append(f"- {item}")
            else:
                lines.append(str(data))

            lines.append("")

        return "\n".join(lines)


class HTMLReportingAdapter(ReportingPort):
    """
    Reporting adapter for generating HTML formatted reports.

    Produces styled HTML documents suitable for web viewing.
    """

    def __init__(self, template: str = "default") -> None:
        """
        Initialize the HTML reporting adapter.

        Args:
            template: HTML template to use
        """
        self.template = template
        logger.info(f"HTMLReportingAdapter initialized with template={template}")

    def generate_report(
        self,
        title: str,
        content: dict[str, Any],
        report_type: str,
        output_format: str = "html",
    ) -> Report:
        """
        Generate an HTML formatted report.

        Args:
            title: Report title
            content: Content to include in report
            report_type: Type of report
            output_format: Output format (should be 'html')

        Returns:
            Generated report

        Raises:
            ReportingException: If report generation fails
        """
        try:
            # Build HTML content
            html_content = self._build_html(title, content)

            report = Report(
                report_id=uuid4(),
                title=title,
                report_type=report_type,
                content=html_content,
                format="html",
            )

            report.metadata = {
                "template": self.template,
                "content_sections": len(content),
            }

            logger.info(f"Generated HTML report: {title}")
            return report

        except Exception as e:
            raise ReportingException(
                f"Failed to generate HTML report: {title}",
                details={"title": title, "report_type": report_type},
                original_exception=e,
            )

    def export_report(self, report: Report, output_path: str) -> str:
        """
        Export a report to an HTML file.

        Args:
            report: Report to export
            output_path: Path to export to

        Returns:
            Path to exported report

        Raises:
            ReportingException: If export fails
        """
        try:
            path = Path(output_path)
            path.parent.mkdir(parents=True, exist_ok=True)

            with open(path, "w", encoding="utf-8") as f:
                f.write(report.content)

            logger.info(f"Exported HTML report to {output_path}")
            return str(path.absolute())

        except Exception as e:
            raise ReportingException(
                f"Failed to export report to {output_path}",
                details={"report_id": str(report.report_id), "output_path": output_path},
                original_exception=e,
            )

    def _build_html(self, title: str, content: dict[str, Any]) -> str:
        """Build HTML formatted content."""
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #333; }}
        h2 {{ color: #666; margin-top: 30px; }}
        .section {{ margin-bottom: 20px; }}
        .key {{ font-weight: bold; }}
        ul {{ list-style-type: none; padding-left: 0; }}
        li {{ margin: 5px 0; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
"""

        for section, data in content.items():
            html += f'    <div class="section">\n'
            html += f'        <h2>{section.replace("_", " ").title()}</h2>\n'

            if isinstance(data, dict):
                html += '        <ul>\n'
                for key, value in data.items():
                    html += f'            <li><span class="key">{key}:</span> {value}</li>\n'
                html += '        </ul>\n'
            elif isinstance(data, list):
                html += '        <ul>\n'
                for item in data:
                    html += f'            <li>{item}</li>\n'
                html += '        </ul>\n'
            else:
                html += f'        <p>{data}</p>\n'

            html += '    </div>\n'

        html += """</body>
</html>"""

        return html


class JSONReportingAdapter(ReportingPort):
    """
    Reporting adapter for generating JSON formatted reports.

    Produces structured JSON documents for programmatic consumption.
    """

    def __init__(self, indent: int = 2) -> None:
        """
        Initialize the JSON reporting adapter.

        Args:
            indent: Indentation level for JSON formatting
        """
        self.indent = indent
        logger.info(f"JSONReportingAdapter initialized with indent={indent}")

    def generate_report(
        self,
        title: str,
        content: dict[str, Any],
        report_type: str,
        output_format: str = "json",
    ) -> Report:
        """
        Generate a JSON formatted report.

        Args:
            title: Report title
            content: Content to include in report
            report_type: Type of report
            output_format: Output format (should be 'json')

        Returns:
            Generated report

        Raises:
            ReportingException: If report generation fails
        """
        try:
            import json

            # Build JSON structure
            report_data = {
                "title": title,
                "report_type": report_type,
                "content": content,
            }

            json_content = json.dumps(report_data, indent=self.indent)

            report = Report(
                report_id=uuid4(),
                title=title,
                report_type=report_type,
                content=json_content,
                format="json",
            )

            logger.info(f"Generated JSON report: {title}")
            return report

        except Exception as e:
            raise ReportingException(
                f"Failed to generate JSON report: {title}",
                details={"title": title, "report_type": report_type},
                original_exception=e,
            )

    def export_report(self, report: Report, output_path: str) -> str:
        """
        Export a report to a JSON file.

        Args:
            report: Report to export
            output_path: Path to export to

        Returns:
            Path to exported report

        Raises:
            ReportingException: If export fails
        """
        try:
            path = Path(output_path)
            path.parent.mkdir(parents=True, exist_ok=True)

            with open(path, "w", encoding="utf-8") as f:
                f.write(report.content)

            logger.info(f"Exported JSON report to {output_path}")
            return str(path.absolute())

        except Exception as e:
            raise ReportingException(
                f"Failed to export report to {output_path}",
                details={"report_id": str(report.report_id), "output_path": output_path},
                original_exception=e,
            )
