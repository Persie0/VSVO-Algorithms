"""
Ring Algorithm - Leader Election (van Steen/Tanenbaum, Section 6.4)

In the Ring algorithm, processes are organized in a logical ring.
When a process notices the coordinator is down, it initiates an election
by sending an ELECTION message around the ring.

Algorithm:
1. Process P sends ELECTION message containing its ID to successor.
2. Each alive process adds its ID to the message and forwards it.
3. When the message returns to initiator, it picks the highest ID as leader.
4. A COORDINATOR message is then circulated to announce the winner.
"""

from tabulate import tabulate


def print_usage():
    print("""
Usage:
  Enter process IDs (space-separated integers) in ring order.
  Specify which processes are alive (1) or crashed (0).
  Specify which process initiates the election.
""")


def ring_election(processes: list[int], alive: list[bool], initiator: int) -> tuple[int, list[str], list[int]]:
    """
    Simulate the Ring election algorithm.
    
    Args:
        processes: List of process IDs in ring order.
        alive: List of booleans indicating if each process is alive.
        initiator: The process ID that initiates the election.
    
    Returns:
        Tuple of (elected_coordinator, list_of_steps, election_message_contents).
    """
    steps = []
    n = len(processes)
    
    try:
        init_idx = processes.index(initiator)
    except ValueError:
        return -1, [f"Error: Initiator {initiator} not in ring."], []
    
    if not alive[init_idx]:
        return -1, [f"Error: Initiator {initiator} is crashed."], []
    
    # Phase 1: ELECTION message travels around the ring
    election_list = [initiator]
    steps.append(f"Process {initiator} starts election with message: {election_list}")
    
    current_idx = (init_idx + 1) % n
    visited = 0  # Safety counter to prevent infinite loops
    
    while current_idx != init_idx and visited < n:
        proc_id = processes[current_idx]
        
        if alive[current_idx]:
            election_list.append(proc_id)
            steps.append(f"Process {proc_id} adds itself -> message: {election_list}")
        else:
            steps.append(f"Process {proc_id} is crashed, skipping to next.")
        
        current_idx = (current_idx + 1) % n
        visited += 1
    
    # Message returned to initiator
    steps.append(f"Message returns to initiator {initiator}.")
    
    # Phase 2: Determine coordinator (highest ID in the list)
    coordinator = max(election_list)
    steps.append(f"Highest ID in message: {coordinator}")
    
    # Phase 3: COORDINATOR message circulated
    steps.append(f"Process {initiator} sends COORDINATOR({coordinator}) around the ring.")
    
    current_idx = (init_idx + 1) % n
    visited = 0
    while current_idx != init_idx and visited < n:
        proc_id = processes[current_idx]
        if alive[current_idx]:
            steps.append(f"Process {proc_id} receives COORDINATOR({coordinator}).")
        current_idx = (current_idx + 1) % n
        visited += 1
    
    return coordinator, steps, election_list


def main():
    print_usage()
    
    try:
        proc_input = input("Enter process IDs in ring order (space-separated, e.g., '1 3 5 7 2'): ")
        processes = [int(x) for x in proc_input.strip().split()]
        
        if len(processes) < 2:
            raise ValueError("Need at least 2 processes.")
        
        print(f"\nRing order: {' -> '.join(map(str, processes))} -> {processes[0]} (cycle)")
        
        alive_input = input(f"Enter alive status for each process ({len(processes)} values, 1=alive, 0=crashed): ")
        alive = [x == '1' for x in alive_input.strip().split()]
        
        if len(alive) != len(processes):
            raise ValueError(f"Expected {len(processes)} alive values, got {len(alive)}.")
        
        # Display status table
        table = [[processes[i], "Alive" if alive[i] else "Crashed"] for i in range(len(processes))]
        print("\n" + tabulate(table, headers=["Process ID", "Status"], tablefmt="grid"))
        
        initiator = int(input("\nEnter the process ID that initiates the election: "))
        
        coordinator, steps, election_list = ring_election(processes, alive, initiator)
        
        print("\n--- Election Steps ---")
        for i, step in enumerate(steps, 1):
            print(f"{i}. {step}")
        
        if coordinator != -1:
            print(f"\n==> Election List: {election_list}")
            print(f"==> Elected Coordinator: Process {coordinator}")
        else:
            print("\n==> Election failed.")
            
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
