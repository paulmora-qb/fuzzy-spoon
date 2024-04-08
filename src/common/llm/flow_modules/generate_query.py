"""BaseModel instances which provide the attributes and methods desired."""

from langchain_core.pydantic_v1 import BaseModel, Field


class Quote(BaseModel):
    text: str = Field(description="quote to be displayed.")


class Hashtag(BaseModel):
    hashtag: list[str] = Field(description="list of hashtags to be used in the post.")


class Fact(BaseModel):
    text: str = Field(description="fact to be displayed.")
