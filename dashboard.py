import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
summary_df = pd.read_csv("total_tickets_by_date.csv")

# Separate totals row
data_df = summary_df[summary_df['Date'] != 'Total']
totals_row = summary_df[summary_df['Date'] == 'Total']

# Convert Date column to datetime for plotting
data_df['Date'] = pd.to_datetime(data_df['Date'])

# Page config
st.set_page_config(page_title="Tickets Dashboard", layout="centered")
st.title("📊 Support Tickets Dashboard")

# Show totals
st.markdown("### 🧾 Grand Totals")
st.metric("Total Tickets Received", int(totals_row['Tickets Received']))
st.metric("Total Tickets Closed", int(totals_row['Tickets Closed']))

# Line chart
st.markdown("### 📈 Daily Tickets Overview")
fig = px.line(data_df, x='Date', y=['Tickets Received', 'Tickets Closed'], markers=True,
              labels={'value': 'Count', 'variable': 'Ticket Status'}, title="Tickets Received vs Closed")
st.plotly_chart(fig, use_container_width=True)

# Bar chart
st.markdown("### 📊 Daily Breakdown")
fig_bar = px.bar(data_df, x='Date', y=['Tickets Received', 'Tickets Closed'], barmode='group',
                 title="Bar Chart of Tickets by Day")
st.plotly_chart(fig_bar, use_container_width=True)

# Raw data
st.markdown("### 🧾 Raw Data Table")
st.dataframe(summary_df, use_container_width=True)

st.success("Dashboard loaded successfully ✅")
