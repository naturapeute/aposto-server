from pathlib import Path
from typing import List

from pdf_generation.content import Graphic, SwissQRCode
from pdf_generation.template import GraphicTemplate, SwissQRCodeTemplate

frame_template: List[Graphic] = GraphicTemplate(
    Path(
        "pdf_generation/qr_invoice_templates/graphic_templates/invoice_frame_template.json"
    )
).load_template()

qr_part_frame_template: List[Graphic] = GraphicTemplate(
    Path(
        "pdf_generation/qr_invoice_templates/graphic_templates/qr_invoice_frame_template.json"
    )
).load_template()

scissors_template: List[Graphic] = GraphicTemplate(
    Path("pdf_generation/qr_invoice_templates/graphic_templates/scissors_template.json")
).load_template()


swiss_qr_code_template: List[SwissQRCode] = SwissQRCodeTemplate(
    Path(
        "pdf_generation/qr_invoice_templates/graphic_templates/swiss_qr_code_template.json"
    )
).load_template()
