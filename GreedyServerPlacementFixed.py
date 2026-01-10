from tabulate import tabulate

num_latencies = int(input("Enter the number of latencies per client: "))
num_clients = int(input("Enter the number of clients: "))
options = [[0 for _ in range(num_latencies)] for _ in range(num_clients)]

# ---- INPUT ----
for i in range(num_clients):
    for j in range(num_latencies):
        latency = int(input(f"Enter latency for client {i + 1}, latency {j + 1}: "))
        options[i][j] = latency   # FIX: index vertauscht

# ---- TABLE ----
headers = [""] + [f"L{j + 1}" for j in range(num_latencies)]
table = [[f"C{i + 1}"] + options[i] for i in range(num_clients)]
print(tabulate(table, headers, tablefmt="grid"))

# ---- TOTAL LATENCY PER SERVER (column sums) ----
total_latencies = {
    j + 1: sum(options[i][j] for i in range(num_clients))
    for j in range(num_latencies)
}

# ---- FIRST SERVER ----
first_server = min(total_latencies.items(), key=lambda x: x[1])
first_idx = first_server[0] - 1

# ---- SECOND SERVER ----
minimum = {}
for j in range(num_latencies):
    if j != first_idx:
        curr = [min(options[i][j], options[i][first_idx]) for i in range(num_clients)]
        minimum[j + 1] = curr

second_server = min(minimum.items(), key=lambda x: sum(x[1]))
second_idx = second_server[0] - 1

# ---- THIRD SERVER (NEU, minimal) ----
third_candidates = {}
for j in range(num_latencies):
    if j not in (first_idx, second_idx):
        curr = [
            min(
                options[i][j],
                second_server[1][i]   # bereits bestes Ergebnis aus Server 1+2
            )
            for i in range(num_clients)
        ]
        third_candidates[j + 1] = curr

third_server = min(third_candidates.items(), key=lambda x: sum(x[1]))

# ---- OUTPUT ----
print(f"First Server to select: L{first_server[0]}")
print(f"Second Server to select: L{second_server[0]}")
print(f"Third Server to select: L{third_server[0]}")
print(f"Total Latency of the solution: {sum(third_server[1])}")

print("-------------------------")
print("Servers selected in descending order of total latency:")
for server, latency in sorted(total_latencies.items(), key=lambda x: x[1], reverse=True):
    print(f"Server L{server}: Total Latency = {latency}")
