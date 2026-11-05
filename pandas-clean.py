"""Pandas data cleaning pipeline: inspection, deduplication, text cleanup, type conversion, missing values, outliers, and export."""
from pathlib import Path
import pandas as pd

INPUT_FILE = Path('orders.csv')
OUTPUT_FILE = Path('order_clean.csv')


def clean_orders(raw: pd.DataFrame) -> pd.DataFrame:
    """Clean order data without modifying the input DataFrame."""
    required = {'order_id', 'customer', 'city', 'price', 'qty'}
    missing_columns = required - set(raw.columns)
    if missing_columns:
        raise ValueError(f'CSV is missing required columns: {sorted(missing_columns)}')

    # 2.2 Data inspection
    print(f'\nMissing values per column:\n{raw.isna().sum()}')
    print(f'\nNumber of fully duplicated rows:\n{raw.duplicated().sum()}')
    print(f'\nColumn data types:\n{raw.dtypes}')

    # 2.3 Remove duplicates
    print(f'\nOriginal data:\n{raw}')
    df = raw.drop_duplicates().copy()
    print(f'\nAfter removing duplicates:\n{df}')

    # 2.4 Clean text while preserving missing values instead of converting NaN to text
    for column in ['customer', 'city']:
        df[column] = df[column].astype('string').str.strip()
        df[column] = df[column].replace('', pd.NA)
    print(f'\nAfter text cleanup:\n{df[["customer", "city"]]}')

    # 2.5 Convert data types; invalid numeric values become NaN
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df['qty'] = pd.to_numeric(df['qty'], errors='coerce')
    print(f'\nAfter numeric conversion:\n{df[["price", "qty"]]}')
    print(f'\nPrice data type after conversion:\n{df["price"].dtype}')

    # 2.6 Handle missing values
    print(f'\nMissing values before imputation:\n{df.isna().sum()}')
    before = len(df)
    df = df.dropna(subset=['order_id']).copy()
    print(f'\nRows after dropping missing order_id: {before} -> {len(df)}')
    df['customer'] = df['customer'].fillna('Unknown')
    # Fill missing city values to keep the output free of missing data
    df['city'] = df['city'].fillna('Unknown')
    median_price = df['price'].median()
    if pd.isna(median_price):
        raise ValueError('No valid prices available to calculate the median for imputation')
    df['price'] = df['price'].fillna(median_price)
    df['qty'] = df['qty'].fillna(0)
    # Convert quantity to integers only when all values are whole numbers
    if not (df['qty'] % 1 == 0).all():
        raise ValueError('qty contains non-integer values; review the business rules')
    df['qty'] = df['qty'].astype(int)
    print(f'\nAfter filling missing values:\n{df}')
    print(f'\nRemaining missing values after imputation: {int(df.isna().sum().sum())}')

    # 2.7 Outliers: example rule replaces prices above 10000 with the mean of valid prices
    print(f'\nMean price before outlier treatment: {df["price"].mean():.1f}')
    print(f'Median price before outlier treatment: {df["price"].median():.1f}')
    normal_prices = df.loc[df['price'] <= 10000, 'price']
    if normal_prices.empty:
        raise ValueError('No valid prices available to calculate the replacement mean')
    mean = normal_prices.mean()
    df.loc[df['price'] > 10000, 'price'] = mean
    print(f'\nMean price after outlier treatment: {df["price"].mean():.1f}')
    print(f'Median price after outlier treatment: {df["price"].median():.1f}')

    # Sort and reset the row index
    df = df.sort_values('price', ascending=False).reset_index(drop=True)
    print(f'\nCleaned data:\n{df}')
    return df


def main() -> None:
    raw = pd.read_csv(INPUT_FILE, dtype={'order_id': 'string'})
    df = clean_orders(raw)
    df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
    print(f'\nExported successfully: {OUTPUT_FILE.resolve()}, {len(df)} rows')


if __name__ == '__main__':
    main()
