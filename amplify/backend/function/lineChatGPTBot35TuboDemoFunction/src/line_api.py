import json
from linebot import LineBotApi
from linebot.models import TextSendMessage
import const
import chatgpt_api
import message_repository
import logging

logger = logging.getLogger()


def reply_message_for_line(reply_token, completed_text):
    try:
        # Create an instance of the LineBotApi with the Line channel access token
        line_bot_api = LineBotApi(const.LINE_CHANNEL_ACCESS_TOKEN)

        # Reply the message using the LineBotApi instance
        line_bot_api.reply_message(reply_token, TextSendMessage(text=completed_text))

    except Exception as e:
        # Raise the exception
        raise e


def reply_message(event):
    try:
        # Parse the event body as a JSON object
        event_body = json.loads(event['body'])

        prompt_text = _get_prompt_text_from_event_body(event_body)
        line_user_id = _get_line_user_id_from_event_body(event_body)
        reply_token = _get_reply_token_from_event_body(event_body)
        # Check if the event is a message type and is of text type
        if prompt_text is None or line_user_id is None or reply_token is None:
            raise Exception('Elements of the event body are not found.')

        logger.info(prompt_text)

        # Put a record of the user into the Messages table.
        message_repository.insert_message(line_user_id, 'user', prompt_text)

        # Query messages by Line user ID.
        chat_histories = message_repository.fetch_chat_histories_by_line_user_id(line_user_id)

        # Call the GPT3 API to get the completed text
        completed_text = chatgpt_api.completions(chat_histories)

        # Put a record of the assistant into the Messages table.
        message_repository.insert_message(line_user_id, 'assistant', completed_text)

        # Reply the message using the LineBotApi instance
        reply_message_for_line(reply_token, completed_text)

    except Exception as e:
        # Raise the exception
        raise e


def _get_prompt_text_from_event_body(event_body):
    if event_body['events'][0]['type'] == 'message' and event_body['events'][0]['message']['type'] == 'text':
        return event_body['events'][0]['message']['text']
    return None


def _get_line_user_id_from_event_body(event_body):
    if event_body['events'][0]['source'] and event_body['events'][0]['source']['type'] == 'user':
        return event_body['events'][0]['source']['userId']
    return None


def _get_reply_token_from_event_body(event_body):
    if event_body['events'][0]['replyToken']:
        return event_body['events'][0]['replyToken']
    return None
