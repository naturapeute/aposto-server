from pathlib import Path
from typing import List

from pdf_generation.content import Value
from pdf_generation.template import ValueTemplate

value_templates: List[List[Value]] = [
    ValueTemplate(
        Path("pdf_generation/invoice_templates/value_templates/author_template.json")
    ).load_template(),
    ValueTemplate(
        Path("pdf_generation/invoice_templates/value_templates/footer_template.json")
    ).load_template(),
    ValueTemplate(
        Path(
            "pdf_generation/invoice_templates/value_templates/other_fields_template.json"
        )
    ).load_template(),
    ValueTemplate(
        Path("pdf_generation/invoice_templates/value_templates/patient_template.json")
    ).load_template(),
]

services_template: List[Value] = ValueTemplate(
    Path("pdf_generation/invoice_templates/value_templates/services_template.json")
).load_template()
