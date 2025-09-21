from typing import Mapping

from pydantic import BaseModel


class RenderSpecDTO(BaseModel):
    """Data Transfer Object to render a specification"""

    spec: dict


RenderSpecReturn = Mapping
