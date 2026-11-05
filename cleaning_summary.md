# Cleaning Summary

- Rows: 8809 -> 8805
- Columns: 12 -> 16

## Missing values before cleaning

director      2634
cast           825
country        831
date_added      10
rating           4
duration         3

## Missing values after cleaning

date_added     10
year_added     10
month_added    10

## Changes made

1. Removed 0 exact duplicate rows and 4 duplicate records that only differed in `show_id` (after trimming whitespace).
2. Moved 3 duration values that were wrongly stored in `rating`.
3. Converted `date_added` to datetime (output format dd-mm-yyyy); added `year_added`, `month_added`.
4. Filled missing director/cast/country with 'Unknown' and rating with 'NR' (not rated). Missing `date_added` left as null (not guessed).
5. Split `duration` into `duration_value` (int) and `duration_unit` (min/season); `release_year` set to int.
6. Outlier check (IQR) on movie length: 450 unusual values flagged and kept (they are real titles).
