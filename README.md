# python-pandas-data-engineering
A collection of hands-on Python data engineering projects covering Pandas, data cleaning, ETL pipelines, and data processing best practices.

## Pandas Data Cleaning Workflow

### P1 — Core Data Cleaning Steps

1. **Data Inspection:** Check missing values using `isna().sum()` and duplicate rows using `duplicated().sum()`.

2. **Remove Duplicates:** Use `drop_duplicates()` to remove duplicate rows.

3. **String Cleaning:** Use `str.strip()` to remove leading and trailing whitespace.

4. **Data Type Conversion:** Use `pd.to_numeric(errors="coerce")` to convert values to numeric types. Invalid values are converted to `NaN`.

5. **Handle Missing Values:** Use `dropna()` to remove rows with missing values in critical fields, and `fillna()` to fill missing values in other fields.

6. **Outlier Handling:** Replace outliers with the median value.

7. **Export Cleaned Data:** Use `to_csv(index=False, encoding="utf-8-sig")` to export the cleaned dataset without the index and with UTF-8 BOM encoding for Excel compatibility.

### P2 — Important Notes

**DataFrame Modification:** By default, `dropna()` and `fillna()` do not modify the original DataFrame.

To save the changes, either reassign the result or use `inplace=True`.

```python
# Recommended: Reassign the result
df = df.dropna()
df = df.fillna(0)

# Alternative: Modify the DataFrame in place
df.dropna(inplace=True)
df.fillna(0, inplace=True)
```
