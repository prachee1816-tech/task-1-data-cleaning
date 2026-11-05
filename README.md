# Task 1: Data Cleaning and Preprocessing

**Dataset:** Netflix Movies and TV Shows (Kaggle) - `netflix_titles.csv`
**Tools:** Python (Pandas)

## Files
- `netflix_titles.csv` - raw dataset
- `clean_netflix.py` - cleaning script
- `netflix_cleaned.csv` - cleaned dataset
- `cleaning_summary.md` - before/after counts and change log

## Summary of changes
Rows: 8809 -> 8805 | Columns: 12 -> 16

1. Dropped empty "Unnamed" columns and empty rows left over from the CSV export.
2. Cleaned column names (lowercase, underscores) and trimmed whitespace in text columns.
3. Removed 4 duplicate records (same content, different `show_id`).
4. Fixed 3 rows where the movie duration was stored in the `rating` column.
5. Missing values: `director` (2634), `cast` (825), `country` (831) filled with `Unknown`; `rating` (4) filled with `NR`. 10 missing `date_added` values left null instead of guessing.
6. Converted `date_added` to datetime, saved as dd-mm-yyyy; added `year_added` and `month_added`.
7. Standardized text: `type` ("TV Show"), spacing in `country`, and rating labels (NOT RATED / UR merged into NR).
8. Split `duration` into `duration_value` (int) and `duration_unit` (min / season); `release_year` set to int.
9. Outlier check (IQR) on movie length: 450 unusual values flagged and kept, since they are real titles.

## How to run
`pip install pandas` then `python clean_netflix.py netflix_titles.csv`
