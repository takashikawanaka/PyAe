import subprocess
from typing import Callable, Iterator


class Process:

    def __init__(
        self,
        command: list[str],
        reload: bool,
    ) -> None:
        self.__execute: Callable = lambda: subprocess.Popen(
            args=command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        self.__process: subprocess.CompletedProcess = None
        self.__is_processing: bool = False
        self.__reload: bool = reload
        self.__book_execute: bool = False

    @property
    def stdout(self) -> any:
        return self.__process.stdout

    def start(self) -> None:
        self.__process = self.__execute()

    def stop(self) -> None:
        self.__process.kill()
        self.__process = None

    def execute(self) -> None:
        if self.__is_processing:
            # プロセスが存在しない場合．終了している場合
            self.__process = self.__execute()

        elif self.__reload:
            # リロードが許可されている場合
            self.stop()
            self.__process = self.__execute()

        else:
            # プロセス終了後に再実行
            self.__book_execute = True

    def update_state(self) -> None:
        # プロセス状態を更新
        self.__is_processing = self.__process.poll() is None
        if self.__book_execute and not self.__is_processing:
            # 実行予約がされていてかつ、動作中ではない場合
            self.__book_execute = False
            self.__process = self.__execute()
