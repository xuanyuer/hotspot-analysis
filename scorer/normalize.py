import statistics


def normalize_churn(churn_data: dict[str, dict]) -> dict[str, float]:
    """IQR-based min-max normalization of churn to 0-100 scale.
    
    Uses commit_count as the primary churn metric.
    Outliers beyond [Q1-1.5*IQR, Q3+1.5*IQR] are capped.
    """
    if not churn_data:
        return {}

    values = [d["commit_count"] for d in churn_data.values()]
    q1 = statistics.quantiles(values, n=4, method='inclusive')[0]
    q3 = statistics.quantiles(values, n=4, method='inclusive')[2]
    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    def cap(val: float) -> float:
        return max(lower_bound, min(val, upper_bound))

    capped = [cap(v) for v in values]
    min_val = min(capped)
    max_val = max(capped)

    result = {}
    for path, raw in churn_data.items():
        c = cap(raw["commit_count"])
        if max_val == min_val:
            result[path] = 0.0
        else:
            result[path] = ((c - min_val) / (max_val - min_val)) * 100.0

    return result


def normalize_complexity(complexity_data: dict[str, dict]) -> dict[str, float]:
    """IQR-based min-max normalization of complexity to 0-100 scale.
    
    Uses max_complexity as the primary complexity metric.
    """
    if not complexity_data:
        return {}

    values = [d["max_complexity"] for d in complexity_data.values()]
    q1 = statistics.quantiles(values, n=4, method='inclusive')[0]
    q3 = statistics.quantiles(values, n=4, method='inclusive')[2]
    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    def cap(val: float) -> float:
        return max(lower_bound, min(val, upper_bound))

    capped = [cap(v) for v in values]
    min_val = min(capped)
    max_val = max(capped)

    result = {}
    for path, raw in complexity_data.items():
        c = cap(raw["max_complexity"])
        if max_val == min_val:
            result[path] = 0.0
        else:
            result[path] = ((c - min_val) / (max_val - min_val)) * 100.0

    return result
