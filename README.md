<h1 align="center">📊 PLP-Support Data Processing 🛠️</h1>

This repository houses 🐍 Python scripts designed to efficiently process ticket data extracted from multiple 📂 CSV files. These scripts provide a clear overview of ticket activity by summarizing the number of tickets 📥 **received** and 📤 **closed** within a specific timeframe, offering valuable insights through aggregated results.

---

## 📂 Files Overview

Here's a breakdown of the scripts included:

**1. ⚙️ `groups.py`**

* **Purpose:** Processes six distinct CSV files to calculate daily ticket counts (both received and closed). It also computes the total counts for each individual file and a comprehensive grand total across all files.
* **Output:** Generates a CSV file named `all_tickets_ordered_with_grand_total.csv`, containing:
    * 📅 A detailed daily breakdown of tickets for each input file.
    * 📈 The total number of tickets received and closed for each individual file.
    * 💯 Grand totals encompassing all processed files.
* **✨ Key Features:**
    * 🧹 Cleans and standardizes date formats.
    * 🗓️ Aggregates ticket data on a daily basis for the period **2025-04-04** to **2025-04-12**.

**2. 🗓️ `date.py`**

* **Purpose:** Provides a summary of the total tickets received and closed across all input files within a defined date range.
* **Output:** Creates a CSV file named `total_tickets_by_date.csv`, which includes:
    * 📊 Daily ticket counts aggregated from all input files.
    * <tfoot> A concluding row summarizing the overall total of tickets received and closed.
* **✨ Key Features:**
    * 🧹 Cleans and standardizes date formats.
    * 🗓️ Aggregates ticket data for the period **2025-04-04** to **2025-04-12**.

**3. 📊 `Issue-Category-Bargraph`**

* **Purpose:** Visualizes the number of tickets created and closed for each issue category using a bar chart.
* **Output:** Saves the bar graph showing "Tickets Created" and "Tickets Closed" by issue category as an image file (`tickets_bar_graph.png`).
* **✨ Key Features:**
    * Handles categories such as Login, Live Classes, Content, Progress, Certificates, Payment, and Advanced Courses.
    * Converts non-numeric data to zero for accurate plotting.
    * Enhances readability with color, labeling, and layout adjustments.

**4. 📈 `TicketsClosed by Date LineGraph`**

* **Purpose:** Plots a line graph showing the number of tickets created and closed for each day over a week.
* **Output:** Saves the line graph as an image file (`tickets_created_closed_line_graph.png`).
* **✨ Key Features:**
    * Displays daily trends for both ticket creation and closure.
    * Adds visual clarity with color, markers, legends, and grid lines.
    * Ensures readability with rotated x-axis labels and tight layout.

---

## ⚙️ Prerequisites

* **🐍 Python Version:** 3.x
* **📦 Dependencies:**
    * `pandas` - A powerful data analysis and manipulation library.
    * `matplotlib` - For generating visualizations.
        ```bash
        pip install pandas matplotlib
        ```

---

## 🚀 How to Run

Follow these steps to execute the scripts:

**🏃‍♂️ Run Locally:**

1.  Ensure all your CSV files are located in the **same directory** as the Python scripts (`groups.py` and `date.py`).
2.  Open your terminal or command prompt.
3.  Navigate to the directory containing the scripts.
4.  Execute either `groups.py` or `date.py` using the Python interpreter:
    ```bash
    python groups.py
    ```
    or
    ```bash
    python date.py
    ```
5.  For the visualization scripts, run:
    ```bash
    python Issue-Category-Bargraph
    python "TicketsClosed by Date LineGraph"
    ```

**💻 Run in Notebooks (Jupyter/Colab):**

1.  Open a Jupyter Notebook or Google Colab environment.
2.  **Upload** all the necessary script and data files to the working directory of your notebook.
3.  You can then run the script content directly within the notebook cells.

---

## 📤 Outputs

* Executing `groups.py` will generate the file: `all_tickets_ordered_with_grand_total.csv`.
* Executing `date.py` will generate the file: `total_tickets_by_date.csv`.
* Executing `Issue-Category-Bargraph` will generate: `tickets_bar_graph.png`.
* Executing `TicketsClosed by Date LineGraph` will generate: `tickets_created_closed_line_graph.png`.

---

## 📝 Notes
