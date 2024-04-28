import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
import sqlite3

# Setup the database connection and create the table
conn = sqlite3.connect('people_count.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS counts (
    id INTEGER PRIMARY KEY,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    entering INTEGER,
    exiting INTEGER
)
''')
conn.commit()

# Function to fetch current people counts from the FastAPI server
def fetch_counts():
    try:
        response = requests.get("http://127.0.0.1:8000/counts")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching counts: {e}")
        return {"entering": 0, "exiting": 0}

# Function to insert fetched data into the database
def fetch_and_store_counts():
    counts = fetch_counts()
    cursor.execute('INSERT INTO counts (entering, exiting) VALUES (?, ?)', (counts['entering'], counts['exiting']))
    conn.commit()
    return counts

# Function to retrieve data from the database for analysis
def get_data():
    df = pd.read_sql_query("SELECT * from counts", conn)
    return df

# Streamlit UI
st.sidebar.title("Navigation")
app_mode = st.sidebar.selectbox("Choose the Option",
                                ["Real-Time Metrics", "Download Data", "Network Scanner"])

if app_mode == "Real-Time Metrics":
    st.title("Real-Time People Counter Dashboard")

    counts = fetch_and_store_counts()
    current_count = counts['entering'] - counts['exiting']
    df = get_data()

    average_entering = np.mean(df['entering'])
    average_exiting = np.mean(df['exiting'])
    peak_entering = np.max(df['entering'])
    peak_exiting = np.max(df['exiting'])
    min_entering = np.min(df['entering'])
    min_exiting = np.min(df['exiting'])

    metrics_container = st.container()
    with metrics_container:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label="Current Count", value=f"{current_count}", delta="{capacity} capacity", delta_color="inverse")
        with col2:
            st.metric("Average Entries", f"{average_entering:.2f}", delta="{capacity} capacity", delta_color="normal")
        with col3:
            st.metric("Peak Entries", f"{peak_entering}")
        with col4:
            st.metric("Minimum Entries", f"{min_entering}")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Current Exiting", f"{counts['exiting']}")
        with col2:
            st.metric("Average Exits", f"{average_exiting:.2f}")
        with col3:
            st.metric("Peak Exits", f"{peak_exiting}")
        with col4:
            st.metric("Minimum Exits", f"{min_exiting}")

elif app_mode == "Download Data":
    st.title("Download Historical Data")
    if st.button('Download CSV'):
        df = get_data()
        st.download_button(
            label="Download as CSV",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name='people_counts.csv',
            mime='text/csv',
        )

elif app_mode == "Network Scanner":
    st.title("Network MAC Address Scanner")
    if st.button("Scan Network"):
        try:
            result = subprocess.check_output(['sudo', 'arp-scan', '-l']).decode('utf-8')
            mac_addresses = re.findall(r"((?:[0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2})", result)
            unique_mac_addresses = set(mac_addresses)
            st.success(f"Number of unique devices found: {len(unique_mac_addresses)}")
            st.write("MAC Addresses:")
            st.write(unique_mac_addresses)
        except Exception as e:
            st.error(f"Error running arp-scan: {e}")
