from datetime import timedelta

USAGE = """Usage:
  Provide numeric inputs when prompted:
  - How many servers? (integer >= 1)
  - Each server time as HHMM (e.g., 1530 for 3:30 pm)
  - Time Daemon index within range 0..N-1
"""


class Server:
    def __init__(self, name, time):
        self.name = name
        self.time = timedelta(
            hours=int(time[:len(time) // 2]),
            minutes=int(time[len(time) // 2:])
        ).total_seconds()
        self.time_daemon = False


def print_usage(message="Invalid input."):
    print(message)
    print(USAGE)


def parse_time_input(value):
    if not value.isdigit() or len(value) % 2 != 0:
        raise ValueError("Time must be digits in HHMM format.")
    return value


def start_app():
    servers = []
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    # Input-format example: for 3:30 pm = 1530
    server_count = int(input("How many servers? "))
    if server_count < 1:
        raise ValueError("Server count must be at least 1.")
    for i in range(server_count):
        s = parse_time_input(input(f"Server {letters[i]}: "))
        servers.append(Server(f"Server {letters[i]}", s))
    while True:
        print(f"\nWhich server is the time daemon? Range: 0-{len(servers) - 1}")
        time_daemon = int(input("Time Daemon: "))
        if time_daemon < 0 or time_daemon >= len(servers):
            print("Invalid input")
        else:
            servers[time_daemon].time_daemon = True
            break
    return servers, servers[time_daemon]


def convert_seconds(time, show_sign=False):
    sign = ""
    if time < 0:
        sign = "-"
        time = abs(time)
    elif show_sign:
        sign = "+"
    
    m, s = divmod(int(time), 60)
    h, m = divmod(m, 60)
    
    if h > 0:
        return f"{sign}{h:02d}:{m:02d}"
    return f"{sign}00:{m:02d}"


def round_one(servers, time_daemon):
    print("\nRound 1")
    for s in servers:
        print(f"{time_daemon.name} to {s.name}: {convert_seconds(time_daemon.time)}")


def round_two(servers, time_daemon):
    print("\nRound 2")
    differences = []
    for s in servers:
        diff = s.time - time_daemon.time
        print(f"{s.name} to {time_daemon.name}: {convert_seconds(diff, show_sign=True)}")
        differences.append(diff)
    return differences


def round_three(servers, time_differences, time_daemon):
    print("\nRound 3")
    avg = sum(time_differences) / len(time_differences)
    for s in servers:
        diff = time_daemon.time + avg - s.time
        print(f"{time_daemon.name} to {s.name}: {convert_seconds(diff, show_sign=True)} | Final Time: {convert_seconds(s.time + diff)}")


def main():
    try:
        network_servers, time_daemon = start_app()
    except ValueError as exc:
        print_usage(str(exc))
        return

    round_one(network_servers, time_daemon)
    time_differences = round_two(network_servers, time_daemon)
    round_three(network_servers, time_differences, time_daemon)


if __name__ == '__main__':
    main()
