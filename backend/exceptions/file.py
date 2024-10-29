from exceptions.base import LibraryError


class FileNotFoundError(LibraryError):
    """
    ファイルが見つからない場合の例外
    """

    def __init__(self, filepath):
        message = f"ファイルが見つかりません：{filepath}"
        super().__init__(message)
