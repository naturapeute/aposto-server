import json
from pathlib import Path
from typing import List

from pdf_generation.content import Content, Graphic, Text, Value


class Template:
    def __init__(self, path: Path):
        self.path: Path = path
        self.load_template()

    def load_template(self) -> List[Content]:
        with open(self.path.resolve().as_posix()) as json_template:
            return list(
                Content(dict_content) for dict_content in json.load(json_template)
            )


class DescriptorTemplate(Template):
    def load_template(self) -> List[Text]:
        with open(self.path.resolve().as_posix()) as json_template:
            return list(Text(dict_text) for dict_text in json.load(json_template))


class GraphicTemplate(Template):
    def load_template(self) -> List[Graphic]:
        with open(self.path.resolve().as_posix()) as json_template:
            return list(
                Graphic(dict_graphic) for dict_graphic in json.load(json_template)
            )


class ValueTemplate(Template):
    def load_template(self):
        with open(self.path.resolve().as_posix()) as json_template:
            return list(Value(dict_value) for dict_value in json.load(json_template))
