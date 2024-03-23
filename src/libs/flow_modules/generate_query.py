"""BaseModel instances which provide the attributes and methods desired."""

from langchain_core.pydantic_v1 import BaseModel, Field, validator


class Quote(BaseModel):
    quote: str = Field(description="quote to be displayed.")
    author: str = Field(
        description="first name and surname of the person who said the quote."
    )
