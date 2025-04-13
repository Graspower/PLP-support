import pandas as pd
import os

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

# Prepare date range
all_dates = pd.date_range(start=start_date, end=end_date)
date_list = all_dates.date

# Initialize total counts
total_received_by_date = pd.Series(0, index=date_list)
total_closed_by_date = pd.Series(0, index=date_list)

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

    total_received_by_date = total_received_by_date.add(tickets_received, fill_value=0).astype(int)
    total_closed_by_date = total_closed_by_date.add(tickets_closed, fill_value=0).astype(int)

# Create final DataFrame
summary_df = pd.DataFrame({
    "Date": date_list,
    "Tickets Received": total_received_by_date.values,
    "Tickets Closed": total_closed_by_date.values
})

# Add totals row
summary_df.loc[len(summary_df)] = ["Total", summary_df["Tickets Received"].sum(), summary_df["Tickets Closed"].sum()]

# Save to CSV
summary_df.to_csv("total_tickets_by_date.csv", index=False)

print("✅ Total tickets by date saved to 'total_tickets_by_date.csv'")
