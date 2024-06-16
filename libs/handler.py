import os
from hashlib import md5
from typing import Callable

from watchdog.events import (
    FileCreatedEvent,
    FileDeletedEvent,
    FileModifiedEvent,
    FileMovedEvent,
    PatternMatchingEventHandler,
)


class Handler(PatternMatchingEventHandler):

    def __init__(
        self,
        path: str,
        patterns: list[str],
        ignore_patterns: list[str],
        process: Callable,
    ) -> None:
        self.path: str = path

        # ハンドラ初期化
        super().__init__(
            patterns=patterns,
            ignore_patterns=ignore_patterns,
            ignore_directories=True,
            case_sensitive=False,
        )

        # ファイルの変更の差異を検出するためのhash置き場
        self.__cache_hash: dict[str, str] = {}
        for dir, _, files in os.walk(top=self.path):
            for file in files:
                self.__set_hash(path=os.path.join(dir, file))

        # プロセス
        self.__process: Callable = process
        self.__process.execute()

    def on_moved(self, event: FileMovedEvent) -> None:
        print(f"File moved, {event.src_path} to {event.src_path}")
        self.__cache_hash.pop(event.src_path)
        self.__set_hash(path=event.dest_path)
        self.__process.execute()

    def on_created(self, event: FileCreatedEvent) -> None:
        print(f"File created, {event.src_path}")
        # 新規作成
        self.__set_hash(path=event.src_path)
        self.__process.execute()

    def on_deleted(self, event: FileDeletedEvent) -> None:
        print(f"File deleted, {event.src_path}")
        # 削除
        self.__cache_hash.pop(event.src_path)
        self.__process.execute()

    def on_modified(self, event: FileModifiedEvent) -> None:
        filepath: str = event.src_path
        hash: str = self.__get_file_hash(path=filepath)

        if hash != self.__cache_hash[filepath]:
            # ファイルに変更があった場合、書き換え
            print(f"File modified, {event.src_path}")
            self.__cache_hash[filepath] = hash
            self.__process.execute()

    def __get_file_hash(self, path: str) -> str:
        with open(file=path, mode="rb") as f:
            return md5(string=f.read()).hexdigest()

    def __set_hash(self, path: str) -> str:
        self.__cache_hash[path] = self.__get_file_hash(path=path)
