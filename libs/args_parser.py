from argparse import ArgumentParser, Namespace


def args_parser() -> Namespace:
    # パーサー
    parser: ArgumentParser = ArgumentParser(
        allow_abbrev=False,
    )

    # 必須パラメータ
    required_args = parser.add_argument_group("required arguments")

    # コマンド実行
    required_args.add_argument(
        "--command",
        "-c",
        action="store",
        nargs="?",
        default="",
        type=str,
        required=True,
        help="Command",
        dest="command",
    )

    # 任意パラメータ
    optional_args = parser.add_argument_group("optional arguments")

    # 監視ディレクトリ
    required_args.add_argument(
        "--path",
        action="store",
        nargs="?",
        default=".",
        type=str,
        required=False,
        help="Target Path",
        dest="path",
    )

    # 監視対象パターン
    required_args.add_argument(
        "--patterns",
        "-p",
        action="store",
        nargs="*",
        default="*",
        type=str,
        required=False,
        help="Target Patterns",
        dest="patterns",
    )

    # 監視非対象パターン
    required_args.add_argument(
        "--ignore_patterns",
        "-i",
        action="store",
        nargs="*",
        default="",
        type=str,
        required=False,
        help="Ignore Pattern",
        dest="ignore_patterns",
    )

    # 環境変数を設定
    optional_args.add_argument(  # TODO: 環境変数
        "--environment",
        "-e",
        action="store",
        nargs="*",
        default="",
        type=str,
        required=False,
        help="Environmental Variables",
        dest="environment",
    )

    # ログ保存先
    optional_args.add_argument(  # TODO: ログ出力
        "--save",
        "-s",
        action="store",
        nargs="?",
        default="",
        type=str,
        required=False,
        help="Save",
        dest="save",
    )

    # リロードするか?
    optional_args.add_argument(
        "--is_reload",
        "-r",
        action="store_true",
        default=False,
        required=False,
        help="Reload",
        dest="reload",
    )

    args = parser.parse_args()
    if args.patterns and "," in args.patterns[0]:
        # 監視対象パターンが文字列で入力された場合、配列に分解する
        if 1 < len(args.patterns):
            raise ValueError("Too many patterns parameter")
        args.patterns = args.patterns[0].split(",")

    if args.ignore_patterns and "," in args.ignore_patterns[0]:
        # 監視非対象パターンが文字列で入力された場合、配列に分解する
        if 1 < len(args.ignore_patterns):
            raise ValueError("Too many ignore patterns parameter")
        args.ignore_patterns = args.ignore_patterns[0].split(",")

    if args.environment and "," in args.environment[0]:
        # 環境変数が文字列で入力された場合、配列に分解する
        if 1 < len(args.environment):
            raise ValueError("Too many enviroment parameter")
        args.environment = args.environment[0].split(",")

    if 1 == len(args.command):
        # コマンドパラメータに入力された値が一つだった場合、分割する
        args.command = args.command.split(" ")

    return args
