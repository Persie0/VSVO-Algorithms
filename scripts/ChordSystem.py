USAGE = """Usage:
  Provide numeric inputs when prompted:
  - How many nodes exist? (integer >= 1)
  - Bit-Identifier? (integer >= 1)
  - Optional Start-Node and Key (press Enter to skip)
  - Black Dots (one per line, press Enter to finish)
"""


def print_usage(message="Invalid input."):
    print(message)
    print(USAGE)


def parse_optional_int(value):
    if value.strip() == "":
        return None
    return int(value)


def read_inputs():
    nodes_length = int(input("How many nodes exist?: "))
    bit_id = int(input("Bit-Identifier?: "))
    if nodes_length < 1 or bit_id < 1:
        raise ValueError("Node count and Bit-Identifier must be >= 1.")

    start_node = parse_optional_int(input("Start-Node: "))
    key = parse_optional_int(input("Key: "))
    path = []
    if start_node is not None and key is not None:
        path.append(start_node)

    entities = []
    entities_dict = {}

    while True:
        node_text = input("Black Dots: ")
        if node_text.strip() == "":
            break
        node = int(node_text)
        entities.append(node)
        entities_dict[node] = ""

    if not entities:
        raise ValueError("At least one Black Dot is required.")

    return nodes_length, bit_id, start_node, key, path, entities, entities_dict


# finds successor of given node
def find_succ(node, entities):
    above = [i for i in entities if node <= i]
    return min(above) if above != [] else entities[0]


def find_closest(list, nodes_length, key):
    # ID, shortest-distance
    curr = []
    for i in range(len(list)):
        dist = (nodes_length - list[i] + key) % nodes_length
        if not curr or curr[1] > dist:
            curr = [list[i], dist]
    return curr


def main():
    try:
        nodes_length, bit_id, start_node, key, path, entities, entities_dict = read_inputs()
    except ValueError as exc:
        print_usage(str(exc))
        return

    for node in entities:
        nodes = []
        for i in range(1, bit_id + 1):
            nodes.append(find_succ((node + pow(2, i - 1)) % nodes_length, entities))
        entities_dict[node] = nodes

    if key is not None and start_node is not None:
        closest = []
        for i in range(len(entities_dict)):
            try:
                temp = find_closest(entities_dict.get(path[i]), nodes_length, key)
                if not closest or closest[1] > temp[1]:
                    closest = temp
                    path.append(closest[0])
            except IndexError:
                path.append(entities_dict.get(path[-1])[0])
                print(path)
                break
    else:
        # prints the list
        for node_key, entries in entities_dict.items():
            print(f"\nNode: {node_key}")
            [print(f"ID: {i + 1} Node: {entry}") for i, entry in enumerate(entries)]


if __name__ == '__main__':
    main()
