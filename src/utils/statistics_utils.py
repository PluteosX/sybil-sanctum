def calculate_mode(series):
    return series.mode()[0] if not series.mode().empty else None


def calculate_top_3_mode_with_counts(series):
    value_counts = series.value_counts().nlargest(3)
    return list(zip(value_counts.index.tolist(), value_counts.tolist()))


def calculate_top_3_highest(series):
    return series.nlargest(3).tolist()
