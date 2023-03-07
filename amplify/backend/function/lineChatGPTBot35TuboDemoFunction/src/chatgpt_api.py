# import requests
import openai
import const

# OpenAI API endpoint for completions
# GPT3_COMPLETIONS_ENDPOINT = 'https://api.openai.com/v1/completions'

# Model name
GPT3_MODEL = 'gpt-3.5-turbo'

# API request headers
# HEADERS = {
#     'Content-Type': 'application/json',
#     'Authorization': f'Bearer {const.OPEN_AI_API_KEY}'
# }

# Maximum number of tokens to generate
# MAX_TOKENS = 1000

# Controls the randomness of the generated text
# TEMPERATURE = 0.5

# Number of completions to generate
# GENERATE_COMPLETIONS_COUNT = 1

# Specifies the token at which to stop generating completions
# STOP = None


def completions(prompt):
    try:
        openai.api_key = const.OPEN_AI_API_KEY
        response = openai.ChatCompletion.create(
            model=GPT3_MODEL,
            messages=[
                {"role": "system", "content": "敬語を使うのをやめてください。友達のようにタメ口で話してください。また、絵文字をたくさん使って話してください。"},
                {"role": "user", "content": f"{prompt}"}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        # Raise the exception
        raise e

# def completions(prompt):
#     """
#     Sends a completion request to the OpenAI API for the given prompt and returns the generated text.

#     :param prompt: The prompt for which completions are generated
#     :return: The generated text
#     """
#     completions_data = {
#         'prompt': prompt,
#         'model': GPT3_MODEL,
#         'max_tokens': MAX_TOKENS,
#         'n': GENERATE_COMPLETIONS_COUNT,
#         'stop': STOP,
#         'temperature': TEMPERATURE
#     }

#     try:
#         response = requests.post(GPT3_COMPLETIONS_ENDPOINT, headers=HEADERS, json=completions_data)
#         response_json = response.json()
#         # Return the generated text
#         return response_json['choices'][0]['text']
#     except Exception as e:
#         # Raise the exception
#         raise e
