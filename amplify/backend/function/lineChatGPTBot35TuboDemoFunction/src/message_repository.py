from datetime import datetime
import uuid
import db_accessor


QUERY_LIMIT = 7


def fetch_chat_histories_by_line_user_id(line_user_id):
    try:
        if line_user_id is None:
            raise Exception('To query an element is none.')

        # Query messages by Line user ID.
        db_results = db_accessor.query_by_line_user_id(line_user_id, QUERY_LIMIT)

        # Reverse messages
        reserved_results = list(reversed(db_results))

        # Create new dict list of a prompt
        return list(map(lambda item: {"role": item["role"]["S"], "content": item["content"]["S"]}, reserved_results))
    except Exception as e:
        # Raise the exception
        raise e


def insert_message(line_user_id, role, prompt_text):
    try:
        if prompt_text is None or role is None or line_user_id is None:
            raise Exception('To insert elements are none.')

        # Create a partition key
        partition_key = str(uuid.uuid4())

        # Put a record of the user into the Messages table.
        db_accessor.put_message(partition_key, line_user_id, role, prompt_text, datetime.now())

    except Exception as e:
        # Raise the exception
        raise e

