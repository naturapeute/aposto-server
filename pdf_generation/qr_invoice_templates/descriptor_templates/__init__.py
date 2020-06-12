from pathlib import Path
from typing import List

from pdf_generation.content import Text
from pdf_generation.template import DescriptorTemplate

descriptor_templates: List[List[Text]] = [
    DescriptorTemplate(
        Path(
            "pdf_generation/qr_invoice_templates/descriptor_templates/author_template.json"
        )
    ).load_template(),
    DescriptorTemplate(
        Path(
            "pdf_generation/qr_invoice_templates/descriptor_templates/header_template.json"
        )
    ).load_template(),
    DescriptorTemplate(
        Path(
            "pdf_generation/qr_invoice_templates/descriptor_templates/invoice_template.json"
        )
    ).load_template(),
    DescriptorTemplate(
        Path(
            "pdf_generation/qr_invoice_templates/descriptor_templates/patient_template.json"
        )
    ).load_template(),
    DescriptorTemplate(
        Path(
            "pdf_generation/qr_invoice_templates/descriptor_templates/payment_section_template.json"
        )
    ).load_template(),
    DescriptorTemplate(
        Path(
            "pdf_generation/qr_invoice_templates/descriptor_templates/receipt_template.json"
        )
    ).load_template(),
]
