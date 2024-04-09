"""BaseModel instances which provide the attributes and methods desired."""

from langchain_core.pydantic_v1 import BaseModel, Field


class Quote(BaseModel):
    """Quote Class."""

    text: str = Field(description="quote to be displayed.")


class Hashtag(BaseModel):
    """Hashtag Class."""

    hashtag: list[str] = Field(description="list of hashtags to be used in the post.")


class Fact(BaseModel):
    """Fact Class."""

    text: str = Field(description="fact to be displayed.")
