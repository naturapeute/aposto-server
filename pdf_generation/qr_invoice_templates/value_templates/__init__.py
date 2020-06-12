from pathlib import Path
from typing import List

from pdf_generation.content import Value
from pdf_generation.template import ValueTemplate

value_templates: List[List[Value]] = [
    ValueTemplate(
        Path("pdf_generation/qr_invoice_templates/value_templates/author_template.json")
    ).load_template(),
    ValueTemplate(
        Path("pdf_generation/qr_invoice_templates/value_templates/invoice_template.json")
    ).load_template(),
    ValueTemplate(
        Path("pdf_generation/qr_invoice_templates/value_templates/patient_template.json")
    ).load_template(),
    ValueTemplate(
        Path(
            "pdf_generation/qr_invoice_templates/value_templates/payment_section_template.json"
        )
    ).load_template(),
    ValueTemplate(
        Path("pdf_generation/qr_invoice_templates/value_templates/receipt_template.json")
    ).load_template(),
]
