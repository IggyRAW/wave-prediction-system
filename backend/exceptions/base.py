class LibraryError(Exception):
    """
    ライブラリ全体で使用するベースの例外クラス
    """

    def __init__(self, message=None):
        if message is None:
            message = "ライブラリ内でエラーが発生しました。"
        super().__init__(message)
