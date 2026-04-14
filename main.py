import sys

from presentation import CLI


def main():
    if len(sys.argv) < 2:
        CLI.print_usage()
        return

    command = sys.argv[1]

    commands = {
        "migrate": CLI.cmd_migrate,
        "load": CLI.cmd_load,
        "fill": CLI.cmd_fill,
        "query": lambda: _handle_query(),
        "info": CLI.cmd_info,
        "cross-migrate": CLI.cmd_cross_migrate,
        "demo": CLI.cmd_demo,
    }

    handler = commands.get(command)
    if handler:
        handler()
    else:
        print(f"Невідома команда: {command}")
        CLI.print_usage()


def _handle_query():
    if len(sys.argv) >= 3:
        country = sys.argv[2]
        date_str = sys.argv[3] if len(sys.argv) >= 4 else None
        CLI.cmd_query_auto(country, date_str)
    else:
        CLI.cmd_query()


if __name__ == "__main__":
    main()
