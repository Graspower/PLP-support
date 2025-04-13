import pandas as pd

# Load the CSV file
df_raw = pd.read_csv("List of Tickets certificates.csv")

# Strip " +0000 UTC" from date columns
df_raw["Created On"] = df_raw["Created On"].str.replace(" +0000 UTC", "", regex=False)
df_raw["Closed On"] = df_raw["Closed On"].str.replace(" +0000 UTC", "", regex=False)

# Convert to datetime format
df_raw["Created On"] = pd.to_datetime(df_raw["Created On"], errors='coerce')
df_raw["Closed On"] = pd.to_datetime(df_raw["Closed On"], errors='coerce')

# Define the date range for filtering
start_date = pd.to_datetime("2025-04-04")
end_date = pd.to_datetime("2025-04-12")

# Filter data within the date range
mask_created = (df_raw["Created On"] >= start_date) & (df_raw["Created On"] <= end_date)
mask_closed = (df_raw["Closed On"] >= start_date) & (df_raw["Closed On"] <= end_date)

# Group by date to count tickets received and closed
tickets_received = df_raw.loc[mask_created].groupby(df_raw["Created On"].dt.date).size()
tickets_closed = df_raw.loc[mask_closed].groupby(df_raw["Closed On"].dt.date).size()

# Merge the two series into a DataFrame
daily_tickets = pd.DataFrame({
    "Tickets Received": tickets_received,
    "Tickets Closed": tickets_closed
}).fillna(0).astype(int)

# Make sure all dates in range are included
all_dates = pd.date_range(start=start_date, end=end_date)
daily_tickets = daily_tickets.reindex(all_dates.date, fill_value=0)

# Reset index to make Date a column
daily_tickets = daily_tickets.reset_index()
daily_tickets = daily_tickets.rename(columns={"index": "Date"})

# Calculate totals
totals = {
    "Date": "Total",
    "Tickets Received": daily_tickets["Tickets Received"].sum(),
    "Tickets Closed": daily_tickets["Tickets Closed"].sum()
}

# Add totals row
daily_tickets_with_total = daily_tickets.copy()
daily_tickets_with_total.loc[len(daily_tickets_with_total)] = totals

# Ensure correct column order
daily_tickets_with_total = daily_tickets_with_total[["Date", "Tickets Received", "Tickets Closed"]]

# Save the results to CSV with totals
daily_tickets_with_total.to_csv("clean_tickets_with_totals.csv", index=False)

# Print the DataFrame to confirm the output
print(daily_tickets_with_total)
