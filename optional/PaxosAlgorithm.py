"""
Paxos Consensus Algorithm (van Steen/Tanenbaum, Section 8.2)

Paxos is a consensus algorithm that allows a distributed system to
agree on a single value even if some processes fail (crash failures).

Roles:
    - Proposers: Propose values
    - Acceptors: Accept/reject proposals
    - Learners: Learn the decided value

Phases:
    Phase 1a (Prepare): Proposer sends PREPARE(n) with proposal number n.
    Phase 1b (Promise): Acceptors respond with PROMISE if n > any seen number.
    Phase 2a (Accept):  Proposer sends ACCEPT(n, v) if majority promised.
    Phase 2b (Accepted): Acceptors accept if n >= highest promised number.

Key invariant: Once a value is chosen (accepted by majority), 
all future proposals with higher numbers must propose that same value.
"""

from tabulate import tabulate


def print_usage():
    print("""
Usage:
  Simulate a Paxos round with multiple proposers and acceptors.
  Enter the number of acceptors (should be odd for clear majority).
  Enter proposal numbers and values for proposers.
""")


class Acceptor:
    """An acceptor in the Paxos protocol."""
    
    def __init__(self, acceptor_id: int):
        self.id = acceptor_id
        self.promised_n = -1  # Highest proposal number promised
        self.accepted_n = -1  # Proposal number of accepted value
        self.accepted_v = None  # Accepted value
    
    def prepare(self, n: int) -> tuple[bool, int, any]:
        """
        Handle PREPARE(n) request.
        Returns (promise_granted, accepted_n, accepted_v).
        """
        if n > self.promised_n:
            self.promised_n = n
            return True, self.accepted_n, self.accepted_v
        return False, -1, None
    
    def accept(self, n: int, v: any) -> bool:
        """
        Handle ACCEPT(n, v) request.
        Returns True if accepted.
        """
        if n >= self.promised_n:
            self.promised_n = n
            self.accepted_n = n
            self.accepted_v = v
            return True
        return False


def paxos_round(num_acceptors: int, proposal_n: int, proposal_v: any) -> tuple[bool, list[str]]:
    """
    Simulate a single Paxos round.
    
    Args:
        num_acceptors: Number of acceptors.
        proposal_n: Proposal number.
        proposal_v: Proposed value.
    
    Returns:
        Tuple of (value_chosen, list_of_steps).
    """
    steps = []
    acceptors = [Acceptor(i + 1) for i in range(num_acceptors)]
    majority = num_acceptors // 2 + 1
    
    steps.append(f"=== PHASE 1: PREPARE ===")
    steps.append(f"Proposer sends PREPARE({proposal_n}) to all {num_acceptors} acceptors.")
    
    # Phase 1: Prepare
    promises = []
    highest_accepted = (-1, None)
    
    for acc in acceptors:
        ok, acc_n, acc_v = acc.prepare(proposal_n)
        if ok:
            promises.append(acc.id)
            steps.append(f"  Acceptor A{acc.id}: PROMISE (previously accepted: n={acc_n}, v={acc_v})")
            if acc_n > highest_accepted[0]:
                highest_accepted = (acc_n, acc_v)
        else:
            steps.append(f"  Acceptor A{acc.id}: REJECT (already promised higher: {acc.promised_n})")
    
    steps.append(f"\nPromises received: {len(promises)} (majority needed: {majority})")
    
    if len(promises) < majority:
        steps.append("FAILED: Did not receive majority promises.")
        return False, steps
    
    # Determine value to propose (must use highest accepted value if any)
    if highest_accepted[1] is not None:
        final_value = highest_accepted[1]
        steps.append(f"Using previously accepted value: {final_value}")
    else:
        final_value = proposal_v
        steps.append(f"No previously accepted value; using proposed value: {final_value}")
    
    # Phase 2: Accept
    steps.append(f"\n=== PHASE 2: ACCEPT ===")
    steps.append(f"Proposer sends ACCEPT({proposal_n}, {final_value}) to acceptors that promised.")
    
    accepted = []
    for acc in acceptors:
        if acc.id in promises:
            if acc.accept(proposal_n, final_value):
                accepted.append(acc.id)
                steps.append(f"  Acceptor A{acc.id}: ACCEPTED")
            else:
                steps.append(f"  Acceptor A{acc.id}: REJECTED (promised higher)")
    
    steps.append(f"\nAccepts received: {len(accepted)} (majority needed: {majority})")
    
    if len(accepted) >= majority:
        steps.append(f"\n=== VALUE CHOSEN ===")
        steps.append(f"Consensus reached on value: {final_value}")
        return True, steps
    else:
        steps.append("FAILED: Did not receive majority accepts.")
        return False, steps


def main():
    print_usage()
    
    try:
        num_acceptors = int(input("Enter number of acceptors (e.g., 3 or 5): "))
        
        if num_acceptors < 1:
            raise ValueError("Need at least 1 acceptor.")
        
        proposal_n = int(input("Enter proposal number (unique integer): "))
        proposal_v = input("Enter proposed value (any string): ").strip()
        
        print(f"\n--- Paxos Simulation ---")
        print(f"Acceptors: {num_acceptors}")
        print(f"Majority: {num_acceptors // 2 + 1}")
        print(f"Proposal: n={proposal_n}, v='{proposal_v}'")
        
        chosen, steps = paxos_round(num_acceptors, proposal_n, proposal_v)
        
        print("\n--- Protocol Execution ---")
        for step in steps:
            print(step)
        
        if chosen:
            print(f"\n==> Consensus ACHIEVED on value: '{proposal_v}'")
        else:
            print(f"\n==> Consensus FAILED")
            
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
