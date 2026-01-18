import streamlit as st
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import pandas as pd
from io import BytesIO

# ----------------------
# CONFIG
# ----------------------
BUCKET_NAME = "devopscommunitypythonfodevops"

s3 = boto3.client(
    's3',
    region_name='us-east-1',
    aws_access_key_id="",
    aws_secret_access_key="",
)

st.title("📂 Streamlit S3 File Manager for BA")

# ----------------------
# UPLOAD FILE
# ----------------------
st.header("⬆️ Upload your file to S3")
upload_file = st.file_uploader("Choose a file to upload", type=["csv", "txt", "xlsx", "jpg", "png"])
if upload_file:
    try:
        s3.upload_fileobj(upload_file, BUCKET_NAME, upload_file.name)
        st.success(f"✅ File '{upload_file.name}' uploaded successfully!")
    except NoCredentialsError:
        st.error("❌ AWS credentials not available")
    except ClientError as e:
        st.error(f"❌ Error: {e}")

# ----------------------
# LIST FILES
# ----------------------
st.header("📄 List & Manage Files")
search_query = st.text_input("Search files by name")

try:
    contents = s3.list_objects_v2(Bucket=BUCKET_NAME)
    if "Contents" in contents:
        files = contents['Contents']
        
        for obj in files:
            filename = obj['Key']
            file_size_kb = round(obj['Size'] / 1024, 2)
            last_modified = obj['LastModified']
            
            if search_query.lower() in filename.lower():
                with st.expander(f"{filename} | {file_size_kb} KB | Last Modified: {last_modified}"):
                    col1, col2, col3 = st.columns([3,1,1])
                    
                    if col1.button("Preview", key="preview_" + filename):
                        # Preview CSV or text files
                        file_obj = s3.get_object(Bucket=BUCKET_NAME, Key=filename)
                        if filename.endswith(".csv"):
                            df = pd.read_csv(file_obj['Body'])
                            st.dataframe(df.head(10))
                        elif filename.endswith(".txt"):
                            content = file_obj['Body'].read().decode("utf-8")
                            st.text(content[:1000])
                        else:
                            st.info("Preview not available for this file type")
                    
                    if col2.button("Download", key="download_" + filename):
                        file_obj = s3.get_object(Bucket=BUCKET_NAME, Key=filename)
                        st.download_button(
                            label="Download",
                            data=file_obj['Body'].read(),
                            file_name=filename
                        )
                    
                    if col3.button("Delete", key="delete_" + filename):
                        s3.delete_object(Bucket=BUCKET_NAME, Key=filename)
                        st.success(f"✅ File '{filename}' deleted successfully")
                        st.experimental_rerun()
    else:
        st.info("No files found in S3 bucket.")
except NoCredentialsError:
    st.error("❌ AWS credentials not available")
except ClientError as e:
    st.error(f"❌ Error: {e}")
