"""
NTP Algorithm - Clock Synchronization (van Steen/Tanenbaum, Section 6.1)

The Network Time Protocol (NTP) uses four timestamps to calculate
the clock offset and round-trip delay between client and server.

Timestamps:
    T1 = Client sends request (client clock)
    T2 = Server receives request (server clock)
    T3 = Server sends reply (server clock)
    T4 = Client receives reply (client clock)

Formulas:
    Offset (θ) = ((T2 - T1) + (T3 - T4)) / 2
    Delay (δ)  = (T4 - T1) - (T3 - T2)

The offset θ tells you how much to adjust the client clock.
Positive θ means client is behind; negative θ means client is ahead.
"""


def print_usage():
    print("""
Usage:
  Enter the four NTP timestamps:
    T1 = Time client sends request (client clock)
    T2 = Time server receives request (server clock)
    T3 = Time server sends reply (server clock)
    T4 = Time client receives reply (client clock)
  All times should be in the same unit (e.g., seconds).
""")


def ntp_algorithm(t1: float, t2: float, t3: float, t4: float) -> tuple[float, float]:
    """
    Calculate clock offset and round-trip delay using NTP algorithm.
    
    Args:
        t1: Client request send time (client clock).
        t2: Server request receive time (server clock).
        t3: Server reply send time (server clock).
        t4: Client reply receive time (client clock).
    
    Returns:
        Tuple of (offset_theta, delay_delta).
    """
    # Offset: how much to adjust client clock
    theta = ((t2 - t1) + (t3 - t4)) / 2
    
    # Round-trip delay (excluding server processing time)
    delta = (t4 - t1) - (t3 - t2)
    
    return theta, delta


def main():
    print_usage()
    
    try:
        t1 = float(input("Enter T1 (client sends request): "))
        t2 = float(input("Enter T2 (server receives request): "))
        t3 = float(input("Enter T3 (server sends reply): "))
        t4 = float(input("Enter T4 (client receives reply): "))
        
        theta, delta = ntp_algorithm(t1, t2, t3, t4)
        
        print("\n--- NTP Algorithm Results ---")
        print(f"T1 (client -> server): {t1}")
        print(f"T2 (server receives):  {t2}")
        print(f"T3 (server -> client): {t3}")
        print(f"T4 (client receives):  {t4}")
        
        print(f"\n--- Calculations ---")
        print(f"(T2 - T1) = {t2} - {t1} = {t2 - t1}")
        print(f"(T3 - T4) = {t3} - {t4} = {t3 - t4}")
        print(f"θ = ((T2-T1) + (T3-T4)) / 2 = ({t2-t1} + {t3-t4}) / 2 = {theta}")
        
        print(f"\n(T4 - T1) = {t4} - {t1} = {t4 - t1}")
        print(f"(T3 - T2) = {t3} - {t2} = {t3 - t2}")
        print(f"δ = (T4-T1) - (T3-T2) = {t4-t1} - {t3-t2} = {delta}")
        
        print(f"\n==> Offset (θ): {theta:+}")
        if theta > 0:
            print("    Client clock is BEHIND server; advance client clock.")
        elif theta < 0:
            print("    Client clock is AHEAD of server; slow down client clock.")
        else:
            print("    Clocks are synchronized.")
        
        print(f"\n==> Round-trip Delay (δ): {delta}")
        print(f"    Network propagation time (both ways): {delta}")
        print(f"    Server processing time: {t3 - t2}")
        
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
