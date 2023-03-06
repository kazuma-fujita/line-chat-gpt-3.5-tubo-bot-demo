import json
import guard
import line_api
import app_logger

# Initialize logger for the handler function
logger = app_logger.init()


def handler(event, context):
    """
    Main handler function to process incoming events and send replies.

    Args:
        event (dict): Incoming event data from the Line Platform
        context (obj): AWS Lambda Context runtime methods and attributes

    Returns:
        dict: A JSON response with status code and body to be sent to the Line Platform
    """
    # Log the incoming event data
    logger.info(event)

    try:
        # Verify if the request is valid
        guard.verify_request(event)

        # Call line_api module to send a reply to the incoming event
        line_api.reply_message(event)
    except Exception as e:
        # Log the error
        logger.error(e)

        # Return 200 even when an error occurs as mentioned in Line API documentation
        # https://developers.line.biz/ja/reference/messaging-api/#response
        return {'statusCode': 200, 'body': json.dumps(f'Exception occurred: {e}')}

    # Return a success message if the reply was sent successfully
    return {'statusCode': 200, 'body': json.dumps('Reply ended normally.')}
