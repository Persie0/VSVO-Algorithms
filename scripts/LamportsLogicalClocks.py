USAGE = """Usage:
  Provide numeric inputs when prompted:
  - Amount of processors (integer >= 1)
  - Amount of rows (integer >= 1)
  - Sequence numbers for each processor
"""


def print_usage(message="Invalid input."):
    print(message)
    print(USAGE)


def main():
    try:
        processors = int(input("Amount of processor: "))
        rows = int(input("Amount of rows: "))
        if processors < 1 or rows < 1:
            raise ValueError("Counts must be >= 1.")
    except ValueError as exc:
        print_usage(str(exc))
        return

    # message from[1-Processor], to[1-Processor], step from [1-rows]
    # Example: messages = [[1, 2, 2], [2, 3, 4], [3, 2, 7], [2, 1, 9]]
    messages = [[]]  # Fill in
    number_sequences = []
    vectors = {}
    for i in range(processors):
        try:
            number_sequences.append(int(input(f"Sequence number {i + 1}: ")))
        except ValueError:
            print_usage("Sequence numbers must be integers.")
            return
        vectors[i + 1] = []
        for j in range(rows):
            vectors[i + 1].append(j * number_sequences[i])

    for message in messages:
        if len(message) != 3:
            continue
        f, t, step = message
        if vectors.get(f)[step - 1] > vectors.get(t)[step - 1]:
            vectors.get(t)[step] = vectors.get(f)[step - 1] + 1
            for x in range(step + 1, rows):
                vectors.get(t)[x] = vectors.get(t)[x - 1] + number_sequences[t - 1]

    [print(f"{z}") for z in vectors.items()]


if __name__ == '__main__':
    main()
