import tkinter as tk
from tkinter import ttk
import socket
import psutil
import threading
import time
import cpuinfo # For CPU name

# Attempt to import GPUtil for GPU info
try:
    import GPUtil
    gpus_available = True
except ImportError:
    gpus_available = False
    print("GPUtil library not found. GPU information will not be available.")
    print("Install it using: pip install GPUtil")
except Exception as e:
    gpus_available = False
    print(f"An error occurred importing GPUtil: {e}")
    print("GPU information might not be available.")


# --- Data Fetching Functions ---

def get_ip_address():
    """Gets the primary local IP address."""
    try:
        hostname = socket.gethostname()
        # Try getting IP associated with hostname first
        ip_address = socket.gethostbyname(hostname)

        # If it's loopback, try the socket connection trick to find a non-loopback interface
        if ip_address.startswith("127."):
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(0.1) # Short timeout
            try:
                # Doesn't actually have to connect, just initiates the process
                s.connect(('10.254.254.254', 1))
                ip_address = s.getsockname()[0]
            except Exception:
                # If trick fails, fallback to the hostname associated IP
                ip_address = socket.gethostbyname(hostname) # Re-fetch original
            finally:
                s.close()
        return ip_address
    except socket.gaierror:
        return "N/A (Network Error)"
    except Exception as e:
        print(f"IP Address Error: {e}")
        return "N/A (Error)"

def get_cpu_info():
    """Gets CPU name and current usage percentage."""
    try:
        # Get CPU Name using py-cpuinfo
        info = cpuinfo.get_cpu_info()
        cpu_name = info.get('brand_raw', 'N/A')
    except Exception as e:
        print(f"CPU Name Error: {e}")
        cpu_name = "N/A (Error getting name)"

    # Get CPU Usage using psutil
    try:
        cpu_percent = psutil.cpu_percent(interval=0.1) # Small interval for responsiveness
    except Exception as e:
        print(f"CPU Usage Error: {e}")
        cpu_percent = "N/A"

    return cpu_name, cpu_percent

def get_ram_info():
    """Gets total RAM and current usage percentage."""
    try:
        memory = psutil.virtual_memory()
        total_ram_gb = memory.total / (1024**3) # Bytes to GB
        ram_percent = memory.percent
        return f"{total_ram_gb:.2f} GB", ram_percent
    except Exception as e:
        print(f"RAM Info Error: {e}")
        return "N/A", "N/A"

def get_gpu_info():
    """Gets GPU name and current usage percentage (if GPUtil available/compatible)."""
    if not gpus_available:
        return "N/A (GPUtil unavailable)", "N/A"

    try:
        gpus = GPUtil.getGPUs()
        if not gpus:
            # GPUtil might be installed but no supported (usually NVIDIA) GPU found
            return "N/A (No supported GPU found)", "N/A"

        # For simplicity, display info for the first GPU found
        gpu = gpus[0]
        gpu_name = gpu.name
        gpu_load = gpu.load * 100 # load is 0.0-1.0
        # Optional: Add Memory Usage
        # gpu_mem_used = gpu.memoryUsed
        # gpu_mem_total = gpu.memoryTotal
        # gpu_mem_percent = (gpu_mem_used / gpu_mem_total) * 100 if gpu_mem_total else 0
        # return gpu_name, f"{gpu_load:.1f}% Load, {gpu_mem_percent:.1f}% VRAM"

        return gpu_name, f"{gpu_load:.1f}%"

    except Exception as e:
        # Catch potential errors during GPU query (e.g., driver issues)
        print(f"GPU Info Error: {e}")
        return f"N/A (Error querying GPU)", "N/A"


# --- GUI Application Class ---

class SystemMonitorApp:
    def __init__(self, root):
        self.root = root
        root.title("System Monitor")
        root.geometry("400x250") # Adjust size as needed
        root.resizable(False, False)

        # Style
        self.style = ttk.Style()
        self.style.theme_use('clam') # Or 'vista', 'xpnative', 'winnative'

        # --- Variables to hold data ---
        self.ip_var = tk.StringVar(value="Fetching...")
        self.cpu_name_var = tk.StringVar(value="Fetching...")
        self.cpu_usage_var = tk.StringVar(value="Fetching...")
        self.ram_total_var = tk.StringVar(value="Fetching...")
        self.ram_usage_var = tk.StringVar(value="Fetching...")
        self.gpu_name_var = tk.StringVar(value="Fetching...")
        self.gpu_usage_var = tk.StringVar(value="Fetching...")

        # --- GUI Layout ---
        frame = ttk.Frame(root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Row definitions (Label, Value)
        row_defs = [
            ("IP Address:", self.ip_var),
            ("CPU Model:", self.cpu_name_var),
            ("CPU Usage:", self.cpu_usage_var),
            ("GPU Model:", self.gpu_name_var),
            ("GPU Usage:", self.gpu_usage_var),
            ("Total RAM:", self.ram_total_var),
            ("RAM Usage:", self.ram_usage_var),
        ]

        # Create and place labels
        for i, (label_text, data_var) in enumerate(row_defs):
            # Static Label
            label = ttk.Label(frame, text=label_text, font=('Segoe UI', 10, 'bold'))
            label.grid(row=i, column=0, sticky=tk.W, padx=5, pady=5)

            # Dynamic Data Label
            data_label = ttk.Label(frame, textvariable=data_var, font=('Segoe UI', 10))
            data_label.grid(row=i, column=1, sticky=tk.W, padx=5, pady=5)

        # --- Start the update loop ---
        self.update_info()

    def update_info(self):
        """Fetches new data and updates the GUI labels."""
        try:
            # Fetch data (consider running heavy tasks in a separate thread if GUI freezes)
            ip = get_ip_address()
            cpu_name, cpu_usage = get_cpu_info()
            ram_total, ram_usage = get_ram_info()
            gpu_name, gpu_usage = get_gpu_info()

            # Update StringVars (which automatically updates labels)
            self.ip_var.set(ip)
            self.cpu_name_var.set(cpu_name)
            self.cpu_usage_var.set(f"{cpu_usage:.1f}%" if isinstance(cpu_usage, (int, float)) else cpu_usage)
            self.ram_total_var.set(ram_total)
            self.ram_usage_var.set(f"{ram_usage:.1f}%" if isinstance(ram_usage, (int, float)) else ram_usage)
            self.gpu_name_var.set(gpu_name)
            self.gpu_usage_var.set(gpu_usage) # Already formatted string from get_gpu_info

        except Exception as e:
            print(f"Error during update: {e}")
            # Optionally display an error in the GUI
            # self.ip_var.set("Update Error") # Example

        # Schedule the next update (e.g., every 1000ms = 1 second)
        self.root.after(1000, self.update_info)


# --- Main Execution ---
if __name__ == "__main__":
    main_root = tk.Tk()
    app = SystemMonitorApp(main_root)
    main_root.mainloop()