"""
Vector Clock Simulation

Vector clocks are used to determine the partial ordering of events in a 
distributed system and detect causality violations.

Rules:
1. Before each event (internal, send, or receive), the process increments 
   its own entry in its vector.
2. When sending a message, the process includes its (incremented) vector.
3. Upon receiving a message with vector V_msg, the receiving process:
   a. Updates its own vector: VC[i] = max(VC[i], V_msg[i]) for all i.
   b. Increments its own entry in the updated vector.

Note: Some definitions increment BEFORE sending and AFTER receiving. 
This script follows the standard approach:
- Internal/Send: VC[i]++
- Receive: VC = max(VC, V_msg); VC[i]++
"""

from tabulate import tabulate


def merge_vectors(v_local, v_remote):
    """Update local vector by taking the maximum of each entry."""
    return [max(l, r) for l, r in zip(v_local, v_remote)]


def vector_clock_main():
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                    VECTOR CLOCK SIMULATOR                        ║
║  Track event causality across multiple processes                  ║
╚══════════════════════════════════════════════════════════════════╝

Usage:
  1. Define number of processes (e.g., 3).
  2. Set initial vector states (usually all zeros).
  3. Enter tasks for each time step:
     - Internal Event: "1" (increments RC1)
     - Message: "12" (Process 1 sends to Process 2)
     - Multiple: "1 23 2" (Process 1 event, P2 to P3 msg, P2 event)
""")

    try:
        num_procs = int(input("Number of processes (e.g., 3): "))
        if num_procs < 1:
            raise ValueError("Must have at least 1 process.")

        # Initialize vectors
        vectors = []
        custom_init = input(f"Initialize all to 0? (y/n): ").lower() == 'y'
        if custom_init:
            vectors = [[0] * num_procs for _ in range(num_procs)]
        else:
            for i in range(num_procs):
                v_str = input(f"  Init VC{i+1} (space-separated, e.g., '0 0 0'): ")
                v = [int(x) for x in v_str.strip().split()]
                if len(v) != num_procs:
                    raise ValueError(f"Expected {num_procs} values, got {len(v)}.")
                vectors.append(v)

        num_steps = int(input("\nNumber of time steps (t1 to tN): "))
        
        history = [ [v[:] for v in vectors] ]  # Store t0 state

        for t in range(1, num_steps + 1):
            print(f"\n--- Time Step t{t} ---")
            task_input = input(f"  Enter tasks (e.g., '1' for event in P1, '13' for msg P1->P3): ")
            tasks = task_input.strip().split()
            
            # Create a copy for the next state
            new_vectors = [v[:] for v in vectors]
            
            # To handle multiple simultaneous events in one timestep accurately,
            # we need to be careful. Standard problems usually treat tasks sequentially 
            # within a timestep or assume they don't depend on each other's updates 
            # in the same step.
            
            # We'll process them strictly in the order entered.
            for task in tasks:
                if len(task) == 1: # Internal Event
                    p_idx = int(task) - 1
                    new_vectors[p_idx][p_idx] += 1
                    print(f"  Event in P{p_idx+1}: {new_vectors[p_idx]}")
                elif len(task) == 2: # Message
                    src = int(task[0]) - 1
                    dst = int(task[1]) - 1
                    
                    # 1. Sender increments own clock
                    new_vectors[src][src] += 1
                    v_msg = new_vectors[src][:]
                    print(f"  P{src+1} sends to P{dst+1} with VC: {v_msg}")
                    
                    # 2. Receiver merges and increments
                    new_vectors[dst] = merge_vectors(new_vectors[dst], v_msg)
                    new_vectors[dst][dst] += 1
                    print(f"  P{dst+1} receives and updates to VC: {new_vectors[dst]}")
                else:
                    print(f"  Skipping invalid task: {task}")
            
            vectors = new_vectors
            history.append([v[:] for v in vectors])

        # Final table display
        print("\n" + "="*60)
        print("FINAL VECTOR CLOCK STATES")
        print("="*60)
        
        headers = ["Step"] + [f"VC{i+1}" for i in range(num_procs)]
        table_data = []
        for i, state in enumerate(history):
            row = [f"t{i}"] + [f"({','.join(map(str, v))})" for v in state]
            table_data.append(row)
            
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

    except ValueError as e:
        print(f"Error: {e}")
    except IndexError:
        print(f"Error: Process index out of range.")

if __name__ == "__main__":
    vector_clock_main()
