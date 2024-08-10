import dotenv
from litellm import embedding
import os
from aijson import register_action

# dotenv.load_dotenv(".env")

@register_action
def embed(text: str | list[str], model: str='amazon.titan-embed-text-v2:0') -> list[float] | None:
    """
    embed a string or strings
    """
    os.environ["AWS_REGION"] = os.environ["AWS_DEFAULT_REGION"]
    res = embedding(
        model=model,
        input=text,
    )
    if res.data is not None:
        return res.data[0]["embedding"]
    else:
        return None
    

# embed_list = embed("amazon.titan-embed-text-v2:0", "hello")

# if embed_list is not None:
#     print(embed_list)
#     print(len(embed_list))