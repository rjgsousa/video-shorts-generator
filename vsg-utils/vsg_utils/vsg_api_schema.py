
from pydantic import BaseModel, Field


class ThemesRequest(BaseModel):
    content: str = Field(
        ...,
        description="Text email for prediction",
    )
