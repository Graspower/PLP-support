import pandas as pd
import os

# List of your 6 CSV files
file_list = [
    "List of Tickets login.csv",
    "List of Tickets live classes.csv",
    "List of Tickets content.csv",
    "List of Tickets progress.csv",
    "List of Tickets certificates.csv",
    "List of Tickets advanced.csv"
]

start_date = pd.to_datetime("2025-04-04")
end_date = pd.to_datetime("2025-04-12")

# Collect everything in rows
final_output_rows = []

grand_total_received = 0
grand_total_closed = 0

for file in file_list:
    df_raw = pd.read_csv(file)

    df_raw["Created On"] = df_raw["Created On"].str.replace(" +0000 UTC", "", regex=False)
    df_raw["Closed On"] = df_raw["Closed On"].str.replace(" +0000 UTC", "", regex=False)

    df_raw["Created On"] = pd.to_datetime(df_raw["Created On"], errors='coerce')
    df_raw["Closed On"] = pd.to_datetime(df_raw["Closed On"], errors='coerce')

    mask_created = (df_raw["Created On"] >= start_date) & (df_raw["Created On"] <= end_date)
    mask_closed = (df_raw["Closed On"] >= start_date) & (df_raw["Closed On"] <= end_date)

    tickets_received = df_raw.loc[mask_created].groupby(df_raw["Created On"].dt.date).size()
    tickets_closed = df_raw.loc[mask_closed].groupby(df_raw["Closed On"].dt.date).size()

    daily_tickets = pd.DataFrame({
        "Tickets Received": tickets_received,
        "Tickets Closed": tickets_closed
    }).fillna(0).astype(int)

    all_dates = pd.date_range(start=start_date, end=end_date)
    daily_tickets = daily_tickets.reindex(all_dates.date, fill_value=0)

    daily_tickets = daily_tickets.reset_index().rename(columns={"index": "Date"})

    total_received = daily_tickets["Tickets Received"].sum()
    total_closed = daily_tickets["Tickets Closed"].sum()

    totals = {
        "Date": "Total",
        "Tickets Received": total_received,
        "Tickets Closed": total_closed
    }
    daily_tickets.loc[len(daily_tickets)] = totals

    # Track grand totals
    grand_total_received += total_received
    grand_total_closed += total_closed

    source_name = os.path.splitext(os.path.basename(file))[0]
    daily_tickets["Source"] = source_name

    # Add a header (filename) row
    final_output_rows.append([source_name, "", "", ""])  # extra column for spacing
    final_output_rows.append(["Date", "Tickets Received", "Tickets Closed", "Source"])
    final_output_rows.extend(daily_tickets.values.tolist())
    final_output_rows.append([])  # blank row for spacing

# Add Grand Total at the end
final_output_rows.append(["Grand Total", "", "", ""])
final_output_rows.append(["", grand_total_received, grand_total_closed, ""])

# Save to CSV
final_df = pd.DataFrame(final_output_rows)
final_df.to_csv("all_tickets_ordered_with_grand_total.csv", index=False, header=False)

print("🎉 All files cleaned, combined, and saved with totals as 'all_tickets_ordered_with_grand_total.csv'!")
