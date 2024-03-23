"""Functions for the llm callback pipeline."""

from kedro.config import OmegaConfigLoader
from langchain.prompts.chat import (
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)
from typing import Any
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
import importlib


def prompt_wrapper(
    system_message: SystemMessagePromptTemplate = "",
    instruction_message: HumanMessagePromptTemplate = "",
    pydantic_object_path="",
) -> str:

    prompt = _build_prompt(
        instruction_message=instruction_message, system_message=system_message
    )
    llm = _get_openai_endpoint()
    output_parser = _build_output_parser(pydantic_object_path=pydantic_object_path)

    chain = prompt | llm | output_parser
    return chain.invoke(
        {"format_instructions": output_parser.get_format_instructions()}
    )


def _get_openai_endpoint(
    model_name: str = "gpt-3.5-turbo", temperature: float = 0.0
) -> ChatOpenAI:
    # Load the OpenAI credentials.
    conf_loader = OmegaConfigLoader(conf_source="./conf")
    openai_params = conf_loader["credentials"]["openai_settings"]

    # Extract the OpenAI credentials.
    openai_api_base = openai_params["openai_base_url"]
    openai_api_key = openai_params["openai_api_key"]

    return ChatOpenAI(
        temperature=temperature,
        model_name=model_name,
        openai_api_key=openai_api_key,
        openai_api_base=openai_api_base,
        request_timeout=15,
        max_retries=2,
    )


def _build_output_parser(pydantic_object_path: str):

    pydantic_object = _load_obj(pydantic_object_path)
    return PydanticOutputParser(pydantic_object=pydantic_object)


def _load_obj(path: str) -> Any:
    # Split the string into module name and class name
    module_name, class_name = path.rsplit(".", 1)

    # Import the module dynamically
    module = importlib.import_module(module_name)

    # Get the class from the module
    return getattr(module, class_name)


def _build_prompt(instruction_message, system_message):
    """_summary_

    Args:
        instruction_message (str): _description_
        system_message (str): _description_

    Returns:
        str: _description_
    """
    instruction_message = HumanMessagePromptTemplate.from_template(instruction_message)
    system_message = SystemMessagePromptTemplate.from_template(system_message)
    return ChatPromptTemplate.from_messages([system_message, instruction_message])
