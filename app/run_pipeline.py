import subprocess

def free_port_8000():
    """Kill any uvicorn/python process using port 8000"""
    try:
        output = subprocess.check_output(["lsof", "-i", ":8000"])
        lines = output.decode().strip().split("\n")[1:] 
        for line in lines:
            if "uvicorn" in line or "python" in line:
                pid = line.split()[1]
                print(f"Killing process {pid} using port 8000")
                subprocess.run(["kill", "-9", pid])
    except subprocess.CalledProcessError:
        print("Port 8000 is already free.")

def start_uvicorn():
    print("TASK - Starting FastAPI (uvicorn)...")
    subprocess.Popen(["uvicorn", "endpoint:app", "--port", "8000"])
    
def start_frontend():
    print("TASK - Starting Streamlit app...")
    subprocess.Popen(["streamlit", "run", "frontend.py"])


if __name__ == "__main__":
    free_port_8000()
    start_uvicorn()
    start_frontend()
