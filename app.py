import streamlit as st
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io
import os
from datetime import datetime

st.set_page_config(
    page_title="PLP-Support Data Processing",
    layout="wide",
    page_icon="PLP.png"
)

# Centered logo and title at the top
col1, col2, col3 = st.columns([1,2,1])
with col1:
    st.write("")
with col2:
    st.image("PLP.png", width=120)
with col3:
    st.write("")
st.markdown(
    """
    <div style='display: flex; flex-direction: column; align-items: center; margin-bottom: 1em;'>
        <h1 style='color: #008080; margin-top: 0.5em; font-size: 2.5rem;'>PLP Support Data Processing</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Centered, smaller st.title
st.markdown(
    """
    <div style='display: flex; justify-content: center; align-items: center; margin-bottom: 0.5em;'>
        <span style='color: #008080; font-size: 1.6rem; font-weight: 600;'>📊 PLP Support Data Processing</span>
    </div>
    """,
    unsafe_allow_html=True
)

# Custom theme colors for light mode and UI elements
st.markdown(
    """
    <style>
    body, .stApp {
        background-color: #f9f9f9 !important;
        color: #222 !important;
    }
    .stApp h1 {
        color: #008080 !important;
        font-size: 2.5rem !important;
        text-align: center !important;
    }
    .stApp .stMarkdown h2, .stApp h2, .stApp .stHeader, .stApp .stMarkdown h3, .stApp h3 {
        color: #008080 !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        margin-top: 1.2em !important;
        margin-bottom: 0.7em !important;
        text-align: center !important;
    }
    .stApp .stButton>button {
        background-color: #009688 !important;
        color: #fff !important;
        border-radius: 6px;
        border: none;
        font-weight: bold;
        transition: background 0.2s;
    }
    .stApp .stButton>button:hover {
        background-color: #008080 !important;
        color: #fff !important;
    }
    .stApp .stDownloadButton>button {
        background-color: #009688 !important;
        color: #fff !important;
        border-radius: 6px;
        border: none;
        font-weight: bold;
        transition: background 0.2s;
    }
    .stApp .stDownloadButton>button:hover {
        background-color: #008080 !important;
        color: #fff !important;
    }
    .stApp .stDataFrame, .stApp .stTable {
        background-color: #fff !important;
        border-radius: 8px;
        border: 1px solid #eee;
    }
    /* Light blue background for file upload drag-and-drop boxes */
    .stApp .stFileUploader, .stApp .stFileUploader label {
        background-color: #e3f2fd !important;
        color: #008080 !important;
        border-radius: 8px !important;
        padding: 0.5em 1em !important;
        font-weight: bold !important;
        margin-bottom: 0.5em !important;
        display: inline-block !important;
        border: 1.5px solid #b3e5fc !important;
    }
    .stApp .stFileUploader label:hover {
        background-color: #1976d2 !important;
        color: #fff !important;
    }
    /* Light blue for date input and calendar widgets */
    .stApp .stDateInput input, .stApp .stDateInput, .stApp .stDateInput .st-b3, .stApp .stDateInput .st-b4 {
        background-color: #e3f2fd !important;
        color: #008080 !important;
        border-radius: 6px !important;
        border: 1.5px solid #b3e5fc !important;
    }
    .stApp .stDateInput input:focus {
        border: 2px solid #008080 !important;
        outline: none !important;
    }
    .stApp .stDateInput svg {
        color: #008080 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Section 1: Upload CSVs for Aggregation ---
st.header("1️⃣ Upload Ticket CSV Files for Aggregation")

required_files = [
    "List of Tickets login.csv",
    "List of Tickets live classes.csv",
    "List of Tickets content.csv",
    "List of Tickets progress.csv",
    "List of Tickets certificates.csv",
    "List of Tickets advanced.csv"
]

uploaded_files = {}
cols = st.columns(3)
for i, fname in enumerate(required_files):
    uploaded_files[fname] = cols[i % 3].file_uploader(f"Upload {fname}", type="csv", key=fname)

# --- Section 2: Aggregation Buttons ---
st.header("2️⃣ Aggregate Data and Download Results")

# Date input fields
col_date1, col_date2 = st.columns(2)
def_date_start = datetime(2025, 7, 5)
def_date_end = datetime(2025, 7, 12)
with col_date1:
    start_date = st.date_input("Start Date", value=def_date_start, key="start_date")
with col_date2:
    end_date = st.date_input("End Date", value=def_date_end, key="end_date")

# Two columns for aggregation
col_left, col_right = st.columns(2)

if all(uploaded_files.values()):
    # Read all uploaded files into DataFrames
    dfs = {fname: pd.read_csv(uploaded_files[fname]) for fname in required_files}
    date_list = [d.date() for d in pd.date_range(start=start_date, end=end_date)]

    # --- daily data.py logic ---
    with col_left:
        st.subheader("Daily Data")
        if st.button("Aggregate by Day (Download daily data.csv)", key="agg_day"):
            total_received_by_date = pd.Series(0, index=date_list)
            total_closed_by_date = pd.Series(0, index=date_list)
            for df in dfs.values():
                df["Created On"] = df["Created On"].str.replace(" +0000 UTC", "", regex=False)
                df["Closed On"] = df["Closed On"].str.replace(" +0000 UTC", "", regex=False)
                df["Created On"] = pd.to_datetime(df["Created On"], errors='coerce')
                df["Closed On"] = pd.to_datetime(df["Closed On"], errors='coerce')
                # Fix: Include the entire end date by using end_date + 1 day for the upper bound
                mask_created = (df["Created On"].dt.date >= start_date) & (df["Created On"].dt.date <= end_date)
                mask_closed = (df["Closed On"].dt.date >= start_date) & (df["Closed On"].dt.date <= end_date)
                tickets_received = df.loc[mask_created].groupby(df["Created On"].dt.date).size()
                tickets_closed = df.loc[mask_closed].groupby(df["Closed On"].dt.date).size()
                total_received_by_date = total_received_by_date.add(tickets_received, fill_value=0).astype(int)
                total_closed_by_date = total_closed_by_date.add(tickets_closed, fill_value=0).astype(int)
            summary_df = pd.DataFrame({
                "Day": date_list,
                "Ticket Created": total_received_by_date.values,
                "Ticket Closed": total_closed_by_date.values
            })
            summary_df.loc[len(summary_df)] = ["Total", summary_df["Ticket Created"].sum(), summary_df["Ticket Closed"].sum()]
            csv_bytes = summary_df.to_csv(index=False).encode()
            st.success("Aggregated by day!")
            st.download_button("Download daily data.csv", csv_bytes, file_name="daily data.csv", mime="text/csv")

    # --- category data.py logic ---
    with col_right:
        st.subheader("Category Data")
        if st.button("Aggregate by Category (Download category data.csv)", key="agg_cat"):
            final_output_rows = []
            grand_total_received = 0
            grand_total_closed = 0
            for fname, df in dfs.items():
                df["Created On"] = df["Created On"].str.replace(" +0000 UTC", "", regex=False)
                df["Closed On"] = df["Closed On"].str.replace(" +0000 UTC", "", regex=False)
                df["Created On"] = pd.to_datetime(df["Created On"], errors='coerce')
                df["Closed On"] = pd.to_datetime(df["Closed On"], errors='coerce')
                # Fix: Include the entire end date by using end_date + 1 day for the upper bound
                mask_created = (df["Created On"].dt.date >= start_date) & (df["Created On"].dt.date <= end_date)
                mask_closed = (df["Closed On"].dt.date >= start_date) & (df["Closed On"].dt.date <= end_date)
                tickets_received = df.loc[mask_created].groupby(df["Created On"].dt.date).size()
                tickets_closed = df.loc[mask_closed].groupby(df["Closed On"].dt.date).size()
                daily_tickets = pd.DataFrame({
                    "Ticket Created": tickets_received,
                    "Ticket Closed": tickets_closed
                }).fillna(0).astype(int)
                daily_tickets = daily_tickets.reindex([d.date() for d in pd.date_range(start=start_date, end=end_date)], fill_value=0)
                daily_tickets = daily_tickets.reset_index().rename(columns={"index": "Day"})
                total_received = daily_tickets["Ticket Created"].sum()
                total_closed = daily_tickets["Ticket Closed"].sum()
                totals = {
                    "Day": "Total",
                    "Ticket Created": total_received,
                    "Ticket Closed": total_closed
                }
                daily_tickets.loc[len(daily_tickets)] = totals
                grand_total_received += total_received
                grand_total_closed += total_closed
                source_name = fname.replace("List of Tickets ", "").replace(".csv", "")
                daily_tickets["Source"] = source_name
                final_output_rows.append([source_name, "", "", ""])  # header row
                final_output_rows.append(["Day", "Ticket Created", "Ticket Closed", "Source"])
                final_output_rows.extend(daily_tickets.values.tolist())
                final_output_rows.append([])
            final_output_rows.append(["Grand Total", "", "", ""])
            final_output_rows.append(["", grand_total_received, grand_total_closed, ""])
            final_df = pd.DataFrame(final_output_rows)
            csv_bytes = final_df.to_csv(index=False, header=False).encode()
            st.success("Aggregated by category!")
            col1, col2 = st.columns(2)
            with col1:
                st.download_button("Download category data.csv", csv_bytes, file_name="category data.csv", mime="text/csv")
            with col2:
                # Refined download button logic for category data
                def get_refined_csv_and_df():
                    # Use the upload input keys for mapping, not the uploaded file's name
                    upload_keys = [
                        "List of Tickets login.csv",
                        "List of Tickets live classes.csv",
                        "List of Tickets content.csv",
                        "List of Tickets progress.csv",
                        "List of Tickets certificates.csv",
                        "List of Tickets advanced.csv"
                    ]
                    categories = ["login", "live classes", "content", "progress", "certificates", "advanced"]
                    refined_rows = []
                    for key, cat in zip(upload_keys, categories):
                        df = dfs[key]
                        if "Created On" not in df.columns or "Closed On" not in df.columns:
                            refined_rows.append([cat, 0, 0])
                            continue
                        df["Created On"] = df["Created On"].astype(str).str.replace(" +0000 UTC", "", regex=False)
                        df["Closed On"] = df["Closed On"].astype(str).str.replace(" +0000 UTC", "", regex=False)
                        df["Created On"] = pd.to_datetime(df["Created On"], errors='coerce')
                        df["Closed On"] = pd.to_datetime(df["Closed On"], errors='coerce')
                        # Fix: Include the entire end date by using end_date + 1 day for the upper bound
                        mask_created = (df["Created On"].dt.date >= start_date) & (df["Created On"].dt.date <= end_date)
                        mask_closed = (df["Closed On"].dt.date >= start_date) & (df["Closed On"].dt.date <= end_date)
                        total_created = mask_created.sum()
                        total_closed = mask_closed.sum()
                        refined_rows.append([cat, total_created, total_closed])
                    refined = pd.DataFrame(refined_rows)
                    refined.columns = ["Issue Category", "Ticket Created", "Ticket Closed"]
                    return refined, refined.to_csv(index=False).encode()
                refined_df, refined_csv = get_refined_csv_and_df()
                st.dataframe(refined_df)
                st.download_button(
                    "Download Refined Data",
                    refined_csv,
                    file_name="refined_category_data.csv",
                    mime="text/csv"
                )
else:
    st.info("Please upload all six required CSV files to enable aggregation.")

# --- Section 3: Visualization: Bar Graph ---
st.header("3️⃣ Generate Category Data Bar Graph")
bar_data_file = st.file_uploader("Upload refined category data", type="csv", key="bargraph")
if bar_data_file:
    bar_df = pd.read_csv(bar_data_file)
    if set(["Issue Category", "Ticket Created", "Ticket Closed"]).issubset(bar_df.columns):
        categories = bar_df["Issue Category"].tolist()
        created = pd.Series(pd.to_numeric(bar_df["Ticket Created"], errors='coerce')).fillna(0).astype(int).tolist()
        closed = pd.Series(pd.to_numeric(bar_df["Ticket Closed"], errors='coerce')).fillna(0).astype(int).tolist()
        bar_width = 0.35
        r1 = np.arange(len(categories))
        r2 = [x + bar_width for x in r1]
        fig, ax = plt.subplots(figsize=(12, 7))
        ax.bar(r1, created, color='#850101', width=bar_width, label='Ticket Created')
        ax.bar(r2, closed, color='#009688', width=bar_width, label='Ticket Closed')
        ax.set_xlabel('Issue Category', fontweight='bold')
        ax.set_ylabel('Number of Tickets', fontweight='bold')
        ax.set_title('Ticket Created and Ticket Closed by Issue Category', fontweight='bold')
        ax.set_xticks([r + bar_width / 2 for r in range(len(categories))])
        ax.set_xticklabels(categories, rotation=45, ha='right')
        ax.legend()
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        st.pyplot(fig)
        img_bytes = io.BytesIO()
        fig.savefig(img_bytes, format='png')
        st.download_button("Download Bar Graph Image", img_bytes.getvalue(), file_name="tickets_bar_graph.png", mime="image/png")
    else:
        st.error("CSV must have columns: Issue Category, Ticket Created, Ticket Closed.")

# --- Section 4: Visualization: Line Graph ---
st.header("4️⃣ Generate Daily Data Line Graph")

# Only allow manual upload for line graph data
upload_col = st.columns([1])[0]
line_data_file = upload_col.file_uploader("Upload downloaded daily data", type="csv", key="linegraph")
daily_data_df = None
if line_data_file:
    daily_data_df = pd.read_csv(line_data_file)
    # Remove the "Total" row if it exists - do this immediately after reading
    daily_data_df = daily_data_df[daily_data_df["Day"] != "Total"]

if daily_data_df is not None and len(daily_data_df) > 0:
    if set(["Day", "Ticket Created", "Ticket Closed"]).issubset(daily_data_df.columns):
        days = daily_data_df["Day"].tolist()
        created = pd.Series(pd.to_numeric(daily_data_df["Ticket Created"], errors='coerce')).fillna(0).astype(int).tolist()
        closed = pd.Series(pd.to_numeric(daily_data_df["Ticket Closed"], errors='coerce')).fillna(0).astype(int).tolist()
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(days, created, color='#850101', marker='o', linestyle='-', label='Ticket Created')
        ax.plot(days, closed, color='#009688', marker='o', linestyle='-', label='Ticket Closed')
        ax.set_xlabel('Day', fontweight='bold')
        ax.set_ylabel('Number of Tickets', fontweight='bold')
        ax.set_title('Ticket Created and Closed by Day', fontweight='bold')
        ax.set_xticklabels(days, rotation=45, ha='right')
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        ax.legend()
        plt.tight_layout()
        st.pyplot(fig)
        img_bytes = io.BytesIO()
        fig.savefig(img_bytes, format='png')
        st.download_button("Download Line Graph Image", img_bytes.getvalue(), file_name="tickets_created_closed_line_graph.png", mime="image/png")
    else:
        st.error("CSV must have columns: Day, Ticket Created, Ticket Closed.") 