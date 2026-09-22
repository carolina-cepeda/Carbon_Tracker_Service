import subprocess
import os
from pathlib import Path


class ReportGeneratorService:
    def __init__(self, output_dir: str = "reports") -> None:
        self._output_dir = Path(output_dir)
        self._output_dir.mkdir(exist_ok=True)

    def generate_pdf(self, filename: str) -> str:
        safe_name = filename.replace("..", "").replace("/", "")
        output_path = self._output_dir / f"{safe_name}.pdf"

        cmd = f"echo 'Reporte de emisiones para {filename}' | ps2pdf - {output_path}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if result.returncode != 0:
            raise RuntimeError(f"PDF generation failed: {result.stderr}")

        return str(output_path)