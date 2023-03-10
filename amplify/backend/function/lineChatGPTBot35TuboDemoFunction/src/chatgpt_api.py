# import asyncio
import openai
import const
import logging

logger = logging.getLogger()

# Model name
GPT3_MODEL = 'gpt-3.5-turbo'

# Maximum number of tokens to generate
MAX_TOKENS = 1024


# async def completions(chat_histories):
def completions(chat_histories):
    # Create a new dict list of a system
    system_prompts = [{'role': 'system', 'content': '敬語を使うのをやめてください。友達のようにタメ口で話してください。また、絵文字をたくさん使って話してください。'}]
    # Create a new dict list of a prompt
    history_prompts = list(map(lambda history: {"role": history["role"], "content": history["content"]}, chat_histories))
    messages = system_prompts + history_prompts
    logger.info(f"prompts:{messages}")
    try:
        openai.api_key = const.OPEN_AI_API_KEY
        # response = await openai.ChatCompletion.create(
        response = openai.ChatCompletion.create(
            model=GPT3_MODEL,
            messages=messages,
            max_tokens=MAX_TOKENS
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        # Raise the exception
        raise e
