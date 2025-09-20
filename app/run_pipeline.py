import subprocess
import webbrowser

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
    """Start uvicorn on port 8000 for endpoint.py"""
    print("test1")
    subprocess.run(["uvicorn", "endpoint:app", "--reload", "--port", "8000"])

    
def start_webprocess():
    print("Opening new browser")
    browser = webbrowser.get('chrome')
    browser.open_new("http://127.0.0.1:8000/docs")

if __name__ == "__main__":
    free_port_8000()
    start_webprocess()
    start_uvicorn()