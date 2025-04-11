import streamlit as st
from datetime import datetime
from graph import graphbuilder
import requests
from dotenv import load_dotenv
from utils import process_directory, process_txt
import os

# Load environment variables from .env file
load_dotenv()

# 1. Initialize session state variables if not already initialized
if "job_openings" not in st.session_state:
    st.session_state.job_openings = []  # Stores job openings data
if "trace_id" not in st.session_state:
    st.session_state.trace_id = None  # Stores trace ID for requests
if "files" not in st.session_state:
    st.session_state.files = []  # Stores uploaded files

# 2. API Setup - Set the URL and headers for API calls
JDW_API_URL = os.getenv("JDW_API_URL", "http://localhost:8090")
JDW_HEADERS = {"DIREC-AI-JDW-API-KEY": os.getenv("DIREC-AI-JDW-API-KEY")}

# Function to send job descriptions to the API
def send_job_description(job_openings):
    """Send job description data to the API"""
    try:
        payload = {
            "job_openings": job_openings  # Job openings data to send
        }
        # Make POST request to the API
        response = requests.post(f"{JDW_API_URL}/ai/jdw/v1/job_description_writer", headers=JDW_HEADERS, json=payload)
        response.raise_for_status()  # Check if the response was successful
        response_data = response.json()  # Parse the JSON response
        return st.session_state.job_openings(response_data)  # Update session state with response data
    except requests.exceptions.RequestException as e:
        st.error(f"Error sending job description: {str(e)}")  # Display error message in case of failure

# Function to retrieve a value from session state by key
def get_session_state(key):
    """Get session state value"""
    return st.session_state.job_openings.get(key, None)

# Function to format job description for display or submission
def compile_job_description(job_title, job_location, job_type, department, expiry_date, job_description):
    return f"""Job Title: {job_title}
Job Location: {job_location}
Job Type: {job_type}
Department: {department}
Job Expiry Date: {expiry_date}

Job Description: 
{job_description}
"""

# Streamlit UI components
st.title("Job Jigsaw - Job Posting Form")

# Radio button to choose between single or multiple file upload
job_description_type = st.radio("Upload TXT Files", ["Single Upload", "Multiple Upload"])

# Handling Single File Upload
if job_description_type == "Single Upload":
    txt_file = st.file_uploader("Upload a single TXT file", type="txt", accept_multiple_files=False)
    if txt_file:
        try:
            # Remove the last file from the session before adding the new one
            if st.session_state.files:
                st.session_state.files.pop()  # Removes the last file

            # Treat the uploaded file as a list, even if it's a single file
            uploaded_files = [txt_file] if not isinstance(txt_file, list) else txt_file
            
            # Process the uploaded files and add them to session state
            for txt in uploaded_files:
                processed_txt = process_txt(txt)  # Process the text file
                st.session_state.files.extend(processed_txt)  # Add processed file to session state

            # Remove duplicates based on file name
            unique_files = {item['name']: item for item in st.session_state.files}.values()
            st.session_state.files = list(unique_files)

            # Display the processed files
            st.success("File processed and added to session.")
            st.write(st.session_state.files)

        except Exception as e:
            st.error(f"Error processing file: {str(e)}")  # Display error in case of failure

# Handling Multiple File Upload
elif job_description_type == "Multiple Upload":
    folder_directory = st.text_input("Enter TXT folder PATH")  # Text input for folder directory
    if folder_directory:
        try:
            st.session_state.files.pop()  # Removes the last file
            processed_files = process_directory(folder_directory)  # Process files in the directory
            st.session_state.files.extend(processed_files)  # Add processed files to session state
            # Remove duplicates based on file name
            unique_files = {item['name']: item for item in st.session_state.files}.values()
            st.session_state.files = list(unique_files)
            st.success("Folder processed and added to session.")  # Success message
            st.write(st.session_state.files)
            
        except Exception as e:
            st.error(f"Error processing folder: {str(e)}")  # Display error in case of failure


# Video file uploader for MP4 videos
video_file = st.file_uploader("Upload a video (MP4 format)", type=["mp4"])

# Button to send the compiled job description to the API or perform other actions
if st.button("Send Compiled Job Description"):
    if job_description_type:
        jdw_graph_builder = graphbuilder()  # Initialize the graph builder
        # Call the graph builder function to process the job openings
        jdw_response = jdw_graph_builder.invoke({
            "job_openings": st.session_state.files
        })

        # Display success message and the compiled job description
        st.success("Job Description Compiled Successfully!")
        st.text_area("Compiled Job Description", jdw_response, height=200)
        st.balloons()  # Show balloons animation
    else:
        st.error("Please fill out all fields before submitting.")  # Display error if required fields are missing
