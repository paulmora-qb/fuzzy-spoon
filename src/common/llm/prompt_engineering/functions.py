"""Functions for the llm callback pipeline."""

import os

from common.llm.flow_modules.generate_query import Fact, Hashtag, Quote
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.prompts.chat import (
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from langchain_openai import ChatOpenAI

PYDANTIC_OUTPUT_PARSER = {
    "quote": Quote,
    "hashtag": Hashtag,
    "fact": Fact,
}


def prompt_wrapper(
    system_message: str,
    instruction_message: str,
    output_parser_key: str,
) -> str:
    """Building the prompt through instruction and system messages.

    Args:
        system_message (str): System message which states how the AI should behave.
        instruction_message (str): Instruction message which states what the AI should
            do.
        output_parser_key (str): Name of the pipeline. Used to find the correct output
            parser object.

    Returns:
        str: The output of the pipeline. This oftentimes is a class which has different
            attributes.
    """
    prompt = _build_prompt(
        instruction_message=instruction_message, system_message=system_message
    )

    llm = _get_openai_endpoint()
    llm = GPT4All(model="libs/nous-hermes-llama2-13b.Q4_0.gguf")
    output_parser = PydanticOutputParser(
        pydantic_object=PYDANTIC_OUTPUT_PARSER[output_parser_key]
    )

    chain = prompt | llm | output_parser
    return chain.invoke(
        {"format_instructions": output_parser.get_format_instructions()}
    )


def _get_openai_endpoint(
    model_name: str = "gpt-3.5-turbo", temperature: float = 0.0
) -> ChatOpenAI:
    """Initializing the OpenAI endpoint.

    Args:
        model_name (str, optional): Name of the instance of the openai model name.
            Defaults to "gpt-3.5-turbo".
        temperature (float, optional): The temperature states the certainty that the AI
            has. Defaults to 0.0.

    Returns:
        ChatOpenAI: OpenAI endpoint.
    """
    openai_api_key = os.environ.get("OPENAI_API")
    openai_base_url = os.environ.get("OPENAI_API_BASE_URL")

    return ChatOpenAI(
        temperature=temperature,
        model_name=model_name,
        openai_api_key=openai_api_key,
        openai_api_base=openai_base_url,
        request_timeout=15,
        max_retries=2,
    )


def _build_prompt(instruction_message: str, system_message: str) -> ChatPromptTemplate:
    """Building the prompt through instruction and system messages.

    Args:
        instruction_message (str): Instruction message which states what the AI should
            do.
        system_message (str): System message which states how the AI should behave.

    Returns:
        ChatPromptTemplate: The prompt that is built.
    """
    instruction_message = HumanMessagePromptTemplate.from_template(instruction_message)
    system_message = SystemMessagePromptTemplate.from_template(system_message)
    return ChatPromptTemplate.from_messages([system_message, instruction_message])
