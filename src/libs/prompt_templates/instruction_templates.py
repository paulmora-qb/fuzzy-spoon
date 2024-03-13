from enum import Enum

from langchain.prompts.chat import HumanMessagePromptTemplate


class InstructionMessages(Enum):
    """Collection of templates for the instruction prompt."""

    quote_message = HumanMessagePromptTemplate.from_template(
        """
        Write a famous quote from a well-known person. This quote can be motivational, inspirational, or thought-provoking.
        The quote should be less than 100 characters. The main goal is to inspire and motivate the reader.

        topic: {topic}
        """
    )

    hashtag_message = HumanMessagePromptTemplate.from_template(
        """
        Suggest a hashtag for the quote.

        quote: {quote}
        """
    )
