"""
Bully Algorithm - Leader Election (van Steen/Tanenbaum, Section 6.4)

The Bully algorithm elects a coordinator (leader) among a set of processes.
Higher-ID processes "bully" lower-ID ones. When a process notices the
coordinator is down, it initiates an election.

Algorithm:
1. Process P sends ELECTION message to all processes with higher IDs.
2. If no one responds, P wins and becomes coordinator.
3. If a higher-ID process responds with OK, P's job is done (it waits).
4. The higher-ID process then takes over and starts its own election.
5. Eventually, the highest-ID alive process sends COORDINATOR to all.
"""

from tabulate import tabulate


def print_usage():
    print("""
Usage:
  Enter process IDs (space-separated integers).
  Specify which processes are alive (1) or crashed (0).
  Specify which process initiates the election.
""")


def bully_election(processes: list[int], alive: list[bool], initiator: int) -> tuple[int, list[str]]:
    """
    Simulate the Bully algorithm.
    
    Args:
        processes: List of process IDs (sorted ascending).
        alive: List of booleans indicating if each process is alive.
        initiator: The process ID that initiates the election.
    
    Returns:
        Tuple of (elected_coordinator, list_of_steps).
    """
    steps = []
    n = len(processes)
    process_set = set(processes)
    alive_map = {processes[i]: alive[i] for i in range(n)}
    
    if initiator not in process_set:
        return -1, [f"Error: Initiator {initiator} not in process list."]
    
    if not alive_map[initiator]:
        return -1, [f"Error: Initiator {initiator} is crashed and cannot start election."]
    
    # Track which processes are currently running an election
    election_queue = [initiator]
    processed = set()
    
    while election_queue:
        current = election_queue.pop(0)
        if current in processed:
            continue
        processed.add(current)
        
        steps.append(f"Process {current} starts election.")
        
        # Send ELECTION to all higher-ID processes
        higher = [p for p in processes if p > current and alive_map[p]]
        
        if not higher:
            # No higher process alive -> current wins
            steps.append(f"Process {current} receives no OK responses.")
            steps.append(f"Process {current} becomes COORDINATOR and broadcasts to all.")
            return current, steps
        else:
            steps.append(f"Process {current} sends ELECTION to: {higher}")
            # Higher processes respond with OK
            for h in higher:
                steps.append(f"Process {h} responds OK to {current}.")
            # The highest alive process takes over
            steps.append(f"Process {current} waits (a higher process will take over).")
            # Add highest to queue
            election_queue.append(max(higher))
    
    return -1, steps


def main():
    print_usage()
    
    try:
        proc_input = input("Enter process IDs (space-separated, e.g., '1 2 3 4 5'): ")
        processes = sorted([int(x) for x in proc_input.strip().split()])
        
        if len(processes) < 2:
            raise ValueError("Need at least 2 processes.")
        
        print(f"\nProcesses: {processes}")
        
        alive_input = input(f"Enter alive status for each process ({len(processes)} values, 1=alive, 0=crashed): ")
        alive = [x == '1' for x in alive_input.strip().split()]
        
        if len(alive) != len(processes):
            raise ValueError(f"Expected {len(processes)} alive values, got {len(alive)}.")
        
        # Display status table
        table = [[processes[i], "Alive" if alive[i] else "Crashed"] for i in range(len(processes))]
        print("\n" + tabulate(table, headers=["Process ID", "Status"], tablefmt="grid"))
        
        initiator = int(input("\nEnter the process ID that initiates the election: "))
        
        coordinator, steps = bully_election(processes, alive, initiator)
        
        print("\n--- Election Steps ---")
        for i, step in enumerate(steps, 1):
            print(f"{i}. {step}")
        
        if coordinator != -1:
            print(f"\n==> Elected Coordinator: Process {coordinator}")
        else:
            print("\n==> Election failed.")
            
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
