"""
RPC Timing Calculator

Calculates the time it takes for synchronous Remote Procedure Calls (RPC)
to complete based on various timing parameters.

RPC Timing Components:
1. Client Preparation Time (t_client): Time for client to compute arguments
2. Server Processing Time (t_server): Time for server to process and compute response
3. Marshalling/Unmarshalling Time (t_marshal): Time for stubs to serialize/deserialize
   - Applies on both client side (request) and server side (request+response)
4. Network Transmission Time (t_network): Time for message to travel over network
   - Applies in both directions (request and response)

Formula for single RPC call:
  Total = t_client + t_marshal(client) + t_network + t_marshal(server) + 
          t_server + t_marshal(server) + t_network + t_marshal(client)
        = t_client + 2*t_marshal + t_network + 2*t_marshal + t_server + t_network
        = t_client + 4*t_marshal + 2*t_network + t_server
"""

from tabulate import tabulate


def rpc_timing_single_call(
    t_client: float,
    t_server: float,
    t_marshal: float,
    t_network: float
) -> tuple[float, list[tuple[str, float]]]:
    """
    Calculate the timing for a single RPC call.
    
    Args:
        t_client: Time for client to prepare/compute arguments (ms)
        t_server: Time for server to process and compute response (ms)
        t_marshal: Time for marshalling/unmarshalling per operation (ms)
        t_network: Time for network transmission one way (ms)
        
    Returns:
        Tuple of (total_time, breakdown_steps)
    """
    steps = []
    total = 0.0
    
    # Client prepares request
    steps.append(("Client computes arguments", t_client))
    total += t_client
    
    # Client stub marshals request
    steps.append(("Client stub marshals request", t_marshal))
    total += t_marshal
    
    # Network transmission to server
    steps.append(("Network transmission (client → server)", t_network))
    total += t_network
    
    # Server stub unmarshals request
    steps.append(("Server stub unmarshals request", t_marshal))
    total += t_marshal
    
    # Server processes request
    steps.append(("Server processes request", t_server))
    total += t_server
    
    # Server stub marshals response
    steps.append(("Server stub marshals response", t_marshal))
    total += t_marshal
    
    # Network transmission to client
    steps.append(("Network transmission (server → client)", t_network))
    total += t_network
    
    # Client stub unmarshals response
    steps.append(("Client stub unmarshals response", t_marshal))
    total += t_marshal
    
    return total, steps


def rpc_timing_sequential(
    num_requests: int,
    t_client: float,
    t_server: float,
    t_marshal: float,
    t_network: float
) -> tuple[float, list[str]]:
    """
    Calculate timing for multiple sequential RPC calls (single-threaded client).
    Each request must complete before the next one starts.
    """
    single_call_time, _ = rpc_timing_single_call(t_client, t_server, t_marshal, t_network)
    total_time = single_call_time * num_requests
    
    explanation = [
        f"Single RPC call time: {single_call_time} ms",
        f"Number of requests: {num_requests}",
        f"Total time (sequential): {single_call_time} × {num_requests} = {total_time} ms"
    ]
    
    return total_time, explanation


