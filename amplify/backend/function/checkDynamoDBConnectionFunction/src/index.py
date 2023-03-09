import json
import boto3
import time
from datetime import datetime, timezone

TABLE_NAME = 'Messages-t6ceffvesncxvgkpx6u6yus4zm-dev'
QUERY_INDEX_NAME = 'byLineUserId'

dynamodb = boto3.client('dynamodb')

messages = [
    {'pKey': 'p0001', 'lineUserId': 'uid0001', 'role': 'user', 'content': 'What is your name?'},
    {'pKey': 'p0002', 'lineUserId': 'uid0001', 'role': 'assistant', 'content': 'My name is ChatGPT.'},
    {'pKey': 'p0003', 'lineUserId': 'uid0001', 'role': 'user', 'content': 'Where are you from?'},
    {'pKey': 'p0004', 'lineUserId': 'uid0001', 'role': 'assistant', 'content': 'I’m from the internet.'},
    {'pKey': 'p0005', 'lineUserId': 'uid0001', 'role': 'user', 'content': 'What can ChatGPT do?'},
    {'pKey': 'p0006', 'lineUserId': 'uid0001', 'role': 'assistant', 'content': 'ChatGPT can chat with you about various topics.'},
]


def handler(event, context):

    print('received event:')

    print(event)
    try:
        pKey = 'p0001'
        now = datetime.now()

        print('--- scan ---')
        scan()

        print('--- put ---')
        message = messages[0]
        pKey = message['pKey']
        put(pKey, message['lineUserId'], message['role'], message['content'], now)

        print('--- get ---')
        get(pKey)

        print('--- update ---')
        update(pKey, 'It\'s a new question.', now)

        print('--- get ---')
        get(pKey)

        print('--- delete ---')
        delete(pKey)

        print('--- put items ---')
        for message in messages:
            time.sleep(1)
            now = datetime.now()
            put(message['pKey'], message['lineUserId'], message['role'], message['content'], now)

        print('--- scan ---')
        scan()

        print('--- query ---')
        query('uid0001')

        print('--- delete items ---')
        for message in messages:
            delete(message['pKey'])

        print('--- scan ---')
        scan()

        return {
            'statusCode': 200,
            'body': json.dumps('Successfully connected to DynamoDB')
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps('Error scanning DynamoDB table')
        }


def printArray(items):
    # アイテムの要素（属性名と値）を順番にprintする
    print(f'length: {len(items)}')
    for index, item in enumerate(items):
        print(f'index: {index}')
        for key, value in item.items():
            print(key, value)


def scan():
    # スキャン結果の最後のキー
    last_key = None

    # スキャン結果が空になるまでループ
    while True:
        # スキャンパラメータを設定
        scan_params = {
            'TableName': TABLE_NAME,
        }
        # 最後のキーがあれば追加
        if last_key:
            scan_params['ExclusiveStartKey'] = last_key
        try:
            # テーブルをスキャンして結果を取得
            scan_result = dynamodb.scan(**scan_params)
            # 結果からアイテム（辞書型）のリストを取得
            items = scan_result['Items']
            printArray(items)
            # 結果から最後のキーを取得
            last_key = scan_result.get('LastEvaluatedKey')
            # 最後のキーがなければループ終了
            if not last_key:
                break
        except Exception as e:
            raise e


def query(queryKey):

    # クエリパラメータを設定
    query_params = {
        'TableName': TABLE_NAME,
        'IndexName': QUERY_INDEX_NAME,
        'KeyConditionExpression': '#lineUserId = :lineUserId',
        'ExpressionAttributeNames': {
            '#lineUserId': 'lineUserId'
        },
        'ExpressionAttributeValues': {
            ':lineUserId': {'S': queryKey}
        },
        # createdAtの降順でソート
        'ScanIndexForward': False,
        # 上位20件だけ取得
        'Limit': 20
    }
    try:
        # テーブルをクエリして結果を取得
        query_result = dynamodb.query(**query_params)
        # 結果からアイテム（辞書型）のリストを取得
        items = query_result['Items']
        printArray(items)
    except Exception as e:
        raise e


def put(pKey, uid, role, content, now):
    options = {
        'TableName': TABLE_NAME,
        'Item': {
            'id': {'S': pKey},
            'lineUserId': {'S': uid},
            'role': {'S': role},
            'content': {'S': content},
            'createdAt': {'S': now.isoformat()},
        },
    }
    try:
        dynamodb.put_item(**options)
    except Exception as e:
        raise e


def get(pKey):
    options = {
        'TableName': TABLE_NAME,
        'Key': {
            'id': {'S': pKey},
        }
    }
    try:
        ret = dynamodb.get_item(**options)
        print(ret['Item'])
    except Exception as e:
        raise e


def update(pKey, content, now):
    options = {
        'TableName': TABLE_NAME,
        'Key': {
            'id': {'S': pKey},
        },
        'UpdateExpression': 'set #content = :content, #updatedAt = :updatedAt',
        'ExpressionAttributeNames': {
            '#content': 'content',
            '#updatedAt': 'updatedAt',
        },
        'ExpressionAttributeValues': {
            ':content': {'S': content},
            ':updatedAt': {'S': now.isoformat()},
        }
    }
    try:
        dynamodb.update_item(**options)
    except Exception as e:
        raise e


def delete(pKey):
    options = {
        'TableName': TABLE_NAME,
        'Key': {
            'id': {'S': pKey},
        }
    }
    try:
        dynamodb.delete_item(**options)
    except Exception as e:
        raise e
