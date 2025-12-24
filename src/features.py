import pandas as pd


def standardize_per_engine(df, sensors, group_col='engine_id', window=20):
    for sensor in sensors:
        healthy = (
            df[df['cycle'] <= window]
            .groupby(group_col)[sensor]
            .agg(['mean', 'std'])
            .reset_index()
        )
        healthy.columns = [group_col, f'{sensor}_mean', f'{sensor}_std']
        df = df.merge(healthy, on=group_col, how='left')
        df[sensor] = (df[sensor] - df[f'{sensor}_mean']) / df[f'{sensor}_std'].replace(0, 1)
        df.drop([f'{sensor}_mean', f'{sensor}_std'], axis=1, inplace=True)
    return df

def create_rolling_features(df, sensors, windows=[5, 10, 20], group_col='engine_id'):
    for sensor in sensors:
        for w in windows:
            grouped = df.groupby(group_col)[sensor]
            df[f'{sensor}_mean_{w}'] = grouped.transform(lambda x: x.rolling(w, min_periods=1).mean())
            df[f'{sensor}_std_{w}'] = grouped.transform(lambda x: x.rolling(w, min_periods=1).std())
            df[f'{sensor}_slope_{w}'] = grouped.transform(lambda x: (x - x.shift(w)) / w).fillna(0)
    return df.fillna(0)