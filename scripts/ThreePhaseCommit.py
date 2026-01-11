"""
Three-Phase Commit (3PC) Protocol (van Steen/Tanenbaum, Section 8.2)

3PC extends 2PC to avoid the blocking problem. It adds a "pre-commit"
phase so participants can recover if the coordinator crashes.

Phase 1 - VOTE REQUEST (same as 2PC):
    1. Coordinator sends VOTE_REQUEST.
    2. Participants vote COMMIT or ABORT.

Phase 2 - PRE-COMMIT (new phase):
    3. If all vote COMMIT, coordinator sends PRE_COMMIT.
    4. Participants acknowledge readiness.

Phase 3 - FINAL COMMIT:
    5. Coordinator sends GLOBAL_COMMIT.
    6. Participants commit and send ACK.

If coordinator crashes after PRE_COMMIT, participants can 
independently decide to commit (they know everyone voted YES).
"""

from tabulate import tabulate


def print_usage():
    print("""
Usage:
  Enter the number of participants.
  Specify each participant's vote: COMMIT (1) or ABORT (0).
  The simulation shows the 3PC protocol execution.
""")


def three_phase_commit(votes: list[bool]) -> tuple[str, list[str]]:
    """
    Simulate the Three-Phase Commit protocol.
    
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
    
    # Check votes
    if not all(votes):
        decision = "GLOBAL_ABORT"
        abort_participants = [f"P{i+1}" for i, v in enumerate(votes) if not v]
        steps.append(f"\nParticipant(s) {', '.join(abort_participants)} voted ABORT.")
        steps.append(f"Coordinator decides: {decision}")
        steps.append(f"Coordinator sends {decision} to all participants.")
        for i in range(n):
            steps.append(f"  Participant P{i+1} aborts the transaction.")
        return decision, steps
    
    # Phase 2: PRE-COMMIT (all voted COMMIT)
    steps.append("")
    steps.append("=== PHASE 2: PRE-COMMIT ===")
    steps.append("All participants voted COMMIT.")
    steps.append("Coordinator sends PRE_COMMIT to all participants.")
    
    for i in range(n):
        steps.append(f"  Participant P{i+1} acknowledges PRE_COMMIT (now in 'Prepared to Commit' state).")
    
    steps.append("")
    steps.append("Coordinator receives all ACKs for PRE_COMMIT.")
    steps.append("(If coordinator crashes now, participants can independently decide to COMMIT)")
    
    # Phase 3: GLOBAL COMMIT
    steps.append("")
    steps.append("=== PHASE 3: GLOBAL COMMIT ===")
    decision = "GLOBAL_COMMIT"
    steps.append(f"Coordinator sends {decision} to all participants.")
    
    for i in range(n):
        steps.append(f"  Participant P{i+1} commits the transaction.")
    
    # Final ACKs
    steps.append("")
    steps.append("=== ACKNOWLEDGMENT ===")
    for i in range(n):
        steps.append(f"  Participant P{i+1} sends final ACK.")
    steps.append("Coordinator: Transaction complete.")
    
    return decision, steps


def compare_2pc_3pc():
    """Show comparison between 2PC and 3PC."""
    print("\n--- 2PC vs 3PC Comparison ---")
    table = [
        ["Phases", "2 (Vote, Commit)", "3 (Vote, Pre-Commit, Commit)"],
        ["Blocking?", "Yes (if coordinator crashes)", "No (participants can recover)"],
        ["Messages", "3n (Vote+Commit+ACK)", "4n (Vote+PreCommit+Commit+ACK)"],
        ["Use case", "General transactions", "High-availability systems"],
    ]
    print(tabulate(table, headers=["Property", "2PC", "3PC"], tablefmt="grid"))


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
        
        decision, steps = three_phase_commit(votes)
        
        print("\n--- 3PC Protocol Execution ---")
        for step in steps:
            print(step)
        
        print(f"\n==> Final Decision: {decision}")
        
        compare_2pc_3pc()
            
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
