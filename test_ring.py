from scripts.RingAlgorithm import ring_election

# Test: Ring with 5 processes, one crashed
processes = [1, 3, 5, 7, 2]
alive = [True, False, True, True, True]  # Process 3 is crashed
initiator = 5

coord, steps, msg = ring_election(processes, alive, initiator)
print(f"Coordinator: {coord}")
print(f"Election message: {msg}")
