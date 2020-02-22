import pandas as pd


def generate_rank_df(df, ascending=True):
    order = pd.DataFrame(columns=df.columns)

    for column in df.columns:
        sort = df.sort_values([column], ascending=ascending, kind='mergesort')
        order[column] = tuple(sort.index)

    return order


def calculate_rank_correlation(df, correlation):
    corr = []

    for column in df.columns:
        row = []
        for other in df.columns:
            row.append(correlation(df[column], df[other])[0])
        corr.append(row)

    return pd.DataFrame(corr, index=df.columns, columns=df.columns)
