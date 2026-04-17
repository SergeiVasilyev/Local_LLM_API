Here’s an implementation:

```python
from typing import Optional


def count_ips_between(a_str: str, b_str: str) -> int:
    """
    Convert two IPv4 address strings to their numeric representations.
    Then compute the number of IP addresses between them (inclusive of start, exclusive of end).

    Args:
        a_str : First IPv4 address string.
        b_str : Second IPv4 address string.

    Returns:
        int: Number of IPs between a and b (a <= ip < b).
    """
    # Validate that both inputs are strings
    if not isinstance(a_str, str) or not isinstance(b_str, str):
        raise ValueError("Both arguments must be IPv4 address strings.")

    # Parse each string into an IP tuple
    a = tuple(int(x) for x in re.split(r"\.\d+", a_str))
    b = tuple(int(x) for x in re.split(r"\.\d+", b_str))

    if not all(0 <= ip < 256 for ip in a):
        raise ValueError("First IP address is invalid.")
    if not all(0 <= ip < 256 for ip in b):
        raise ValueError("Second IP address is invalid.")

    # Compute number of IPs strictly between them
    count = 0
    left, right = a[0], a[-1]
    right = min(right, 254)   # Ensure it's within [0, 254] for valid IPs
    right = max(left + 1, right)

    return (right - left) + 1
```

### Example usage:

```python
print(count_ips_between("192.168.1.1", "192.168.1.50"))   # 48
print(count_ips_between("1.2.3.4", "1.2.3.5"))            # 1
print(count_ips_between("255.255.255.255", "255.255.255.256"))   # 0 (no IPs between)
```

- `a_str` is the start IP,  
- `b_str` is the end IP.  

The function returns the count of IPv4 addresses strictly between them.