import pandas as pd
def concise_value_counts_summary(df: pd.DataFrame, bins: int = 5, max_categories_shown: int = 10):
    summary = []

    for col in df.columns:
        col_data = df[col].dropna()

        if pd.api.types.is_numeric_dtype(col_data):
            if col_data.empty:
                continue

            summary.append({
                "Column": col,
                "Type": "Numeric",
                "Non-null Count": len(col_data),
                "Unique Values": col_data.nunique(),
                "Min": col_data.min(),
                "Max": col_data.max(),
                "Details": " "
            })

        else:
            col_data = col_data.astype(str)
            unique_vals = col_data.nunique()
            categories = col_data.unique()

            category_preview = ", ".join(sorted(categories)[:max_categories_shown])
            if len(categories) > max_categories_shown:
                category_preview += f", ... (+{len(categories) - max_categories_shown} more)"

            summary.append({
                "Column": col,
                "Type": "Categorical",
                "Non-null Count": len(col_data),
                "Unique Values": unique_vals,
                "Min": "-",
                "Max": "-",
                "Details": category_preview
            })

    return pd.DataFrame(summary).to_markdown(index=False)