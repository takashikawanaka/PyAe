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
        self.__reload: bool = reload
        self.__book_execute: bool = False

    @property
    def stdout(self) -> any:
        return self.__process.stdout

    def execute(self) -> None:
        if self.__process is None or not self.is_processing():
            # プロセスが存在しない場合．終了している場合
            self.__process = self.__execute()

        elif self.__reload:
            # リロードが許可されている場合
            self.kill()
            self.__process = self.__execute()

        else:
            # プロセス終了後に再実行
            self.__book_execute = True

    def reload(self) -> None:
        if self.__book_execute and not self.is_processing():
            self.__book_execute = False
            self.__process = self.__execute()

    def kill(self) -> None:
        self.__process.kill()
        self.__process = None

    def is_processing(self) -> bool:
        return self.__process.poll() is None
