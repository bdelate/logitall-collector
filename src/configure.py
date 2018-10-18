from typing import Optional


def get_menu_input() -> Optional[int]:
    """Prompt the user with the available configuration options"""
    options = [
        '1: List directories being monitored',
        '2: Add directory to be monitored',
    ]
    print(*options, sep='\n')

    try:
        choice = int(input('> '))
        if choice not in range(1, len(options) + 1):
            raise ValueError
    except ValueError:
        print('Invalid choice.')
        return None
    else:
        return choice


if __name__ == "__main__":
    option = get_menu_input()

