USAGE = """Usage:
  Provide numeric inputs when prompted:
  - Public Key A, Private Key A, N modules A
  - Public Key B, Private Key B, N modules B
  - Message, Hash function value
"""


def print_usage(message="Invalid input."):
    print(message)
    print(USAGE)


def E(K, m, n):
    return (m ** K) % n


def H(m):
    return m % h


def main():
    try:
        ka_pu = int(input("Public Key A: "))
        ka_pr = int(input("Private Key A: "))
        na = int(input("N modules A: "))
        kb_pu = int(input("Public Key B: "))
        kb_pr = int(input("Private Key B: "))
        nb = int(input("N modules B: "))
        message = int(input("Message: "))
        global h
        h = int(input("Hash function value: "))
    except ValueError:
        print_usage()
        return

    print(f"Confidentiality: {E(kb_pu, message, nb)}")
    print(f"Authenticity and Integrity: {E(ka_pr, H(message), na)}")


if __name__ == '__main__':
    main()
