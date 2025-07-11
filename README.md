<h1 align="center">📊 PLP-Support Data Processing 🛠️</h1>

This repository houses 🐍 Python scripts designed to efficiently process ticket data extracted from multiple 📂 CSV files of closed and created tickets. These scripts provide a clear overview of ticket activity by summarizing the number of tickets 📥 **received** and 📤 **closed** within a specific timeframe, offering valuable insights through aggregated results.

**Additionaly** 
There are two files that provide a visual analysis of the aggregated data.

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
    * 🗓️ Aggregates ticket data on a daily basis for the weekly period adjusted in the date inputs. e.g. **2025-06-04** to **2025-04-12**.

**2. 🗓️ `date.py`**

* **Purpose:** Provides a summary of the total tickets received and closed across all input files within a defined date range.
* **Output:** Creates a CSV file named `total_tickets_by_date.csv`, which includes:
    * 📊 Daily ticket counts aggregated from all input files.
    * <tfoot> A concluding row summarizing the overall total of tickets received and closed.
* **✨ Key Features:**
    * 🧹 Cleans and standardizes date formats.
    * 🗓️ Aggregates ticket data for the period adjusted in the date inpute e.g. **2025-04-04** to **2025-04-12**.

**3. bargraph:**
   * provides a visualization of the tickets closed by category issue.
   * 
---

## ⚙️ Prerequisites

* **🐍 Python Version:** 3.x
* **📦 Dependencies:**
    * `pandas` - A powerful data analysis and manipulation library.
        ```bash
        pip install pandas
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

**💻 Run in Notebooks (Jupyter/Colab):**

1.  Open a Jupyter Notebook or Google Colab environment.
2.  **Upload** all the necessary CSV files to the working directory of your notebook.
3.  You can then run the script content directly within the notebook cells.

---

## 📤 Outputs

* Executing `groups.py` will generate the file: `all_tickets_ordered_with_grand_total.csv`.
* Executing `date.py` will generate the file: `total_tickets_by_date.csv`.

---

## 📝 Notes

* ⚠️ Please ensure that your CSV files are correctly formatted and contain columns named **`Created On`** and **`Closed On`**.
* ✏️ If you need to analyze data for a different time period, you can easily modify the date range directly within the scripts.

---

**❗ Important Note:**

* There were brief issues encountered where, to ensure accurate data representation for a specific previous date, it was necessary to include one additional day in the date range during processing. Please be aware of this potential anomaly when interpreting the results.
