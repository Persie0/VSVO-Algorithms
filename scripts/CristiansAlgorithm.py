"""
Cristian's Algorithm - Clock Synchronization (van Steen/Tanenbaum, Section 6.1)

Cristian's algorithm synchronizes a client's clock with a time server.
The client requests the time and adjusts for network delay.

Formula:
    T_client = T_server + RTT/2

Where:
    T_server = Time received from server
    RTT = Round-Trip Time (T_reply - T_request)

The accuracy is bounded by: ± (RTT/2 - min_one_way_delay)
"""


def print_usage():
    print("""
Usage:
  Enter the time when the request was sent (T_request).
  Enter the time when the reply was received (T_reply).
  Enter the server time included in the reply (T_server).
  All times should be in the same unit (e.g., seconds or milliseconds).
""")


def cristians_algorithm(t_request: float, t_reply: float, t_server: float) -> tuple[float, float, float]:
    """
    Calculate the estimated current time using Cristian's algorithm.
    
    Args:
        t_request: Local time when request was sent.
        t_reply: Local time when reply was received.
        t_server: Server time included in the reply.
    
    Returns:
        Tuple of (estimated_time, rtt, one_way_delay_estimate).
    """
    rtt = t_reply - t_request
    one_way_delay = rtt / 2
    estimated_time = t_server + one_way_delay
    
    return estimated_time, rtt, one_way_delay


def main():
    print_usage()
    
    try:
        t_request = float(input("Enter T_request (time when request was sent): "))
        t_reply = float(input("Enter T_reply (time when reply was received): "))
        t_server = float(input("Enter T_server (server time in the reply): "))
        
        if t_reply < t_request:
            raise ValueError("T_reply must be >= T_request.")
        
        estimated_time, rtt, one_way_delay = cristians_algorithm(t_request, t_reply, t_server)
        
        print("\n--- Cristian's Algorithm Results ---")
        print(f"T_request (client):     {t_request}")
        print(f"T_reply (client):       {t_reply}")
        print(f"T_server (from server): {t_server}")
        print(f"RTT:                    {rtt}")
        print(f"Estimated one-way delay: {one_way_delay}")
        print(f"\n==> Estimated Current Time: {estimated_time}")
        print(f"    (T_server + RTT/2 = {t_server} + {one_way_delay} = {estimated_time})")
        
        # Calculate clock adjustment
        current_client_time = t_reply
        adjustment = estimated_time - current_client_time
        print(f"\n==> Clock Adjustment: {adjustment:+}")
        if adjustment > 0:
            print("    (Client clock is behind; advance it)")
        elif adjustment < 0:
            print("    (Client clock is ahead; slow it down)")
        else:
            print("    (Clocks are synchronized)")
            
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
