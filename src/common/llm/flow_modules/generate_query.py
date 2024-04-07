"""BaseModel instances which provide the attributes and methods desired."""

from langchain_core.pydantic_v1 import BaseModel, Field


class Quote(BaseModel):
    quote: str = Field(description="quote to be displayed.")
    author: str = Field(
        description="first name and surname of the person who said the quote."
    )


class Hashtag(BaseModel):
    hashtag: list[str] = Field(description="list of hashtags to be used in the post.")


class Fact(BaseModel):
    fact: str = Field(description="fact to be displayed.")
