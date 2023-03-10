import json
import logging

import chatgpt_api
import guard
import line_request_body_parser
import message_repository
import line_api

logger = logging.getLogger()


def handler(event, context):
    try:
        # Verify if the request is valid
        guard.verify_request(event)

        # Parse the event body as a JSON object
        event_body = json.loads(event['body'])

        prompt_text = line_request_body_parser.get_prompt_text(event_body)
        line_user_id = line_request_body_parser.get_line_user_id(event_body)
        reply_token = line_request_body_parser.get_reply_token(event_body)
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
        line_api.reply_message_for_line(reply_token, completed_text)

    except Exception as e:
        # Log the error
        logger.error(e)

        # Return 200 even when an error occurs as mentioned in Line API documentation
        # https://developers.line.biz/ja/reference/messaging-api/#response
        return {'statusCode': 200, 'body': json.dumps(f'Exception occurred: {e}')}

    # Return a success message if the reply was sent successfully
    return {'statusCode': 200, 'body': json.dumps('Reply ended normally.')}
