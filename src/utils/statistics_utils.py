import numpy as np


def calculate_mode(series):
    return series.mode()[0] if not series.mode().empty else None


def calculate_top_3_mode_with_counts(series):
    value_counts = series.value_counts().nlargest(3)
    return list(zip(value_counts.index.tolist(), value_counts.tolist()))


def calculate_top_3_mode_with_percentage(series, total_count):
    value_counts = series.value_counts().nlargest(3)
    percentages = (value_counts / total_count) * 100
    rounded_percentages = np.round(percentages, 2)

    return list(zip(value_counts.index.tolist(), rounded_percentages.tolist()))


def calculate_top_3_highest(series):
    return series.nlargest(3).tolist()


def calculate_percentage(df, col_value, col_total):
    return (df[col_value] / df[col_total]) * 100
