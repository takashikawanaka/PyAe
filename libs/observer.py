from typing import Iterator

from watchdog.observers.polling import PollingObserver

from libs.handler import Handler
from libs.process import Process


class Observer(PollingObserver):

    def __init__(
        self,
        path: str,
        patterns: list[str],
        ignore_patterns: list[str],
        command: list[str],
        reload: bool,
    ) -> None:
        # オブザーバ初期化
        super().__init__()

        # 監視対象パス
        self.__path: str = path

        # プロセス
        self.__process: Process = Process(
            command=command,
            reload=reload,
        )

        # ハンドラ
        self.__handler: Handler = Handler(
            path=path,
            patterns=patterns,
            ignore_patterns=ignore_patterns,
            process=self.__process,
        )

        # 一時停止フラグ
        self.is_pause: bool = False

        self.schedule(
            event_handler=self.__handler,
            path=self.__path,
            recursive=True,
        )

    def pause(self) -> None:
        self.is_pause: bool = not self.is_pause

    def polling(self) -> None:
        pass

    def loop(self) -> Iterator[str]:
        super().start()
        self.__process.start()
        try:
            while super().is_alive():
                self.__process.update_state()
                for line in self.__process.stdout:
                    yield line.strip()

        except:
            raise

        finally:
            self.__process.stop()
            super().stop()
            super().join(timeout=1)

    def dispatch_events(self, event_queue, timeout) -> None:  # TODO: Test
        if not self.is_pause:
            super().dispatch_events(
                event_queue=event_queue,
                timeout=timeout,
            )
