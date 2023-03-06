import json
from linebot import LineBotApi
from linebot.models import TextSendMessage
import const
import gpt3_api
import app_logger

logger = app_logger.init()


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
            # Get the reply token from the event
            replyToken = event_body['events'][0]['replyToken']

            # Get the prompt text from the event
            prompt = event_body['events'][0]['message']['text']

            # Call the GPT3 API to get the completed text
            completed_text = gpt3_api.completions(prompt)

            # Remove any leading/trailing white spaces from the response message
            response_message = completed_text.strip()

            # Create an instance of the LineBotApi with the Line channel access token
            line_bot_api = LineBotApi(const.LINE_CHANNEL_ACCESS_TOKEN)

            # Reply the message using the LineBotApi instance
            line_bot_api.reply_message(replyToken, TextSendMessage(text=response_message))

            # Log the prompt and response message
            logger.info(prompt)
            logger.info(response_message)

    except Exception as e:
        # Raise the exception
        raise e
