"""
Test suite for all algorithms in the optional/ folder
"""

print("=" * 60)
print("TESTING ALL OPTIONAL ALGORITHMS")
print("=" * 60)

# Test 1: Cristian's Algorithm
print("\n1. CRISTIAN'S ALGORITHM")
from optional.CristiansAlgorithm import cristians_algorithm
result = cristians_algorithm(100, 110, 200)
print(f"   Input: T_req=100, T_reply=110, T_server=200")
print(f"   Output: estimated_time={result[0]}, RTT={result[1]}, delay={result[2]}")
print(f"   ✓ PASS" if result == (205.0, 10, 5.0) else f"   ✗ FAIL")

# Test 2: NTP Algorithm
print("\n2. NTP ALGORITHM")
from optional.NTPAlgorithm import ntp_algorithm
theta, delta = ntp_algorithm(10, 15, 16, 20)
print(f"   Input: T1=10, T2=15, T3=16, T4=20")
print(f"   Output: θ={theta}, δ={delta}")
print(f"   ✓ PASS" if (theta, delta) == (0.5, 9) else f"   ✗ FAIL")

# Test 3: Bully Algorithm
print("\n3. BULLY ALGORITHM")
from optional.BullyAlgorithm import bully_election
coord, steps = bully_election([1,2,3,4,5], [True,False,True,True,False], 3)
print(f"   Input: processes=[1,2,3,4,5], alive=[T,F,T,T,F], initiator=3")
print(f"   Output: coordinator={coord}")
print(f"   ✓ PASS" if coord == 4 else f"   ✗ FAIL")

# Test 4: Ring Algorithm
print("\n4. RING ALGORITHM")
from optional.RingAlgorithm import ring_election
coord, steps, msg = ring_election([1,3,5,7,2], [True,False,True,True,True], 5)
print(f"   Input: ring=[1,3,5,7,2], alive=[T,F,T,T,T], initiator=5")
print(f"   Output: coordinator={coord}, message={msg}")
print(f"   ✓ PASS" if coord == 7 and msg == [5,7,2,1] else f"   ✗ FAIL")

# Test 5: Two-Phase Commit
print("\n5. TWO-PHASE COMMIT (2PC)")
from optional.TwoPhaseCommit import two_phase_commit
decision, steps = two_phase_commit([True, True, True])
print(f"   Input: votes=[COMMIT, COMMIT, COMMIT]")
print(f"   Output: {decision}")
print(f"   ✓ PASS" if decision == "GLOBAL_COMMIT" else f"   ✗ FAIL")

# Test 6: Three-Phase Commit
print("\n6. THREE-PHASE COMMIT (3PC)")
from optional.ThreePhaseCommit import three_phase_commit
decision, steps = three_phase_commit([True, True, True])
print(f"   Input: votes=[COMMIT, COMMIT, COMMIT]")
print(f"   Output: {decision}")
print(f"   ✓ PASS" if decision == "GLOBAL_COMMIT" else f"   ✗ FAIL")

# Test 7: Paxos
print("\n7. PAXOS CONSENSUS")
from optional.PaxosAlgorithm import paxos_round
chosen, steps = paxos_round(3, 5, 'value_A')
print(f"   Input: acceptors=3, proposal_n=5, value='value_A'")
print(f"   Output: consensus_reached={chosen}")
print(f"   ✓ PASS" if chosen == True else f"   ✗ FAIL")

# Test 8: DNS Resolution
print("\n8. DNS RESOLUTION")
from optional.DNSResolution import iterative_resolution
ip, steps = iterative_resolution('tuwel.tuwien.ac.at')
print(f"   Input: domain='tuwel.tuwien.ac.at'")
print(f"   Output: IP={ip}")
print(f"   ✓ PASS" if ip == "128.130.0.10" else f"   ✗ FAIL")

print("\n" + "=" * 60)
print("ALL TESTS COMPLETED")
print("=" * 60)
