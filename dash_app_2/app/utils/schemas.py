from pydantic import BaseModel
from typing import Optional


class Filter(BaseModel):
    options: list[str]
    selected: list[str]
    mappings: Optional[dict[str, str]]

    def map_filter_value(self, value: str) -> str:
        if self.mappings is None:
            raise ValueError("No mapping available for this filter")
        
        mapped_value = self.mappings.get(value)

        if mapped_value is None:
            raise ValueError(f"Key '{value}' not found in mapping table")
        
        return mapped_value