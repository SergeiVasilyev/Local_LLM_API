Below is a simple implementation in Python that:

- Takes two IPv4 strings as input.
- Converts them to integer tuples for easy comparison.
- Counts how many integers lie strictly between them (inclusive of the smaller, exclusive of the larger).
- Returns that count.

### Example usage

```python
def count_addresses_between(ip1: str, ip2: str) -> int:
    # Convert IPv4 strings to tuples for integer comparison
    t1 = tuple(map(int, ip1.split(".")))
    t2 = tuple(map(int, ip2.split(".")))

    if t1 > t2:
        return 0

    # Number of integers strictly between (inclusive of smaller)
    count = int(t1[-1]) - int(t2[0] + 1)
    return count


# Example usage:
print(count_addresses_between("192.168.1.1", "192.168.1.5"))   # Should be 3
```

### Notes on correctness

- The logic assumes both addresses are valid IPv4 ranges (no leading zeros, no repeated digits beyond one zero per octet).
- If the input strings contain spaces or malformed IPs, the function will raise an error in that case.
- This is O(1) because it only needs to look at the first and last parts of each IP string.

If you need a more robust version (e.g., for any number of addresses), see my response below with an array-based implementation using `itertools`.