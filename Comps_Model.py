def compute_median_multiple(peers: list, metric: str) -> float:
    """
    Computes the median multiple for a specified valuation metric from a list of peers.

    Parameters:
        peers (list): List of dictionaries containing valuation multiples for each peer.
        metric (str): Valuation metric key (e.g., 'EV/EBITDA', 'P/E', or 'EV/Sales').

    Returns:
        float: Median multiple, or None if no valid data is found.
    """
    # Extract non-null values for the given metric
    multiples = [peer[metric] for peer in peers if peer.get(metric) is not None]

    if not multiples:
        return None

    multiples.sort()
    n = len(multiples)
    mid = n // 2
    if n % 2 == 0:
        # even number of elements: average the two middle numbers
        return (multiples[mid - 1] + multiples[mid]) / 2.0
    else:
        # odd number of elements: return the middle element
        return multiples[mid]


def apply_comps(target_metric_value: float, median_multiple: float) -> float:
    """
    Applies the median multiple to the target's metric (e.g., EBITDA) to derive an estimated enterprise value.

    Parameters:
        target_metric_value (float): The target company's metric value (e.g., EBITDA).
        median_multiple (float): The median valuation multiple from the peer group.

    Returns:
        float: Estimated enterprise value.
    """
    return target_metric_value * median_multiple


if __name__ == "__main__":
    # Example static peer group data: each peer is represented as a dictionary of valuation multiples.
    peers = [
        {"ticker": "AAPL", "P/E": 28.0, "EV/EBITDA": 18.0, "EV/Sales": 7.5},
        {"ticker": "MSFT", "P/E": 35.0, "EV/EBITDA": 20.0, "EV/Sales": 10.0},
        {"ticker": "GOOGL", "P/E": 30.0, "EV/EBITDA": 19.0, "EV/Sales": 8.0},
        {"ticker": "AMZN", "P/E": 90.0, "EV/EBITDA": 22.0, "EV/Sales": 5.0},
        {"ticker": "FB", "P/E": 25.0, "EV/EBITDA": 16.0, "EV/Sales": 6.5},
    ]

    # Suppose the target company's EBITDA is known (units can be in millions)
    target_ebitda = 150.0

    # Calculate the median EV/EBITDA multiple from the peer group
    median_ev_ebitda = compute_median_multiple(peers, "EV/EBITDA")

    # Apply the median multiple to the target's EBITDA to get an estimated enterprise value
    enterprise_value = apply_comps(target_ebitda, median_ev_ebitda)

    print(f"Median EV/EBITDA Multiple: {median_ev_ebitda}")
    print(f"Estimated Enterprise Value: {enterprise_value}")
