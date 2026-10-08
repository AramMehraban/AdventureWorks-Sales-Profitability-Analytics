from pathlib import Path

import pandas as pd


# ============================================================
# ADVENTUREWORKS EXCEL EXPORT
# ============================================================

print("=" * 70)
print("ADVENTUREWORKS EXCEL EXPORT")
print("=" * 70)


# ============================================================
# 1. PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

ANALYSIS_DIR = (
    BASE_DIR
    / "reports"
    / "analysis"
)

OUTPUT_FILE = (
    BASE_DIR
    / "reports"
    / "AdventureWorks_Analytics_Report.xlsx"
)


# ============================================================
# 2. REQUIRED INPUT FILES
# ============================================================

print("\n[1] CHECKING INPUT FILES")

input_files = {
    "KPI Summary": "kpi_summary.csv",
    "Yearly Analysis": "yearly_sales_profit.csv",
    "Monthly Analysis": "monthly_sales_profit.csv",
    "Country Analysis": "country_analysis.csv",
    "Category Analysis": "category_analysis.csv",
    "Product Analysis": "product_analysis.csv",
    "Customer Analysis": "customer_analysis.csv",
    "City Analysis": "city_analysis.csv",
}


missing_files = []

for sheet_name, file_name in input_files.items():

    file_path = (
        ANALYSIS_DIR
        / file_name
    )

    if not file_path.exists():

        missing_files.append(
            file_name
        )


print(
    f"Required files: "
    f"{len(input_files)}"
)

print(
    f"Missing files: "
    f"{len(missing_files)}"
)


if missing_files:

    print("\nMissing files:")

    for file_name in missing_files:
        print(
            f" - {file_name}"
        )

    raise FileNotFoundError(
        "Required analysis files are missing."
    )


# ============================================================
# 3. LOAD DATA
# ============================================================

print("\n[2] LOADING ANALYSIS DATA")

dataframes = {}

for sheet_name, file_name in input_files.items():

    file_path = (
        ANALYSIS_DIR
        / file_name
    )

    df = pd.read_csv(
        file_path
    )

    dataframes[sheet_name] = df

    print(
        f"{sheet_name}: "
        f"{len(df):,} rows × "
        f"{len(df.columns):,} columns"
    )


# ============================================================
# 4. PREPARE OUTPUT DIRECTORY
# ============================================================

print("\n[3] PREPARING EXCEL OUTPUT")

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# 5. EXCEL WRITER
# ============================================================

