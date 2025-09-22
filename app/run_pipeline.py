import subprocess

# def free_port_8000():
#     """Kill any uvicorn/python process using port 8000"""
#     try:
#         output = subprocess.check_output(["lsof", "-i", ":8000"])
#         lines = output.decode().strip().split("\n")[1:] 
#         for line in lines:
#             if "uvicorn" in line or "python" in line:
#                 pid = line.split()[1]
#                 print(f"Killing process {pid} using port 8000")
#                 subprocess.run(["kill", "-9", pid])
#     except subprocess.CalledProcessError:
#         print("Port 8000 is already free.")

# def start_uvicorn():
#     print("TASK - Starting FastAPI (uvicorn)...")
#     subprocess.Popen(["uvicorn", "endpoint:app", "--port", "8000"])
    
# def start_frontend():
#     print("TASK - Starting Streamlit app...")
#     subprocess.Popen(["streamlit", "run", "frontend.py"])


# if __name__ == "__main__":
#     free_port_8000()
#     start_uvicorn()
#     start_frontend()

# def start_uvicorn():
#     print("TASK - Starting FastAPI (uvicorn)...")
#     subprocess.Popen(["uvicorn", "endpoint:app", "--host", "0.0.0.0", "--port", "8000"])
    
# def start_frontend():
#     print("TASK - Starting Streamlit app...")
#     subprocess.Popen(["streamlit", "run", "frontend.py", "--server.port=8501",
#         "--server.address=0.0.0.0"])


# if __name__ == "__main__":
#     start_uvicorn()
#     start_frontend()
    
    
    
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

# Registreer de signal handler voor nette shutdown
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)  # Dit is wat Docker gebruikt!

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
        "--server.port=8501",
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
