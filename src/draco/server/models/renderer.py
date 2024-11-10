from typing import Mapping

from pydantic import BaseModel


class RenderSpecDTO(BaseModel):  # pytype: disable=base-class-error
    """Data Transfer Object to render a specification"""

    spec: dict


RenderSpecReturn = Mapping
