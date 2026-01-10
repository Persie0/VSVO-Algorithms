import random

USAGE = """Usage:
  Provide numeric inputs when prompted:
  - N (integer >= 1)
  - Read important? (1 = True, anything else = False)
"""


def print_usage(message="Invalid input."):
    print(message)
    print(USAGE)


def main():
    try:
        N = int(input("N: "))
        if N < 1:
            raise ValueError("N must be >= 1.")
        read_important = int(input("1 = True : Other = False ")) == 1
    except ValueError as exc:
        print_usage(str(exc))
        return

    if read_important:
        print(f"N_r = {1}\nN_w = {N}")
    else:
        x = random.randint(N // 2, N)
        y = random.randint(N - x + 1, N)
        print(f"N_r = {y}\nN_w = {x}")


if __name__ == '__main__':
    main()
