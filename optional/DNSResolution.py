"""
DNS Resolution Simulation (van Steen/Tanenbaum, Section 5.3)

DNS uses a hierarchical naming system to resolve domain names to IP addresses.
This simulation demonstrates iterative and recursive resolution.

Resolution Modes:
    Iterative: Client queries each server, which returns a referral.
    Recursive: Client queries local resolver, which handles all lookups.

DNS Hierarchy:
    Root (.) -> TLD (.com, .org) -> Authoritative (google.com)
"""

from tabulate import tabulate


# Simulated DNS database
DNS_DATABASE = {
    # Root servers
    ".": {
        "type": "root",
        "referrals": {
            "com.": "TLD_COM",
            "org.": "TLD_ORG",
            "at.": "TLD_AT",
        }
    },
    # TLD servers
    "TLD_COM": {
        "type": "tld",
        "zone": "com.",
        "referrals": {
            "google.com.": "AUTH_GOOGLE",
            "github.com.": "AUTH_GITHUB",
        }
    },
    "TLD_ORG": {
        "type": "tld",
        "zone": "org.",
        "referrals": {
            "wikipedia.org.": "AUTH_WIKIPEDIA",
        }
    },
    "TLD_AT": {
        "type": "tld",
        "zone": "at.",
        "referrals": {
            "tuwien.ac.at.": "AUTH_TUWIEN",
        }
    },
    # Authoritative servers
    "AUTH_GOOGLE": {
        "type": "authoritative",
        "zone": "google.com.",
        "records": {
            "google.com.": "142.250.185.46",
            "www.google.com.": "142.250.185.68",
            "mail.google.com.": "142.250.185.69",
        }
    },
    "AUTH_GITHUB": {
        "type": "authoritative",
        "zone": "github.com.",
        "records": {
            "github.com.": "140.82.121.4",
            "www.github.com.": "140.82.121.4",
        }
    },
    "AUTH_WIKIPEDIA": {
        "type": "authoritative",
        "zone": "wikipedia.org.",
        "records": {
            "wikipedia.org.": "208.80.154.224",
            "www.wikipedia.org.": "208.80.154.224",
        }
    },
    "AUTH_TUWIEN": {
        "type": "authoritative",
        "zone": "tuwien.ac.at.",
        "records": {
            "tuwien.ac.at.": "128.130.0.1",
            "www.tuwien.ac.at.": "128.130.0.2",
            "tuwel.tuwien.ac.at.": "128.130.0.10",
        }
    },
}


def normalize_domain(domain: str) -> str:
    """Ensure domain ends with a dot (FQDN)."""
    if not domain.endswith('.'):
        domain += '.'
    return domain.lower()


def get_tld(domain: str) -> str:
    """Extract TLD from domain (e.g., 'com.' from 'www.google.com.')."""
    parts = domain.rstrip('.').split('.')
    return parts[-1] + '.'


def get_parent_zone(domain: str) -> str:
    """Get parent zone (e.g., 'google.com.' from 'www.google.com.')."""
    parts = domain.rstrip('.').split('.')
    if len(parts) <= 2:
        return domain
    # For domains like tuwel.tuwien.ac.at, try progressively larger zones
    return '.'.join(parts[1:]) + '.'


def find_auth_zone(domain: str, tld_data: dict) -> str | None:
    """Find the authoritative zone for a domain by checking parent zones."""
    parts = domain.rstrip('.').split('.')
    # Try progressively larger parent zones
    for i in range(len(parts) - 1):
        zone = '.'.join(parts[i:]) + '.'
        if zone in tld_data.get("referrals", {}):
            return zone
    return None


