import streamlit as st
import requests

st.set_page_config(page_title="DataFlow Pipeline")
st.title("DataFlow Pipeline")

column1, column15, column2 = st.columns([2, 0.1, 1.6])
if "result" not in st.session_state:
    st.session_state.result = None

def show_input_area(): 
    user_input = st.file_uploader(
        "Upload Excel Dataset (.xlsx)", 
        accept_multiple_files=False, 
        type="xlsx",
        help="Upload raw Excel data for automated cleansing and transformation. Enterprise .xlsx format required for analysis."
    )
    
    output_name = st.text_input("Output Filename", placeholder="cleansed_dataset")
    if st.button("Process & Transform Data"):
        if user_input is not None and output_name != "":
            if not user_input.name.lower().endswith('.xlsx'):
                st.error("Enterprise data format required. Please upload .xlsx file.")
                return
            files = {"file": (user_input.name, user_input.getvalue(), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")}
            requests.post("http://localhost:8000/process", files=files)
            
            params = {"output_filename": output_name}
            
            response = requests.post(
                "http://localhost:8000/process", 
                files=files,
                params=params
            )
            if response:
                result = response.json()
                st.success("Data transformation completed successfully!")
                    
                st.session_state["result"] = result
                download_response = requests.get("http://localhost:8000/download-file")
                    
                if download_response.status_code == 200:
                    st.download_button(
                        label="Download output",
                        data=download_response.content,
                        file_name=f"{output_name}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    
def show_processed_info(result):
    col1, col2= st.columns(2)
    with col1:
        st.metric("Rows Processed", result["rows_in"])
    with col2:
        st.metric("Rows Output", result["rows_out"])
    st.metric("Columns", len(result["columns"]))
    if st.button("clean"):
        st.session_state["result"] = None

with column1: 
    show_input_area()   
with column2:
    if st.session_state["result"]:
        show_processed_info(st.session_state["result"])
    else:
        ""


    