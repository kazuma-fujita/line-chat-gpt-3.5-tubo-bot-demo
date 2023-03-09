import json
from linebot import LineBotApi
from linebot.models import TextSendMessage
import const
import chatgpt_api
import app_logger
import db_accessor
from datetime import datetime


logger = app_logger.init()


QUERY_LIMIT = 6


def reply_message(event):
    """
    Reply the message to Line messaging API using the reply token and the completed text obtained from GPT3 API.

    Args:
        event (dict): The event payload passed by the Line messaging API.

    Raises:
        Exception: When an error occurs in replying the message.
    """
    try:
        # Parse the event body as a JSON object
        event_body = json.loads(event['body'])
        # Check if the event is a message type and is of text type
        if event_body['events'][0]['type'] == 'message' and event_body['events'][0]['message']['type'] == 'text':
            # Get the Line user ID from the event
            line_user_id = event_body['events'][0]['source']['userId']

            # Get the reply token from the event
            reply_token = event_body['events'][0]['replyToken']

            # Get the prompt text from the event
            prompt = event_body['events'][0]['message']['text']
            print(prompt)

            # Put a record of the user into the Messages table.
            db_accessor.put(line_user_id, 'user', prompt, datetime.now())

            # Query messages by Line user ID.
            items = db_accessor.query_by_line_user_id(line_user_id, QUERY_LIMIT)

            # Reverse messages
            messages = list(reversed(items))

            # Create new dict list of a prompt
            prompts = list(map(lambda message: {"role": message["role"]["S"], "content": message["content"]["S"]}, messages))

            # Call the GPT3 API to get the completed text
            completed_text = chatgpt_api.completions(prompts)

            # Remove any leading/trailing white spaces from the response message
            # response_message = completed_text.strip()

            # Put a record of the assistant into the Messages table.
            db_accessor.put(line_user_id, 'assistant', completed_text, datetime.now())

            # Create an instance of the LineBotApi with the Line channel access token
            line_bot_api = LineBotApi(const.LINE_CHANNEL_ACCESS_TOKEN)

            # Reply the message using the LineBotApi instance
            line_bot_api.reply_message(reply_token, TextSendMessage(text=completed_text))

            # Log the prompt and response message
            # logger.info(prompt)
            # logger.info(response_message)

    except Exception as e:
        # Raise the exception
        raise e