def iterative_resolution(domain: str) -> tuple[str | None, list[str]]:
    """
    Perform iterative DNS resolution.
    Client queries each server and follows referrals.
    """
    steps = []
    domain = normalize_domain(domain)
    
    steps.append(f"=== ITERATIVE RESOLUTION for '{domain}' ===")
    
    # Step 1: Query root
    steps.append(f"\n1. Client queries ROOT server for '{domain}'")
    tld = get_tld(domain)
    
    root_data = DNS_DATABASE["."]
    if tld not in root_data["referrals"]:
        steps.append(f"   ROOT: Unknown TLD '{tld}'")
        return None, steps
    
    tld_server = root_data["referrals"][tld]
    steps.append(f"   ROOT: Referral -> {tld_server} (handles '{tld}')")
    
    # Step 2: Query TLD
    steps.append(f"\n2. Client queries TLD server '{tld_server}' for '{domain}'")
    tld_data = DNS_DATABASE[tld_server]
    parent_zone = find_auth_zone(domain, tld_data)
    
    if parent_zone is None:
        steps.append(f"   TLD: Unknown zone for '{domain}'")
        return None, steps
    
    auth_server = tld_data["referrals"][parent_zone]
    steps.append(f"   TLD: Referral -> {auth_server} (handles '{parent_zone}')")
    
    # Step 3: Query authoritative
    steps.append(f"\n3. Client queries AUTHORITATIVE server '{auth_server}' for '{domain}'")
    auth_data = DNS_DATABASE[auth_server]
    
    if domain in auth_data["records"]:
        ip = auth_data["records"][domain]
        steps.append(f"   AUTH: Answer -> {ip}")
        return ip, steps
    else:
        steps.append(f"   AUTH: No record for '{domain}'")
        return None, steps


def recursive_resolution(domain: str) -> tuple[str | None, list[str]]:
    """
    Perform recursive DNS resolution.
    Local resolver handles all lookups on behalf of client.
    """
    steps = []
    domain = normalize_domain(domain)
    
    steps.append(f"=== RECURSIVE RESOLUTION for '{domain}' ===")
    steps.append(f"\n1. Client sends query to LOCAL RESOLVER")
    steps.append(f"   (Resolver handles all lookups)")
    
    # Resolver does the work (same as iterative internally)
    tld = get_tld(domain)
    root_data = DNS_DATABASE["."]
    
    if tld not in root_data["referrals"]:
        steps.append(f"\n2. Resolver queries ROOT -> Unknown TLD")
        return None, steps
    
    tld_server = root_data["referrals"][tld]
    steps.append(f"\n2. Resolver queries ROOT -> Referral to {tld_server}")
    
    tld_data = DNS_DATABASE[tld_server]
    parent_zone = get_parent_zone(domain)
    
    if parent_zone not in tld_data["referrals"]:
        steps.append(f"\n3. Resolver queries TLD -> Unknown zone")
        return None, steps
    
    auth_server = tld_data["referrals"][parent_zone]
    steps.append(f"\n3. Resolver queries TLD -> Referral to {auth_server}")
    
    auth_data = DNS_DATABASE[auth_server]
    
    if domain in auth_data["records"]:
        ip = auth_data["records"][domain]
        steps.append(f"\n4. Resolver queries AUTH -> {ip}")
        steps.append(f"\n5. Resolver returns answer to Client: {ip}")
        return ip, steps
    else:
        steps.append(f"\n4. Resolver queries AUTH -> No record")
        return None, steps


def main():
    print("""
DNS Resolution Simulation
=========================
Demonstrates iterative vs recursive DNS lookups.

Available domains:
  - google.com, www.google.com, mail.google.com
  - github.com, www.github.com
  - wikipedia.org, www.wikipedia.org
  - tuwien.ac.at, www.tuwien.ac.at, tuwel.tuwien.ac.at
""")
    
    try:
        domain = input("Enter domain to resolve: ").strip()
        mode = input("Resolution mode (i=iterative, r=recursive): ").strip().lower()
        
        if mode == 'i':
            ip, steps = iterative_resolution(domain)
        elif mode == 'r':
            ip, steps = recursive_resolution(domain)
        else:
            print("Invalid mode. Use 'i' or 'r'.")
            return
        
        print("\n--- Resolution Steps ---")
        for step in steps:
            print(step)
        
        if ip:
            print(f"\n==> RESOLVED: {domain} -> {ip}")
        else:
            print(f"\n==> FAILED: Could not resolve '{domain}'")
            
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
