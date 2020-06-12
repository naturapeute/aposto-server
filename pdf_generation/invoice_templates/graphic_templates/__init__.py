from pathlib import Path
from typing import List

from pdf_generation.content import Graphic
from pdf_generation.template import GraphicTemplate

graphic_templates: List[List[Graphic]] = [
    GraphicTemplate(
        Path(
            "pdf_generation/invoice_templates/graphic_templates/datamatrix_template.json"
        )
    ).load_template(),
    GraphicTemplate(
        Path("pdf_generation/invoice_templates/graphic_templates/frame_template.json")
    ).load_template(),
]