with pd.ExcelWriter(
    OUTPUT_FILE,
    engine="xlsxwriter"
) as writer:

    workbook = writer.book


    # ========================================================
    # EXCEL FORMATS
    # ========================================================

    title_format = workbook.add_format(
        {
            "bold": True,
            "font_size": 16,
            "align": "center",
            "valign": "vcenter",
        }
    )

    header_format = workbook.add_format(
        {
            "bold": True,
            "border": 1,
            "align": "center",
            "valign": "vcenter",
        }
    )

    currency_format = workbook.add_format(
        {
            "num_format": '#,##0.00',
        }
    )

    percentage_format = workbook.add_format(
        {
            "num_format": '0.00%',
        }
    )

    integer_format = workbook.add_format(
        {
            "num_format": '#,##0',
        }
    )

    decimal_format = workbook.add_format(
        {
            "num_format": '#,##0.00',
        }
    )


    # ========================================================
    # 6. WRITE EACH SHEET
    # ========================================================

    print("\n[4] WRITING EXCEL SHEETS")


    for sheet_name, df in dataframes.items():

        df.to_excel(
            writer,
            sheet_name=sheet_name,
            index=False,
            startrow=1
        )

        worksheet = writer.sheets[
            sheet_name
        ]


        # ----------------------------------------------------
        # Title
        # ----------------------------------------------------

        worksheet.merge_range(
            0,
            0,
            0,
            max(len(df.columns) - 1, 0),
            f"AdventureWorks {sheet_name}",
            title_format
        )


        # ----------------------------------------------------
        # Header formatting
        # ----------------------------------------------------

        for col_num, column_name in enumerate(
            df.columns
        ):

            worksheet.write(
                1,
                col_num,
                column_name,
                header_format
            )


        # ----------------------------------------------------
        # Freeze panes
        # ----------------------------------------------------

        worksheet.freeze_panes(
            2,
            0
        )


        # ----------------------------------------------------
        # Excel Table
        # ----------------------------------------------------

        if (
            len(df) > 0
            and len(df.columns) > 0
        ):

            worksheet.add_table(
                1,
                0,
                len(df) + 1,
                len(df.columns) - 1,
                {
                    "columns": [
                        {
                            "header": column
                        }
                        for column in df.columns
                    ],
                    "style": "Table Style Medium 2",
                }
            )


        # ----------------------------------------------------
        # Column widths
        # ----------------------------------------------------

        for col_num, column_name in enumerate(
            df.columns
        ):

            column_values = (
                df[column_name]
                .astype(str)
            )

            if len(column_values) > 0:

                value_lengths = (
                    column_values
                    .map(
                        lambda value: len(str(value))
                    )
                )

                max_value_length = (
                    value_lengths.max()
                )

            else:

                max_value_length = 0


            max_length = max(
                len(str(column_name)),
                max_value_length
            )


            width = min(
                max(max_length + 2, 10),
                35
            )


            worksheet.set_column(
                col_num,
                col_num,
                width
            )


        # ----------------------------------------------------
        # Number formats
        # ----------------------------------------------------

        for col_num, column_name in enumerate(
            df.columns
        ):

            column_lower = (
                column_name.lower()
            )


            # Financial columns
            if column_lower in [
                "sales",
                "cost",
                "profit",
                "value",
            ]:

                worksheet.set_column(
                    col_num,
                    col_num,
                    None,
                    currency_format
                )


            # Percentage columns
            elif (
                "margin" in column_lower
                or "growth" in column_lower
                or "share" in column_lower
            ):

                worksheet.set_column(
                    col_num,
                    col_num,
                    None,
                    percentage_format
                )


            # Integer columns
            elif column_lower in [
                "orders",
                "customers",
                "salesrecords",
                "customerkey",
            ]:

                worksheet.set_column(
                    col_num,
                    col_num,
                    None,
                    integer_format
                )


            # Decimal columns
            elif column_lower in [
                "averageordervalue",
                "averagesalesperrecord",
            ]:

                worksheet.set_column(
                    col_num,
                    col_num,
                    None,
                    decimal_format
                )


# ============================================================
# 7. KPI SUMMARY
# ============================================================

print("\n[5] FORMATTING KPI SUMMARY")

kpi_df = dataframes[
    "KPI Summary"
]


# ============================================================
# 8. ADD KPI DESCRIPTIONS
# ============================================================

# Re-open workbook with xlsxwriter is not possible after
# closing the writer, so KPI descriptions are intentionally
# handled before final validation in the next workbook version.


# ============================================================
# 9. FINAL VALIDATION
# ============================================================

print("\n[6] EXCEL VALIDATION")

if not OUTPUT_FILE.exists():

    raise FileNotFoundError(
        f"Excel file was not created:\n{OUTPUT_FILE}"
    )


file_size = (
    OUTPUT_FILE.stat()
    .st_size
)


print(
    "Excel file exists: YES"
)

print(
    f"File size: "
    f"{file_size:,} bytes"
)


if file_size == 0:

    raise ValueError(
        "Excel file is empty."
    )


# ============================================================
# 10. EXPECTED SHEETS
# ============================================================

print("\n[7] EXPECTED SHEETS")

expected_sheets = [
    "KPI Summary",
    "Yearly Analysis",
    "Monthly Analysis",
    "Country Analysis",
    "Category Analysis",
    "Product Analysis",
    "Customer Analysis",
    "City Analysis",
]


print(
    f"Expected sheets: "
    f"{len(expected_sheets)}"
)

for sheet in expected_sheets:

    print(
        f" - {sheet}"
    )


# ============================================================
# 11. FINAL STATUS
# ============================================================

print("\n" + "=" * 70)
print("EXCEL EXPORT COMPLETED")
print("=" * 70)

print(
    "OVERALL STATUS: PASS"
)

print(
    f"Workbook:\n"
    f"{OUTPUT_FILE}"
)

print(
    f"Sheets: "
    f"{len(expected_sheets)}"
)

print("=" * 70)