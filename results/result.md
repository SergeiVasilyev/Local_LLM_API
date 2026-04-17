Here’s a simple implementation:

```python
def count_addresses(start_ip: str, end_ip: str) -> int:
    """
    Returns the number of IPv4 addresses between start_ip and end_ip.
    
    Parameters:
        start_ip  : First (inclusive) IPv4 address string
        end_ip    : Second (exclusive) IPv4 address string
    
    Returns:
        Number of addresses in [start_ip, end_ip)
    """
    # Convert both strings to an IP object and subtract the second from the first
    ip_obj1 = ip_address(start_ip)
    ip_obj2 = ip_address(end_ip)

    return (ip_obj1 - ip_obj2).total()  # number of addresses between them inclusive, exclusive of end


def ip_address(ip_str: str) -> "IP":
    """Simple IP address parser for IPv4."""
    parts = ip_str.split(".")
    if len(parts) != 4:
        raise ValueError("Invalid IPv4 address format")
    
    try:
        # Validate each octet is numeric, between 0 and 255
        return IP(ip_parts=[int(p) for p in parts])
    except (ValueError, OverflowError):
        raise ValueError(f"Invalid IPv4 address: {ip_str}")


def main():
    start = "192.168.1.10"
    end = "192.168.1.250"

    count = count_addresses(start, end)
    print(f"The number of addresses between '{start}' and '{end}' is: {count}")


if __name__ == "__main__":
    main()
```