import time
from argparse import Namespace

from libs.args_parser import args_parser
from libs.observer import Observer


class Logging:
    pass


if __name__ == "__main__":
    args: Namespace = args_parser()

    print("Initialization...")
    # オブザーバー
    observer: Observer = Observer(
        path=args.path,
        patterns=args.patterns,
        ignore_patterns=args.ignore_patterns,
        command=args.command,
        reload=args.reload,
    )

    print(f"Start watching... {args.path}")
    try:
        for line in observer.loop():
            print(line)
            time.sleep(1)

    except KeyboardInterrupt:
        pass

    except Exception as e:
        print(e)

    print(f"Stop watching...")
