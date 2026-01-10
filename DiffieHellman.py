USAGE = """Usage:
  Provide numeric inputs when prompted:
  - n, g, a, b (integers)
"""


def print_usage(message="Invalid input."):
    print(message)
    print(USAGE)


def main():
    try:
        n = int(input("n: "))
        g = int(input("g: "))
        a = int(input("a: "))
        b = int(input("b: "))
    except ValueError:
        print_usage()
        return

    print(f"{g}^({a}*{b}) mod {n}: {pow(g, a * b) % n}")


if __name__ == '__main__':
    main()