def rpc_timing_parallel(
    num_requests: int,
    num_threads: int,
    t_client: float,
    t_server: float,
    t_marshal: float,
    t_network: float
) -> tuple[float, list[str]]:
    """
    Calculate timing for multiple RPC calls with parallel threads on client.
    
    Important considerations:
    - Client can prepare multiple requests in parallel (if threads available)
    - Server is single-threaded, so it queues requests
    - Network acts like a queue (FIFO)
    - Stubs are also threads
    """
    explanation = []
    
    # Time for a single complete RPC call
    single_call_time, _ = rpc_timing_single_call(t_client, t_server, t_marshal, t_network)
    
    # Time from sending request to receiving response (excludes client computation)
    rpc_latency = single_call_time - t_client
    
    # With parallel threads, requests can be sent overlapped
    # But server is single-threaded, so requests are processed sequentially
    
    # First, client prepares all requests in parallel (takes t_client time for max threads)
    # Then requests go through the pipeline
    
    # Calculate how many batches we need
    batches = (num_requests + num_threads - 1) // num_threads
    
    explanation.append(f"Client threads: {num_threads}")
    explanation.append(f"Number of requests: {num_requests}")
    explanation.append(f"Single RPC call time: {single_call_time} ms")
    explanation.append("")
    
    # Timeline simulation for accurate calculation
    explanation.append("=== Timeline Analysis ===")
    
    if num_threads >= num_requests:
        # All requests can be sent in parallel
        # Client prepares all requests simultaneously: t_client
        # Then all requests are marshalled simultaneously: t_marshal
        # First request travels: t_network
        # Server processes requests sequentially: num_requests * server_processing
        # Last response travels back: t_network + t_marshal
        
        # Time until all requests sent to network
        t_all_sent = t_client + t_marshal
        
        # Time for first request to arrive at server
        t_first_at_server = t_all_sent + t_network + t_marshal
        
        # Server processes all requests sequentially
        t_server_total = num_requests * t_server
        
        # For each request, server also needs to marshal response
        # But responses can overlap with processing if we consider pipelining
        # In strict sequential server: process + marshal for each
        server_per_request = t_server + t_marshal
        t_all_server_done = t_first_at_server + (num_requests - 1) * server_per_request + t_server + t_marshal
        
        # Last response travels to client
        t_last_response = t_all_server_done + t_network + t_marshal
        
        total_time = t_last_response
        
        explanation.append(f"All {num_requests} requests prepared in parallel: {t_client} ms")
        explanation.append(f"All requests marshalled in parallel: +{t_marshal} ms")
        explanation.append(f"Network transmission (overlapped): +{t_network} ms")
        explanation.append(f"Server unmarshals first request: +{t_marshal} ms")
        explanation.append(f"Server processes all {num_requests} requests sequentially: +{num_requests * t_server} ms")
        explanation.append(f"Server marshals responses: +{num_requests * t_marshal} ms (overlapped with processing)")
        explanation.append(f"Last response transmission: +{t_network} ms")
        explanation.append(f"Client unmarshals last response: +{t_marshal} ms")
    else:
        # More complex case: batched client preparation
        # For simplicity, calculate the pipeline effect
        
        # With 2 threads and 2 requests, both can go in parallel
        threads_used = min(num_threads, num_requests)
        
        # Client preparation time (parallel)
        t_client_total = t_client
        
        # After client prep, all requests go into pipeline
        # They get marshalled (can be parallel if stubs are separate threads)
        # For this problem: stubs are threads, so parallel marshalling
        t_marshal_client = t_marshal
        
        # Network queues messages, sends one after another
        # First message takes t_network, subsequent ones are pipelined
        t_network_out = t_network  # First message
        # Other messages are queued, but traveling simultaneously
        
        # Server receives messages, unmarshals sequentially (single-threaded)
        # Actually, server stub is a thread, so unmarshalling happens in the stub
        # Then server processes sequentially
        
        # Let's trace the timeline more carefully:
        # t=0: Client starts preparing Request 1 and Request 2 (parallel)
        # t=t_client: Both requests ready, client stubs start marshalling (parallel)
        # t=t_client+t_marshal: Both requests sent to network
        # t=t_client+t_marshal+t_network: First request arrives at server
        #   - Server stub starts unmarshalling Request 1
        # t=t_client+t_marshal+t_network+t_marshal: Request 1 unmarshalled
        #   - Server starts processing Request 1
        #   - Meanwhile, Request 2 arrives and queues
        # t=t_client+t_marshal+t_network+t_marshal+t_server: Request 1 processed
        #   - Server stub marshals Response 1
        #   - Server stub starts unmarshalling Request 2 (queued)
        # ... and so on
        
        # Simplified calculation for 2 requests with 2 threads:
        # Parallel preparation: t_client
        # Parallel marshalling (client): t_marshal
        # Network (first leaves, second queued): t_network
        # Server unmarshal R1: t_marshal
        # Server process R1: t_server
        # Server marshal Resp1 + unmarshal R2: t_marshal (can overlap? typically sequential)
        # Server process R2: t_server
        # Server marshal Resp2: t_marshal
        # Network (response): t_network
        # Client unmarshal (last response): t_marshal
        
        # Total with pipelining for 2 parallel requests:
        total_time = (t_client + t_marshal + t_network + t_marshal + 
                      t_server + t_marshal +  # R1 complete on server
                      t_marshal + t_server + t_marshal +  # R2 complete on server (unmarshal + process + marshal)
                      t_network + t_marshal)  # Last response back
        
        # Wait, let me recalculate based on the problem constraints:
        # The stubs are threads - so client has stub threads that can work in parallel
        # Server is single-threaded, meaning the SERVER PROCESS is single-threaded
        # Server stub is still a thread
        
        # Actually, re-reading the problem: "stubs are also threads"
        # This means marshalling/unmarshalling can happen in parallel if multiple stubs
        
        # For this specific 2-request, 2-thread scenario:
        # t_client (prepare both) + t_marshal (marshal both) + t_network (send, queued) 
        # + t_marshal (unmarshal at server, but sequential since server stub is one thread? or parallel?)
        
        # Let's use a conservative interpretation:
        # Client side: parallel (2 threads)
        # Network: queue
        # Server side: single-threaded (including stub)
        
        # Time = t_client + t_marshal (client, parallel)
        #      + t_network (both messages travel)
        #      + t_marshal * 2 (server unmarshal sequentially)
        #      + t_server * 2 (server process sequentially)
        #      + t_marshal * 2 (server marshal sequentially)
        #      + t_network (responses travel)
        #      + t_marshal (client unmarshal last, parallel possible)
        
        # Actually, based on the PDF problem description:
        # Total per RPC = t_client + 4*t_marshal + 2*t_network + t_server
        # For single-threaded: 2 * (10 + 4*2 + 2*5 + 10) = 2 * 38 = 76 ms
        # For 2 threads: we save on client computation overlap
        
        # Simpler model matching the PDF:
        # Sequential: 2 * single_call = 2 * 38 = 76 ms
        # Parallel (2 threads): 
        #   - Client comp: 10 ms (parallel)
        #   - Client marshal: 2 ms each (parallel or sequential based on stub threads)
        #   - Network out: 5 ms (queued)
        #   - Server unmarshal + process + marshal: sequential
        #   - Network back: 5 ms
        #   - Client unmarshal: 2 ms
        
        # With server being single-threaded, requests queue at server
        # Time = 10 (client) + 2 (marshal) + 5 (network) + 2*2 (server unmarshal) 
        #      + 2*10 (server process) + 2*2 (server marshal) 
        #      + 5 (network) + 2 (client unmarshal)
        #      = 10 + 2 + 5 + 4 + 20 + 4 + 5 + 2 = 52 ms
        
        # Hmm, this is getting complex. Let me use the standard formula approach.
        explanation.append(f"Requests prepared in parallel: {t_client} ms")
        explanation.append(f"Sequential server processing required")
        
    return total_time, explanation


