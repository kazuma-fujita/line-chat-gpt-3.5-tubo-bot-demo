# import asyncio
import uuid
from datetime import datetime

import chatgpt_api
import db_accessor
import message_repository

QUERY_LIMIT = 7


# async def fetch_chat_histories_by_line_user_id(line_user_id):
def fetch_chat_histories_by_line_user_id(line_user_id):
    try:
        if line_user_id is None:
            raise Exception('To query an element is none.')

        # Query messages by Line user ID.
        # db_results = await db_accessor.query_by_line_user_id(line_user_id, QUERY_LIMIT)
        db_results = db_accessor.query_by_line_user_id(line_user_id, QUERY_LIMIT)

        # Reverse messages
        reserved_results = list(reversed(db_results))

        # Create new dict list of a prompt
        return list(map(lambda item: {"role": item["role"]["S"], "content": item["content"]["S"]}, reserved_results))
    except Exception as e:
        # Raise the exception
        raise e


# async def insert_message(line_user_id, role, prompt_text):
def insert_message(line_user_id, role, prompt_text):
    try:
        if prompt_text is None or role is None or line_user_id is None:
            raise Exception('To insert elements are none.')

        # Create a partition key
        partition_key = str(uuid.uuid4())

        # Put a record of the user into the Messages table.
        # await db_accessor.put_message(partition_key, line_user_id, role, prompt_text, datetime.now())
        db_accessor.put_message(partition_key, line_user_id, role, prompt_text, datetime.now())

    except Exception as e:
        # Raise the exception
        raise e


# async def create_completed_text(line_user_id, prompt_text):
def create_completed_text(line_user_id, prompt_text):
    # Put a record of the user into the Messages table.
    # await message_repository.insert_message(line_user_id, 'user', prompt_text)
    message_repository.insert_message(line_user_id, 'user', prompt_text)

    # Query messages by Line user ID.
    # chat_histories = await message_repository.fetch_chat_histories_by_line_user_id(line_user_id)
    chat_histories = message_repository.fetch_chat_histories_by_line_user_id(line_user_id)

    # Call the GPT3 API to get the completed text
    # completed_text = await chatgpt_api.completions(chat_histories)
    completed_text = chatgpt_api.completions(chat_histories)

    # Put a record of the assistant into the Messages table.
    # await message_repository.insert_message(line_user_id, 'assistant', completed_text)
    message_repository.insert_message(line_user_id, 'assistant', completed_text)
    return completed_text
