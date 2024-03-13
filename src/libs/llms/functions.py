import openai
from kedro.config import OmegaConfigLoader  # noqa: E402


def obtain_text(text_params: dict[str], content: str) -> str:
    """_summary_

    Args:
        text_params (dict[str]): _description_

    Returns:
        str: _description_
    """
    # Load the OpenAI credentials.
    conf_loader = OmegaConfigLoader(conf_source="./conf")
    openai_params = conf_loader["credentials"]["openai_settings"]

    # Extract the OpenAI credentials.
    openai_base_url = openai_params["openai_base_url"]
    openai_api_key = openai_params["openai_api_key"]

    # Initialize a client
    client = openai.OpenAI(api_key=openai_api_key, base_url=openai_base_url)

    # Create a chat completion
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Please write a motivational quote for me. It should not exceed 100 characters.",
            }
        ],
        model="gpt-3.5-turbo",
    )

    return chat_completion.choices[0].message.content