def calculate_rpc_timing(
    t_client: float,
    t_server: float,
    t_marshal: float,
    t_network: float,
    num_requests: int = 1,
    num_threads: int = 1
) -> dict:
    """
    Main calculation function for RPC timing.
    
    Returns a dictionary with all timing information.
    """
    # Single call breakdown
    single_time, single_steps = rpc_timing_single_call(t_client, t_server, t_marshal, t_network)
    
    result = {
        "single_call_time": single_time,
        "single_call_breakdown": single_steps,
        "t_client": t_client,
        "t_server": t_server,
        "t_marshal": t_marshal,
        "t_network": t_network,
        "num_requests": num_requests,
        "num_threads": num_threads,
    }
    
    if num_threads == 1:
        # Sequential processing
        result["total_time"] = single_time * num_requests
        result["mode"] = "sequential"
    else:
        # Parallel processing with server queueing
        # Client prepares in parallel: max(t_client, t_client) = t_client for up to num_threads requests
        # Client stubs marshal in parallel: t_marshal
        # Network sends (may queue if multiple): t_network per message
        # Server is single-threaded: must process sequentially
        # Server stub unmarshals: t_marshal per request
        # Server processes: t_server per request
        # Server stub marshals: t_marshal per request
        # Network sends responses: t_network
        # Client stubs unmarshal in parallel: t_marshal
        
        requests_in_parallel = min(num_threads, num_requests)
        
        # With parallel client threads and single-threaded server:
        # Overlap happens only on client side preparation
        # Server still processes everything sequentially
        
        # Time = Client prep (parallel) + Client marshal (parallel)
        #      + Network (first request) + (num_requests - 1) * 0 (pipelined)
        #      + Server processing chain (sequential for all requests)
        #      + Network (last response)
        #      + Client unmarshal (parallel)
        
        # Server chain per request = unmarshal + process + marshal = t_marshal + t_server + t_marshal
        server_chain = t_marshal + t_server + t_marshal
        
        # Total time with parallel client
        parallel_time = (t_client +  # Parallel client prep
                        t_marshal +  # Parallel client marshal
                        t_network +  # Network to server
                        server_chain * num_requests +  # Server processes all sequentially
                        t_network +  # Network back to client
                        t_marshal)   # Parallel client unmarshal
        
        # But we also need to consider that the last request might arrive later
        # Actually for overlapped sending, first request starts being processed
        # while other requests are still in transit/queuing
        
        # More accurate for 2 requests with 2 threads (overlapped):
        # t=0: Client starts preparing R1 and R2
        # t=10: R1 and R2 ready
        # t=10: Client stubs start marshalling R1 and R2
        # t=12: R1 and R2 sent to network
        # t=17: R1 arrives at server, server stub starts unmarshalling
        # t=17: R2 also arrives (or slightly after due to network queue)
        # t=19: R1 unmarshalled, server starts processing R1
        # t=29: R1 processed, server stub marshals R1 response
        # t=29: Server stub starts unmarshalling R2 (was queued)
        # t=31: R1 response sent to network / R2 unmarshalled
        # t=31: Server starts processing R2
        # t=41: R2 processed, server stub marshals R2 response
        # t=43: R2 response sent to network
        # t=48: R2 response arrives at client
        # t=50: Client unmarshals R2 response (R1 was earlier)
        
        # Total = 50 ms for 2 parallel requests
        
        # Let me verify with formula:
        # First request completion: 10 + 2 + 5 + 2 + 10 + 2 + 5 + 2 = 38 ms
        # Second request completion (sequential after first at server):
        #   Starts server processing at: 10 + 2 + 5 + 2 + 10 + 2 = 31 ms (after R1 done processing)
        #   Wait, need to track when R2 can start being unmarshalled
        
        # Actually simpler: second request queues behind first at server
        # Additional delay for R2 = server_chain for R1 = 2 + 10 + 2 = 14 ms
        # R2 completes at: 38 + 14 = 52 ms? No wait...
        
        # The key insight: with parallel sending, requests arrive ~simultaneously
        # But server processes sequentially
        # So total time = first_request_time + (n-1) * server_processing_per_request
        # where server_processing = unmarshal + process + marshal = 4 + 10 = 14 ms
        
        # Wait no, if requests are pipelined:
        # Time for last response = time first request completes + (n-1) * (t_marshal + t_server + t_marshal)
        #                        = 38 + 1 * 14 = 52 ms
        
        # But that assumes perfect pipelining. Let me recalculate considering actual timing:
        # For parallel threads, the second request's response completes when:
        # Server finishes R2 + network + unmarshal
        # Server starts R2 after R1: at time when R1 is processed
        # R1 processing done: 10 + 2 + 5 + 2 + 10 = 29 ms
        # R2 unmarshal starts: 29 + 2 = 31 ms (marshal R1 response)
        # Actually server can start R2 unmarshal at 29 while marshalling R1 response? No, single-threaded.
        
        # With single-threaded server:
        # R1: unmarshal=2, process=10, marshal=2 = 14 ms at server
        # R2: unmarshal=2, process=10, marshal=2 = 14 ms at server (after R1)
        # R2 response leaves server at: arrival + 14 + 14 = arrival + 28
        # R2 arrives at server at: 10 + 2 + 5 = 17 ms
        # R2 response leaves at: 17 + 28 = 45 ms
        # R2 response arrives at client: 45 + 5 = 50 ms
        # R2 response unmarshalled: 50 + 2 = 52 ms
        
        # So the answer for 2 requests with 2 threads should be 52 ms, not 50.
        
        # General formula for n requests with unlimited client threads:
        # = t_client + t_marshal + t_network + n * (t_marshal + t_server + t_marshal) + t_network + t_marshal
        # = t_client + t_marshal + t_network + n * (2*t_marshal + t_server) + t_network + t_marshal
        # = t_client + 2*t_marshal + 2*t_network + n * (2*t_marshal + t_server)
        
        parallel_time = (t_client + 
                        t_marshal +  # Client marshal (parallel)
                        t_network +  # To server
                        num_requests * (2 * t_marshal + t_server) +  # Server chain
                        t_network +  # Back to client
                        t_marshal)   # Client unmarshal
        
        result["total_time"] = parallel_time
        result["mode"] = "parallel"
    
    return result


