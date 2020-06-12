from pathlib import Path
from typing import List

from pdf_generation.content import Text
from pdf_generation.template import DescriptorTemplate

descriptor_templates: List[List[Text]] = [
    DescriptorTemplate(
        Path("pdf_generation/invoice_templates/descriptor_templates/author_template.json")
    ).load_template(),
    DescriptorTemplate(
        Path("pdf_generation/invoice_templates/descriptor_templates/footer_template.json")
    ).load_template(),
    DescriptorTemplate(
        Path("pdf_generation/invoice_templates/descriptor_templates/header_template.json")
    ).load_template(),
    DescriptorTemplate(
        Path(
            "pdf_generation/invoice_templates/descriptor_templates/other_fields_template.json"
        )
    ).load_template(),
    DescriptorTemplate(
        Path(
            "pdf_generation/invoice_templates/descriptor_templates/patient_template.json"
        )
    ).load_template(),
    DescriptorTemplate(
        Path(
            "pdf_generation/invoice_templates/descriptor_templates/services_template.json"
        )
    ).load_template(),
]
