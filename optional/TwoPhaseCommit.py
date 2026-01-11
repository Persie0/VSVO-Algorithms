"""
Two-Phase Commit (2PC) Protocol (van Steen/Tanenbaum, Section 8.2/8.3)

The Two-Phase Commit protocol ensures atomic commitment across
distributed participants. Either all commit or all abort.

Phase 1 - VOTE REQUEST (Prepare):
    1. Coordinator sends VOTE_REQUEST to all participants.
    2. Each participant votes COMMIT (ready) or ABORT (not ready).

Phase 2 - DECISION:
    3a. If ALL participants vote COMMIT -> Coordinator sends GLOBAL_COMMIT.
    3b. If ANY participant votes ABORT -> Coordinator sends GLOBAL_ABORT.
    4. Participants acknowledge and execute the decision.

Blocking Problem: If coordinator crashes after Phase 1, participants
are blocked waiting for the decision.
"""

from tabulate import tabulate


def print_usage():
    print("""
Usage:
  Enter the number of participants.
  Specify each participant's vote: COMMIT (1) or ABORT (0).
  The simulation shows the 2PC protocol execution.
""")


def two_phase_commit(votes: list[bool]) -> tuple[str, list[str]]:
    """
    Simulate the Two-Phase Commit protocol.
    
    Args:
        votes: List of participant votes (True = COMMIT, False = ABORT).
    
    Returns:
        Tuple of (final_decision, list_of_steps).
    """
    steps = []
    n = len(votes)
    
    # Phase 1: VOTE REQUEST
    steps.append("=== PHASE 1: VOTE REQUEST ===")
    steps.append("Coordinator sends VOTE_REQUEST to all participants.")
    
    for i, vote in enumerate(votes):
        vote_str = "COMMIT" if vote else "ABORT"
        steps.append(f"  Participant P{i+1} votes: {vote_str}")
    
    # Phase 2: DECISION
    steps.append("")
    steps.append("=== PHASE 2: DECISION ===")
    
    if all(votes):
        decision = "GLOBAL_COMMIT"
        steps.append("All participants voted COMMIT.")
        steps.append(f"Coordinator decides: {decision}")
        steps.append(f"Coordinator sends {decision} to all participants.")
        for i in range(n):
            steps.append(f"  Participant P{i+1} commits the transaction.")
    else:
        decision = "GLOBAL_ABORT"
        abort_participants = [f"P{i+1}" for i, v in enumerate(votes) if not v]
        steps.append(f"Participant(s) {', '.join(abort_participants)} voted ABORT.")
        steps.append(f"Coordinator decides: {decision}")
        steps.append(f"Coordinator sends {decision} to all participants.")
        for i in range(n):
            steps.append(f"  Participant P{i+1} aborts the transaction.")
    
    steps.append("")
    steps.append("=== ACKNOWLEDGMENT ===")
    for i in range(n):
        steps.append(f"  Participant P{i+1} sends ACK to Coordinator.")
    steps.append("Coordinator: Transaction complete.")
    
    return decision, steps


def main():
    print_usage()
    
    try:
        n = int(input("Enter number of participants: "))
        
        if n < 1:
            raise ValueError("Need at least 1 participant.")
        
        vote_input = input(f"Enter votes for {n} participants (1=COMMIT, 0=ABORT, space-separated): ")
        votes = [x == '1' for x in vote_input.strip().split()]
        
        if len(votes) != n:
            raise ValueError(f"Expected {n} votes, got {len(votes)}.")
        
        # Display vote table
        table = [[f"P{i+1}", "COMMIT" if votes[i] else "ABORT"] for i in range(n)]
        print("\n" + tabulate(table, headers=["Participant", "Vote"], tablefmt="grid"))
        
        decision, steps = two_phase_commit(votes)
        
        print("\n--- 2PC Protocol Execution ---")
        for step in steps:
            print(step)
        
        print(f"\n==> Final Decision: {decision}")
        
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
