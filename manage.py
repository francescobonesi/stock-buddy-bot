import os
import sys


def _y_n_question():
    answer = ""
    while answer not in ["y", "yes", "n", "no"]:
        answer = input("(Chaos-Ayreon reference) Are you sure you want to continue? (y/n) ").lower()

    if answer in ["y", "yes"]:
        return True
    else:
        return False


def _copy_file(src, dst):
    import shutil
    shutil.copy(src, dst)


def _create_dummy_file(filename, extension):
    path = f'./{filename}.{extension}'
    if os.path.exists(path):
        print(f"File '{path}' already exists, "
              "this operation is going to override it.")
        if _y_n_question():
            _copy_file(path, f'{path}.bk')
            print(f"Original file backup '{path}.bk'")
            _copy_file(f'./sample-{filename}.{extension}', path)
            print(f"Created new file '{path}' with sample content.")
        else:
            print(f"Not proceeding, keeping existing '{path}' file.")
    else:
        _copy_file(f'./sample-{filename}.{extension}', path)
        print(f"Created new file '{path}' with sample content.")


def validate_config_files(*_):
    if not os.path.exists("./config.ini"):
        print("Missing 'config.ini' file")
        return False
    elif not os.path.exists("./portfolio.csv"):
        print("Missing 'portfolio.csv' file")
        return False
    else:
        print("Config file and portfolio file exist. All good.")
        return True


def create_portfolio_csv(*_):
    _create_dummy_file('portfolio', 'csv')


def create_config_ini_file(*_):
    _create_dummy_file('config', 'ini')


def create_bot_webhook_commands(*_):
    from config import Config
    _c = Config()
    print("\nSet webhook by browsing:")
    print(_c.set_webook_cmd())
    print("\nAfter setting check it by browsing:")
    print(_c.get_webook_cmd())
    print("\nIn case you want to remove it, browse:")
    print(_c.remove_webook_cmd())


def print_error_message(*args):
    if len(args) < 2:
        print("Please provide a command!")
    else:
        print(f"The command {args[1]} is not allowed")


manage_commands = {
    "validate": validate_config_files,
    "config": create_config_ini_file,
    "portfolio": create_portfolio_csv,
    "webhook": create_bot_webhook_commands,
    "error": print_error_message
}

if __name__ == '__main__':
    command = sys.argv[1] if len(sys.argv) >= 2 else "error"
    manage_commands.get(command, print_error_message)(*sys.argv)
