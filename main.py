
import streamlit as st      # Importing the Streamlit library for building web apps
import pandas as pd         # Importing Pandas for data manipulation and analysis
import os                   # Importing the OS module for interacting with the operating system (e.g., file handling)
from io import BytesIO      # Importing BytesIO from the io module to handle in-memory file operations (like simulating a file)

  

st.set_page_config(page_title="Data Sweeper App", layout="wide")
st.title("📀 Data Sweeper App")
st.write("This app allows you to transform your files between CSV and Excel formats with built-in data cleaning and visualization tools.")
uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"], accept_multiple_files=True)


if uploaded_file:
    for file in uploaded_file:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file format: {file_ext}")
            continue
        

        # Display the file name and size
        st.write(f"**📄 File Name:** {file.name}")
        st.write(f"**📏 File Size:** {file.size / 1024:.2f} KB")  # File size in KB


        # Display the first few rows of the dataframe
        st.write("🔎 Preview the Head of the Dataframe")
        st.dataframe(df.head())

        # Options for data cleaning
        st.subheader("⚒ Data Cleaning Options")
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write(f"Removed duplicates from {file.name}")

            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write(f"Filled missing values for {file.name}")


        # Choose the output format for conversion of the uploaded file
        st.subheader("🎯 Select Columns to Convert")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]


        # Create Some Visualizations
        st.subheader("📊 Data Visualizations")
        if st.checkbox(f"Show visualizations for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])

        # Convert the File -> CSV to Excel or Excel to CSV
        st.subheader("🔁 Convert the File")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)
            

            # Download the converted file
            st.download_button(
                label=f"⬇ Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.success(f"✅ All Files Successfully Processed")


# Source Code Available : https://github.com/Joshwen7947/Data-Sweeper-App