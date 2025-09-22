import subprocess
import time
import signal
import sys

uvicorn_process = None
streamlit_process = None

def signal_handler(sig, frame):
    print("\nReceived shutdown signal, stopping services...")
    if uvicorn_process:
        uvicorn_process.terminate()
    if streamlit_process:
        streamlit_process.terminate()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler) 

def main():
    global uvicorn_process, streamlit_process
    
    print("Starting FastAPI (uvicorn)...")
    uvicorn_process = subprocess.Popen([
        "uvicorn", "app.endpoint:app", 
        "--host", "0.0.0.0", 
        "--port", "8000"
    ])
    
    print("Starting Streamlit app...")
    streamlit_process = subprocess.Popen([
        "streamlit", "run", "app/frontend.py",
        "--server.port=7860",
        "--server.address=0.0.0.0"
    ])
    
    try:
        while True:
            if uvicorn_process.poll() is not None:  # Check if uvicorn died
                print("Uvicorn stopped unexpectedly!")
                break
            if streamlit_process.poll() is not None:  # Check if streamlit died  
                print("Streamlit stopped unexpectedly!")
                break
            time.sleep(1)
    except:
        pass
    
    print("Cleaning up...")
    if uvicorn_process and uvicorn_process.poll() is None:
        uvicorn_process.terminate()
    if streamlit_process and streamlit_process.poll() is None:
        streamlit_process.terminate()

if __name__ == "__main__":
    main()
