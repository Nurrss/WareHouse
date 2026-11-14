import json
from dataclasses import asdict, Field
from typing import Any, ClassVar

class JsonMixin:
    __dataclass_fields__: ClassVar[dict[str, Field[Any]]] 
    
    def to_json(self) -> str:
        return json.dumps(asdict(self), default=str, ensure_ascii=False)