import re
import subprocess
from pathlib import Path


class ReportGeneratorService:
    def __init__(self, output_dir: str = "reports") -> None:
        self._output_dir = Path(output_dir)
        self._output_dir.mkdir(exist_ok=True)

    def _validate_filename(self, filename: str) -> str:
        if not re.match(r"^[a-zA-Z0-9_-]+$", filename):
            raise ValueError("Invalid filename: only alphanumeric, dash, underscore allowed")
        return filename

    def generate_pdf(self, filename: str) -> str:
        safe_name = self._validate_filename(filename)
        output_path = self._output_dir / f"{safe_name}.pdf"

        content = f"Reporte de emisiones para {safe_name}"
        cmd = ["ps2pdf", "-", str(output_path)]
        result = subprocess.run(cmd, input=content, capture_output=True, text=True)

        if result.returncode != 0:
            raise RuntimeError(f"PDF generation failed: {result.stderr}")

        return str(output_path)