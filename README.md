# 📊 Sales Data Dashboard

An interactive Streamlit web app that allows businesses to upload, manage, and analyze their sales data with clean visualizations, editable tables, and downloadable reports. Now with user authentication!

---

## 🚀 Features

* 🔐 User login system (basic authentication)
* ⬆️ Upload and preview sales data
* ✏️ Edit records directly in-app
* ➕ Add new sales entries manually
* 📊 View key performance indicators (KPIs)
* 📍 Filter by region and customer demographics
* 📉 Interactive dashboards (Plotly visualizations)
* 📤 Export updated data as CSV or PDF

---

## 👤 Login Info

| Username | Password   |
| -------- | ---------- |
| admin    | admin123   |
| analyst  | analyst123 |

---

## 🛠 How to Run

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app**
   Start the main multipage app:

   ```bash
   streamlit run Home.py
   ```

   Or run an individual page directly:

   ```bash
   streamlit run pages/2_Add_New_Sale_Entry.py
   ```

---

## 📁 Sample CSV Format

Ensure your uploaded CSV has these columns (in any delimiter-separated format):

```
Order ID, Date, Region, Sales, Profit, Customer Age, Customer Gender, Product Category
```

Example row:

```
A101,2024-01-15,East,200.50,50.00,35,Male,Electronics
```

---

## 🧠 Notes

* The login system is session-based (no external database), designed for local or internal use.
* All dashboard features require login.
* On successful login, the session state is set; the page does not auto-reload.

---

## 🏷️ Credits

Created by **TIKO Collective**
© 2025 All rights reserved
