import sys

MISSATGE_ERROR = "Crida incorrecta. Utilitza 'exemple_consola [valor entre 1 i 9]"


def main():
    arguments = sys.argv[1:]
    if len(arguments) != 1 or arguments[0] not in "123456789":
        print(MISSATGE_ERROR)
        return

    digit = arguments[0]
    for _ in range(int(digit)):
        print(digit * int(digit))


if __name__ == "__main__":
    main()
