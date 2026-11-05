"""Task 1: Data Cleaning and Preprocessing - Netflix Movies and TV Shows (Kaggle)
Usage: python clean_netflix.py netflix_titles.csv
Outputs: netflix_cleaned.csv, cleaning_summary.md
"""
import sys
import pandas as pd

src = sys.argv[1] if len(sys.argv) > 1 else "netflix_titles.csv"
df = pd.read_csv(src, encoding="utf-8", encoding_errors="replace")
# drop empty "Unnamed" columns and fully empty rows left over from the export
df = df.loc[:, ~df.columns.astype(str).str.startswith("Unnamed")]
df = df.dropna(how="all")
rows0, cols0 = df.shape
log = []

# 1. Clean column names: lowercase, no spaces
df.columns = df.columns.str.strip().str.lower().str.replace(r"\s+", "_", regex=True)

# 2. Trim stray whitespace in text columns
for c in df.select_dtypes(include=["object", "string"]).columns:
    df[c] = df[c].str.strip()

missing_before = df.isnull().sum()

# 3. Duplicates (exact rows, then same title/type/year)
d1 = int(df.duplicated().sum())
df = df.drop_duplicates()
# same record repeated under a different show_id
d2 = int(df.duplicated(subset=[c for c in df.columns if c != "show_id"]).sum())
df = df.drop_duplicates(subset=[c for c in df.columns if c != "show_id"])
log.append(f"Removed {d1} exact duplicate rows and {d2} duplicate records that only differed in `show_id` (after trimming whitespace).")

# 4. Fix misplaced values: some rows have the duration inside `rating`
mask = df["rating"].str.contains("min", na=False) & df["duration"].isnull()
df.loc[mask, "duration"] = df.loc[mask, "rating"]
df.loc[mask, "rating"] = pd.NA
log.append(f"Moved {int(mask.sum())} duration values that were wrongly stored in `rating`.")

# 5. Dates -> datetime (saved as dd-mm-yyyy)
df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce", format="mixed")
df["year_added"] = df["date_added"].dt.year.astype("Int64")
df["month_added"] = df["date_added"].dt.month_name()
log.append("Converted `date_added` to datetime (output format dd-mm-yyyy); added `year_added`, `month_added`.")

# 6. Missing values
for c in ["director", "cast", "country"]:
    df[c] = df[c].fillna("Unknown")
df["rating"] = df["rating"].fillna("Not Rated")
log.append("Filled missing director/cast/country with 'Unknown' and rating with 'NR' (not rated). "
           "Missing `date_added` left as null (not guessed).")

# 7. Standardize text
df["type"] = df["type"].str.title().replace({"Tv Show": "TV Show"})
df["country"] = df["country"].str.replace(r"\s*,\s*", ", ", regex=True)
df["rating"] = df["rating"].str.upper().replace({"NOT RATED": "NR", "UR": "NR"})

# 8. Split duration into number + unit, fix dtypes
parts = df["duration"].str.extract(r"(\d+)\s*(\w+)")
df["duration_value"] = pd.to_numeric(parts[0]).astype("Int64")
df["duration_unit"] = parts[1].str.lower().str.rstrip("s")
df["release_year"] = df["release_year"].astype(int)
log.append("Split `duration` into `duration_value` (int) and `duration_unit` (min/season); `release_year` set to int.")

# 9. Outlier check (flag only, do not delete)
m = df[df["duration_unit"] == "min"]["duration_value"].dropna()
q1, q3 = m.quantile([0.25, 0.75])
iqr = q3 - q1
n_out = int(((m < q1 - 1.5 * iqr) | (m > q3 + 1.5 * iqr)).sum())
log.append(f"Outlier check (IQR) on movie length: {n_out} unusual values flagged and kept (they are real titles).")

df.to_csv("netflix_cleaned.csv", index=False, date_format="%d-%m-%Y")

with open("cleaning_summary.md", "w") as f:
    f.write("# Cleaning Summary\n\n")
    f.write(f"- Rows: {rows0} -> {len(df)}\n- Columns: {cols0} -> {df.shape[1]}\n\n")
    f.write("## Missing values before cleaning\n\n")
    f.write(missing_before[missing_before > 0].to_string() + "\n\n")
    f.write("## Missing values after cleaning\n\n")
    f.write(df.isnull().sum()[lambda s: s > 0].to_string() + "\n\n")
    f.write("## Changes made\n\n" + "\n".join(f"{i}. {l}" for i, l in enumerate(log, 1)) + "\n")
print(open("cleaning_summary.md").read())