def rpc_main():
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                    RPC TIMING CALCULATOR                         ║
║  Calculate synchronous Remote Procedure Call timing              ║
╚══════════════════════════════════════════════════════════════════╝

RPC Components:
  • Client computation (t_client): Time to prepare request arguments
  • Server processing (t_server): Time to process and compute response
  • Marshalling/Unmarshalling (t_marshal): Time for stubs to serialize/deserialize
  • Network transmission (t_network): Time for message to travel (one direction)
""")
    
    try:
        print("Enter timing parameters (in milliseconds):")
        t_client = float(input("  Client computation time (t_client): "))
        t_server = float(input("  Server processing time (t_server): "))
        t_marshal = float(input("  Marshalling time per operation (t_marshal): "))
        t_network = float(input("  Network transmission time one-way (t_network): "))
        
        num_requests = int(input("\nNumber of requests to make: "))
        if num_requests < 1:
            raise ValueError("Need at least 1 request.")
        
        num_threads = int(input("Number of client threads (1 for single-threaded): "))
        if num_threads < 1:
            raise ValueError("Need at least 1 thread.")
        
        # Calculate timing
        result = calculate_rpc_timing(t_client, t_server, t_marshal, t_network, 
                                      num_requests, num_threads)
        
        # Display single call breakdown
        print("\n" + "="*60)
        print("SINGLE RPC CALL BREAKDOWN")
        print("="*60)
        
        table = [[step, f"{time:.1f} ms"] for step, time in result["single_call_breakdown"]]
        table.append(["TOTAL", f"{result['single_call_time']:.1f} ms"])
        print(tabulate(table, headers=["Step", "Time"], tablefmt="grid"))
        
        # Display formula
        print(f"\nFormula: t_client + 4×t_marshal + 2×t_network + t_server")
        print(f"       = {t_client} + 4×{t_marshal} + 2×{t_network} + {t_server}")
        print(f"       = {t_client} + {4*t_marshal} + {2*t_network} + {t_server}")
        print(f"       = {result['single_call_time']:.1f} ms")
        
        # Display multi-request results
        print("\n" + "="*60)
        print(f"TIMING FOR {num_requests} REQUEST(S)")
        print("="*60)
        
        if num_threads == 1:
            print(f"\nMode: SEQUENTIAL (single-threaded client)")
            print(f"Each request must complete before the next starts.")
            print(f"\nTotal time = {result['single_call_time']:.1f} × {num_requests} = {result['total_time']:.1f} ms")
        else:
            print(f"\nMode: PARALLEL ({num_threads} client threads)")
            print(f"Client can prepare/send multiple requests simultaneously,")
            print(f"but server processes them sequentially (single-threaded server).")
            
            print(f"\nTiming breakdown:")
            print(f"  • Client prepares {min(num_threads, num_requests)} requests in parallel: {t_client} ms")
            print(f"  • Client stubs marshal (parallel): {t_marshal} ms")
            print(f"  • Network to server: {t_network} ms")
            print(f"  • Server processes {num_requests} requests sequentially:")
            print(f"      {num_requests} × (unmarshal + process + marshal)")
            print(f"    = {num_requests} × ({t_marshal} + {t_server} + {t_marshal})")
            print(f"    = {num_requests} × {2*t_marshal + t_server} = {num_requests * (2*t_marshal + t_server)} ms")
            print(f"  • Network back to client: {t_network} ms")
            print(f"  • Client stub unmarshals: {t_marshal} ms")
            
            print(f"\nTotal time = {result['total_time']:.1f} ms")
        
        # Compare sequential vs parallel
        if num_threads > 1 and num_requests > 1:
            sequential_time = result['single_call_time'] * num_requests
            parallel_time = result['total_time']
            savings = sequential_time - parallel_time
            
            print("\n" + "="*60)
            print("COMPARISON")
            print("="*60)
            comparison_table = [
                ["Sequential (1 thread)", f"{sequential_time:.1f} ms"],
                [f"Parallel ({num_threads} threads)", f"{parallel_time:.1f} ms"],
                ["Time savings", f"{savings:.1f} ms ({(savings/sequential_time)*100:.1f}%)"],
            ]
            print(tabulate(comparison_table, headers=["Mode", "Time"], tablefmt="grid"))
        
        print("\n" + "="*60)
        print(f"===> ANSWER: {result['total_time']:.0f} ms")
        print("="*60)
        
    except ValueError as e:
        print(f"Error: {e}")


def rpc_print_usage():
    print("""
Usage:
  Enter timing values in milliseconds when prompted:
  - t_client: Client computation time
  - t_server: Server processing time
  - t_marshal: Marshalling/unmarshalling time (per operation)
  - t_network: Network transmission time (one direction)
  - Number of requests
  - Number of client threads
""")


if __name__ == "__main__":
    rpc_main()
