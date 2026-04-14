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
        "info": CLI.cmd_info,
    }

    handler = commands.get(command)
    if handler:
        handler()
    else:
        print(f"Невідома команда: {command}")
        CLI.print_usage()


if __name__ == "__main__":
    main()
