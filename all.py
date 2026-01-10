from datetime import timedelta
import random
import sys

from tabulate import tabulate


def berkeley_print_usage(message="Invalid input."):
    print(message)
    print(
        "Usage:\n"
        "  Provide numeric inputs when prompted:\n"
        "  - How many servers? (integer >= 1)\n"
        "  - Each server time as HHMM (e.g., 1530 for 3:30 pm)\n"
        "  - Time Daemon index within range 0..N-1"
    )


class BerkeleyServer:
    def __init__(self, name, time):
        self.name = name
        self.time = timedelta(
            hours=int(time[:len(time) // 2]),
            minutes=int(time[len(time) // 2:])
        ).total_seconds()
        self.time_daemon = False


def berkeley_parse_time_input(value):
    if not value.isdigit() or len(value) % 2 != 0:
        raise ValueError("Time must be digits in HHMM format.")
    return value


def berkeley_start_app():
    servers = []
    letters = [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ]
    server_count = int(input("How many servers? "))
    if server_count < 1:
        raise ValueError("Server count must be at least 1.")
    for i in range(server_count):
        s = berkeley_parse_time_input(input(f"Server {letters[i]}: "))
        servers.append(BerkeleyServer(f"Server {letters[i]}", s))
    while True:
        print(f"\nWhich server is the time daemon? Range: 0-{len(servers) - 1}")
        time_daemon = int(input("Time Daemon: "))
        if time_daemon < 0 or time_daemon >= len(servers):
            print("Invalid input")
        else:
            servers[time_daemon].time_daemon = True
            break
    return servers, servers[time_daemon]


def berkeley_convert_seconds(time):
    m, s = divmod(abs(time), 60)
    h, m = divmod(m, 60)
    sign = " "
    if time < 0:
        sign = "-"
    return f"{sign}{int(h):02d}:{int(m):02d}:{int(s):02d}"


def berkeley_round_one(servers, time_daemon):
    print("\nRound 1")
    for s in servers:
        print(f"{time_daemon.name} {s.name}: {berkeley_convert_seconds(s.time)}")


def berkeley_round_two(servers, time_daemon):
    print("\nRound 2")
    differences = []
    for s in servers:
        diff = s.time - time_daemon.time
        print(f"{s.name} to {time_daemon.name}: {berkeley_convert_seconds(diff)}")
        differences.append(diff)
    return differences


def berkeley_round_three(servers, time_differences, time_daemon):
    print("\nRound 3")
    avg = sum(time_differences) / len(time_differences)
    for s in servers:
        diff = time_daemon.time + avg - s.time
        print(
            f"{time_daemon.name} to {s.name}: {berkeley_convert_seconds(diff)}"
            f" | Final Time: {berkeley_convert_seconds(s.time + diff)}"
        )


def berkeley_main():
    try:
        network_servers, time_daemon = berkeley_start_app()
    except ValueError as exc:
        berkeley_print_usage(str(exc))
        return

    berkeley_round_one(network_servers, time_daemon)
    time_differences = berkeley_round_two(network_servers, time_daemon)
    berkeley_round_three(network_servers, time_differences, time_daemon)


def chord_print_usage(message="Invalid input."):
    print(message)
    print(
        "Usage:\n"
        "  Provide numeric inputs when prompted:\n"
        "  - How many nodes exist? (integer >= 1)\n"
        "  - Bit-Identifier? (integer >= 1)\n"
        "  - Optional Start-Node and Key (press Enter to skip)\n"
        "  - Black Dots (one per line, press Enter to finish)"
    )


def chord_parse_optional_int(value):
    if value.strip() == "":
        return None
    return int(value)


def chord_read_inputs():
    nodes_length = int(input("How many nodes exist?: "))
    bit_id = int(input("Bit-Identifier?: "))
    if nodes_length < 1 or bit_id < 1:
        raise ValueError("Node count and Bit-Identifier must be >= 1.")

    start_node = chord_parse_optional_int(input("Start-Node: "))
    key = chord_parse_optional_int(input("Key: "))
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


def chord_find_succ(node, entities):
    above = [i for i in entities if node <= i]
    return min(above) if above != [] else entities[0]


def chord_find_closest(items, nodes_length, key):
    curr = []
    for i in range(len(items)):
        dist = (nodes_length - items[i] + key) % nodes_length
        if not curr or curr[1] > dist:
            curr = [items[i], dist]
    return curr


def chord_main():
    try:
        nodes_length, bit_id, start_node, key, path, entities, entities_dict = chord_read_inputs()
    except ValueError as exc:
        chord_print_usage(str(exc))
        return

    for node in entities:
        nodes = []
        for i in range(1, bit_id + 1):
            nodes.append(chord_find_succ((node + pow(2, i - 1)) % nodes_length, entities))
        entities_dict[node] = nodes

    if key is not None and start_node is not None:
        closest = []
        for i in range(len(entities_dict)):
            try:
                temp = chord_find_closest(entities_dict.get(path[i]), nodes_length, key)
                if not closest or closest[1] > temp[1]:
                    closest = temp
                    path.append(closest[0])
            except IndexError:
                path.append(entities_dict.get(path[-1])[0])
                print(path)
                break
    else:
        for node_key, entries in entities_dict.items():
            print(f"\nNode: {node_key}")
            [print(f"ID: {i + 1} Node: {entry}") for i, entry in enumerate(entries)]


def crypto_print_usage(message="Invalid input."):
    print(message)
    print(
        "Usage:\n"
        "  Provide numeric inputs when prompted:\n"
        "  - Public Key A, Private Key A, N modules A\n"
        "  - Public Key B, Private Key B, N modules B\n"
        "  - Message, Hash function value"
    )


def crypto_E(K, m, n):
    return (m ** K) % n


def crypto_H(m, h):
    return m % h


def crypto_main():
    try:
        ka_pu = int(input("Public Key A: "))
        ka_pr = int(input("Private Key A: "))
        na = int(input("N modules A: "))
        kb_pu = int(input("Public Key B: "))
        kb_pr = int(input("Private Key B: "))
        nb = int(input("N modules B: "))
        message = int(input("Message: "))
        h = int(input("Hash function value: "))
    except ValueError:
        crypto_print_usage()
        return

    print(f"Confidentiality: {crypto_E(kb_pu, message, nb)}")
    print(f"Authenticity and Integrity: {crypto_E(ka_pr, crypto_H(message, h), na)}")


def diffie_print_usage(message="Invalid input."):
    print(message)
    print(
        "Usage:\n"
        "  Provide numeric inputs when prompted:\n"
        "  - n, g, a, b (integers)"
    )


def diffie_main():
    try:
        n = int(input("n: "))
        g = int(input("g: "))
        a = int(input("a: "))
        b = int(input("b: "))
    except ValueError:
        diffie_print_usage()
        return

    print(f"{g}^({a}*{b}) mod {n}: {pow(g, a * b) % n}")


def greedy_print_usage(message="Invalid input."):
    print(message)
    print(
        "Usage:\n"
        "  Provide numeric inputs when prompted:\n"
        "  - Number of latencies per client (integer >= 1)\n"
        "  - Number of clients (integer >= 1)\n"
        "  - Latency values for each client/server pair"
    )


def greedy_main():
    try:
        num_latencies = int(input("Enter the number of latencies per client: "))
        num_clients = int(input("Enter the number of clients: "))
        if num_latencies < 1 or num_clients < 1:
            raise ValueError("Counts must be >= 1.")
        options = [[0 for _ in range(num_latencies)] for _ in range(num_clients)]

        for i in range(num_clients):
            for j in range(num_latencies):
                latency = int(input(f"Enter latency for client {i + 1}, latency {j + 1}: "))
                options[j][i] = latency
    except ValueError as exc:
        greedy_print_usage(str(exc))
        return

    headers = [""] + [f"L{j + 1}" for j in range(num_latencies)]
    table = [[f"C{i + 1}"] + [options[j][i] for j in range(num_latencies)] for i in range(num_clients)]
    print(tabulate(table, headers, tablefmt="grid"))

    total_latencies = {i + 1: sum(x) for i, x in enumerate(options)}
    first_server = min(total_latencies.items(), key=lambda x: x[1])

    minimum = {}
    for i, option in enumerate(options):
        if i != first_server[0] - 1:
            curr = [min(o, options[first_server[0] - 1][j]) for j, o in enumerate(option)]
            minimum[i + 1] = curr

    second_server = min(minimum.items(), key=lambda x: sum(x[1]))

    print(f"First Server to select: L{first_server[0]}")
    print(f"Second Server to select: L{second_server[0]}")
    print(f"Total Latency of the solution: {sum(second_server[1])}")

    print("-------------------------")
    print("Servers selected in descending order of total latency:")
    for server, latency in total_latencies.items():
        print(f"Server L{server}: Total Latency = {latency}")


def greedy_fixed_print_usage(message="Invalid input."):
    print(message)
    print(
        "Usage:\n"
        "  Provide numeric inputs when prompted:\n"
        "  - Number of latencies per client (integer >= 1)\n"
        "  - Number of clients (integer >= 1)\n"
        "  - Latency values for each client/server pair"
    )


def greedy_fixed_main():
    try:
        num_latencies = int(input("Enter the number of latencies per client: "))
        num_clients = int(input("Enter the number of clients: "))
        if num_latencies < 1 or num_clients < 1:
            raise ValueError("Counts must be >= 1.")
        options = [[0 for _ in range(num_latencies)] for _ in range(num_clients)]

        for i in range(num_clients):
            for j in range(num_latencies):
                latency = int(input(f"Enter latency for client {i + 1}, latency {j + 1}: "))
                options[i][j] = latency
    except ValueError as exc:
        greedy_fixed_print_usage(str(exc))
        return

    headers = [""] + [f"L{j + 1}" for j in range(num_latencies)]
    table = [[f"C{i + 1}"] + options[i] for i in range(num_clients)]
    print(tabulate(table, headers, tablefmt="grid"))

    total_latencies = {
        j + 1: sum(options[i][j] for i in range(num_clients))
        for j in range(num_latencies)
    }

    first_server = min(total_latencies.items(), key=lambda x: x[1])
    first_idx = first_server[0] - 1

    minimum = {}
    for j in range(num_latencies):
        if j != first_idx:
            curr = [min(options[i][j], options[i][first_idx]) for i in range(num_clients)]
            minimum[j + 1] = curr

    second_server = min(minimum.items(), key=lambda x: sum(x[1]))
    second_idx = second_server[0] - 1

    third_candidates = {}
    for j in range(num_latencies):
        if j not in (first_idx, second_idx):
            curr = [
                min(
                    options[i][j],
                    second_server[1][i]
                )
                for i in range(num_clients)
            ]
            third_candidates[j + 1] = curr

    third_server = None
    if third_candidates:
        third_server = min(third_candidates.items(), key=lambda x: sum(x[1]))

    print(f"First Server to select: L{first_server[0]}")
    print(f"Second Server to select: L{second_server[0]}")
    if third_server:
        print(f"Third Server to select: L{third_server[0]}")
        print(f"Total Latency of the solution: {sum(third_server[1])}")
    else:
        print("Third Server to select: N/A")
        print(f"Total Latency of the solution: {sum(second_server[1])}")

    print("-------------------------")
    print("Servers selected in descending order of total latency:")
    for server, latency in sorted(total_latencies.items(), key=lambda x: x[1], reverse=True):
        print(f"Server L{server}: Total Latency = {latency}")


def lamports_print_usage(message="Invalid input."):
    print(message)
    print(
        "Usage:\n"
        "  Provide numeric inputs when prompted:\n"
        "  - Amount of processors (integer >= 1)\n"
        "  - Amount of rows (integer >= 1)\n"
        "  - Sequence numbers for each processor"
    )


def lamports_main():
    try:
        processors = int(input("Amount of processor: "))
        rows = int(input("Amount of rows: "))
        if processors < 1 or rows < 1:
            raise ValueError("Counts must be >= 1.")
    except ValueError as exc:
        lamports_print_usage(str(exc))
        return

    messages = [[]]  # Fill in
    number_sequences = []
    vectors = {}
    for i in range(processors):
        try:
            number_sequences.append(int(input(f"Sequence number {i + 1}: ")))
        except ValueError:
            lamports_print_usage("Sequence numbers must be integers.")
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


def polyring_print_usage(message="Invalid input."):
    print(message)
    print(
        "Usage:\n"
        "  Provide numeric inputs when prompted:\n"
        "  - Depth (integer >= 1)\n"
        "  - Node Amounts per Depth (integer >= 1)\n"
        "  - Start Node Identifier and End Node Identifier (string like 0.1.2)"
    )


class PolyringNode:
    def __init__(self, identifier):
        self.identifier = identifier
        self.parent = None
        self.children = []


def polyring_construct_graph(depth, node_amount):
    graph = [PolyringNode(str(i)) for i in range(node_amount)]

    for d in range(1, depth):
        next_layer = []
        for node in graph:
            for i in range(node_amount):
                child_identifier = node.identifier + '.' + str(i)
                child = PolyringNode(child_identifier)
                child.parent = node
                node.children.append(child)
                next_layer.append(child)
        graph = next_layer

    return graph


def polyring_get_ancestors(node):
    ancestors = []
    current_node = node.parent
    while current_node:
        ancestors.append(current_node)
        current_node = current_node.parent
    return ancestors[::-1]


def polyring_calculate_matching_coordinates(guid1, guid2):
    coords1 = guid1.split('.')
    coords2 = guid2.split('.')

    matching_coords = 0
    for coord1, coord2 in zip(coords1, coords2):
        if coord1 == coord2:
            matching_coords += 1
        else:
            break
    return matching_coords


def polyring_get_first_node(node):
    current_node = node
    while current_node.parent:
        current_node = current_node.parent
    return current_node


def polyring_find_node_by_prefix(graph, prefix):
    for node in graph:
        if node.identifier.startswith(prefix):
            current_node = node
            while current_node.identifier != prefix:
                current_node = current_node.parent
            return current_node
    return None


def polyring_find_path_in_polyring(start_node, end_node):
    path = [start_node.identifier]
    sibling_count = 0

    while start_node.identifier != end_node.identifier:
        length_of_routing = len(start_node.identifier.split('.'))
        length_of_destination = len(end_node.identifier.split('.'))
        matching_coords = polyring_calculate_matching_coordinates(
            start_node.identifier,
            end_node.identifier
        )

        if matching_coords <= length_of_routing - 2:
            start_node = start_node.parent
            path.append(start_node.identifier)
            sibling_count = 0

        elif matching_coords == length_of_routing - 1:
            if length_of_destination == length_of_routing - 1:
                start_node = start_node.parent
                path.append(start_node.identifier)
                sibling_count = 0
            elif length_of_destination >= length_of_routing:
                start_node = start_node.parent
                if start_node is None:
                    start_node = polyring_get_first_node(end_node)
                else:
                    start_node = start_node.children[sibling_count]
                    sibling_count += 1
                if start_node.identifier not in path:
                    path.append(start_node.identifier)
        elif matching_coords == length_of_routing:
            sibling_count = 0
            if length_of_routing < length_of_destination:
                start_node = start_node.children[sibling_count]
            path.append(start_node.identifier)
    return path


def polyring_main():
    try:
        depth = int(input("Depth: "))
        node_amount = int(input("Node Amounts per Depth: "))
        if depth < 1 or node_amount < 1:
            raise ValueError("Depth and node amounts must be >= 1.")
    except ValueError as exc:
        polyring_print_usage(str(exc))
        return

    graph = polyring_construct_graph(depth, node_amount)

    start_guid = input("Start Node Identifier: ")
    end_guid = input("End Node Identifier: ")

    start_node = polyring_find_node_by_prefix(graph, start_guid)
    end_node = polyring_find_node_by_prefix(graph, end_guid)

    if start_node is None:
        print(f"No node found with prefix '{start_guid}'")
    elif end_node is None:
        print(f"No node found with prefix '{end_guid}'")
    else:
        path = polyring_find_path_in_polyring(start_node, end_node)
        if path:
            print("Path found:")
            print(" -> ".join(path))
        else:
            print("No path found.")


def read_write_print_usage(message="Invalid input."):
    print(message)
    print(
        "Usage:\n"
        "  Provide numeric inputs when prompted:\n"
        "  - N (integer >= 1)\n"
        "  - Read important? (1 = True, anything else = False)"
    )


def read_write_main():
    try:
        N = int(input("N: "))
        if N < 1:
            raise ValueError("N must be >= 1.")
        read_important = int(input("1 = True : Other = False ")) == 1
    except ValueError as exc:
        read_write_print_usage(str(exc))
        return

    if read_important:
        print(f"N_r = {1}\nN_w = {N}")
    else:
        x = random.randint(N // 2, N)
        y = random.randint(N - x + 1, N)
        print(f"N_r = {y}\nN_w = {x}")


def vector_clock_print_usage(message="Invalid input."):
    print(message)
    print(
        "Usage:\n"
        "  This script uses predefined vectors and task list.\n"
        "  Update the vectors and task_list variables before running."
    )


def vector_clock_update_vectors(vector_from, vector_to):
    updated_vector = vector_to
    for idx, (v_from, v_to) in enumerate(zip(vector_from, vector_to)):
        if v_from > v_to:
            updated_vector[idx] = v_from
    return updated_vector


def vector_clock_solve_vector_clocks(vectors, task_list):
    for i, tasks in enumerate(task_list):
        for task in tasks:
            if len(task) == 2:
                v_from, v_to = int(task[0]) - 1, int(task[1]) - 1
                vectors[v_from][v_from] += 1
                vectors[v_to] = vector_clock_update_vectors(vectors[v_from], vectors[v_to])
                vectors[v_to][v_to] += 1
            else:
                inc = int(task[0])
                vectors[inc - 1][inc - 1] += 1
        print(f"t{i + 1} {vectors}")


def vector_clock_main():
    vectors = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]  # Fill in
    task_list = [[]]  # Fill in
    if not vectors or not task_list:
        vector_clock_print_usage("Vectors and task_list must be set before running.")
        return

    print(f"t0 {vectors}")
    vector_clock_solve_vector_clocks(vectors, task_list)


SCRIPTS = {
    "berkeley": ("Berkeley clock synchronization", berkeley_main),
    "chord": ("Chord finger table and lookup", chord_main),
    "crypto": ("Crypto system confidentiality/authenticity", crypto_main),
    "diffie-hellman": ("Diffie-Hellman key exchange", diffie_main),
    "greedy": ("Greedy server placement (2 servers)", greedy_main),
    "greedy-fixed": ("Greedy server placement (3 servers)", greedy_fixed_main),
    "lamports": ("Lamport logical clocks", lamports_main),
    "polyring": ("Polymorph polyring routing", polyring_main),
    "read-write": ("Read/write quorum selection", read_write_main),
    "vector-clock": ("Vector clock simulation", vector_clock_main),
}


def print_usage():
    print("Usage:")
    print("  python all.py <script>")
    print("Available scripts:")
    for key, (description, _) in sorted(SCRIPTS.items()):
        print(f"  {key}: {description}")


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in SCRIPTS:
        print_usage()
        return

    SCRIPTS[sys.argv[1]][1]()


if __name__ == "__main__":
    main()
