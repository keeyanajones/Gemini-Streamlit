import streamlit as st
from google.cloud import storage
import os
import pandas as pd  # For data display (optional)

# Set GCP credentials (environment variables are best)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\sensitive_keys\youtube-bot-252900-0249d8cc2a08.json" 

storage_client = storage.Client()

# --- Streamlit UI ---
st.title("GCP Cloud Storage CRUD App")

# Bucket Selection
bucket_names = [bucket.name for bucket in storage_client.list_buckets()]
if not bucket_names:
    st.warning("No buckets found. Create one below.")
    selected_bucket = None
else:
    selected_bucket = st.selectbox("Select a bucket", bucket_names)

# --- Bucket Operations ---
st.subheader("Bucket Operations")
new_bucket_name = st.text_input("New bucket name:")
if st.button("Create Bucket"):
    try:
        bucket = storage_client.create_bucket(new_bucket_name)
        st.success(f"Bucket '{new_bucket_name}' created.")
        st.experimental_rerun()  # Refresh bucket list
    except Exception as e:
        st.error(f"Error creating bucket: {e}")

if st.button("Delete Bucket"):
    if selected_bucket:
        try:
            bucket = storage_client.bucket(selected_bucket)
            bucket.delete()
            st.success(f"Bucket '{selected_bucket}' deleted.")
            st.experimental_rerun()
        except Exception as e:
            st.error(f"Error deleting bucket: {e}")

# --- Object Operations (if a bucket is selected) ---
if selected_bucket:
    st.subheader("Object Operations in Bucket: " + selected_bucket)
    bucket = storage_client.bucket(selected_bucket)

    uploaded_file = st.file_uploader("Upload File")
    if uploaded_file:
        blob = bucket.blob(uploaded_file.name)
        blob.upload_from_file(uploaded_file)
        st.success(f"File '{uploaded_file.name}' uploaded.")

    # List Objects (with download links)
    if st.button("List Objects"):
        blobs = bucket.list_blobs()
        data = []  # For Pandas display (optional)
        for blob in blobs:
            download_link = f"https://storage.googleapis.com/{selected_bucket}/{blob.name}"  # Construct download link
            data.append({"Name": blob.name, "Size": blob.size, "Download": f'<a href="{download_link}" target="_blank">Download</a>'})
        if data:
            df = pd.DataFrame(data)
            st.write(df.to_html(escape=False), unsafe_allow_html=True) # Display with HTML for links
        else:
            st.info("No objects in this bucket.")
    
    # Delete object
    object_to_delete = st.text_input("Enter object name to delete:")
    if st.button("Delete Object"):
        try:
            blob = bucket.blob(object_to_delete)
            blob.delete()
            st.success(f"Object '{object_to_delete}' deleted.")
        except Exception as e:
            st.error(f"Error deleting object: {e}")

