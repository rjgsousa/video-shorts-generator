
from pydantic import BaseModel, Field


class ThemesRequest(BaseModel):
    content: str = Field(
        ...,
        description="Content for Themes prediction",
    )
