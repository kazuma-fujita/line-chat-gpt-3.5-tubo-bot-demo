import json
import logging

import guard
import line_api
import line_request_body_parser
import message_repository

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

        # completed_text = asyncio.run(message_repository.create_completed_text(line_user_id, prompt_text))
        # loop = asyncio.get_event_loop()
        # completed_text = loop.run_until_complete(message_repository.create_completed_text(line_user_id, prompt_text))
        completed_text = message_repository.create_completed_text(line_user_id, prompt_text)
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
