# テスト用のライブラリをインポート
import unittest
import mock

# テスト対象のモジュールをインポート
import fetch_chat_histories_by_line_user_id

QUERY_LIMIT = 7


# テストケースクラスを定義
class TestFetchChatHistoriesByLineUserId(unittest.TestCase):

    # 正常系のテストメソッドを定義
    def test_fetch_chat_histories_by_line_user_id_success(self):
        # モックオブジェクトを作成
        mock_db_accessor = mock.Mock()

        # モックオブジェクトに戻り値や副作用を設定
        mock_db_accessor.query_by_line_user_id.return_value = [
            {"role": {"S": "user"}, "content": {"S": "hello"}},
            {"role": {"S": "bot"}, "content": {"S": "hi"}},
            {"role": {"S": "user"}, "content": {"S": "how are you?"}},
            {"role": {"S": "bot"}, "content": {"S": "I'm fine, thank you."}}
        ]

        # 期待する戻り値を定義
        expected_result = [
            {"role": "bot", "content": "I'm fine, thank you."},
            {"role": "user", "content": "how are you?"},
            {"role": "bot", "content": "hi"},
            {"role": "user", "content":"hello"}
        ]

        # テスト対象の関数にモックオブジェクトと引数を渡して実行し、戻り値を取得
        actual_result = fetch_chat_histories_by_line_user_id.fetch_chat_histories_by_line_user_id("user1", db_accessor=mock_db_accessor)

        # モックオブジェクトが期待通りに呼び出されたか検証
        mock_db_accessor.query_by_line_user_id.assert_called_once_with("user1", QUERY_LIMIT)

        # 戻り値が期待通りか検証（リストの順序と要素が一致するか）
        self.assertListEqual(actual_result, expected_result)

    # 異常系のテストメソッドを定義（引数がNoneの場合）
    def test_fetch_chat_histories_by_line_user_id_fail_none(self):
        # モックオブジェクトを作成（今回は不要だが一応）
        mock_db_accessor = mock.Mock()

        # 例外が発生することを検証するためにwith文でテスト対象の関数を実行（引数にNoneを渡す）
        with self.assertRaises(Exception) as e:
            fetch_chat_histories_by_line_user_id.fetch_chat_histories_by_line_user_id(None, db_accessor=mock_db_accessor)

        # 発生した例外のメッセージが期待通りか検証
        self.assertEqual(str(e.exception), 'To query an element is none.')


# テストスイートとランナーを作成してテスト実行
suite = unittest.TestLoader().loadTestsFromTestCase(TestFetchChatHistoriesByLineUserId)
runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)