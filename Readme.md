# System Monitor Application

This Python application provides a simple graphical user interface (GUI) to monitor system information, including IP address, CPU usage, RAM usage, and GPU usage (if available). It utilizes the `tkinter` library for the GUI, `psutil` for system information, `socket` for IP address retrieval, and optionally `GPUtil` for GPU information.

## Features

- Displays the local IP address.
- Shows the CPU model and current usage percentage.
- Displays the total RAM and current RAM usage percentage.
- Shows the GPU model and current usage percentage (if `GPUtil` is installed and a supported GPU is found).

## Dependencies

- Python 3.x
- `tkinter` (standard library)
- `psutil`
- `cpuinfo`
- (Optional) `GPUtil`

## Installation

1.  **Install Python:** Ensure you have Python 3.x installed on your system.
2.  **Install Dependencies:** Open a terminal or command prompt and run the following command to install the necessary libraries:

    ```bash
    pip install psutil cpuinfo
    ```

    If you want GPU information, also install `GPUtil`:

    ```bash
    pip install GPUtil
    ```

    **Note:** `GPUtil` works primarily with NVIDIA GPUs. If you have a different GPU, it might not provide accurate information.

## Usage

1.  **Save the Code:** Save the provided Python code as a `.py` file (e.g., `system_monitor.py`).
2.  **Run the Application:** Open a terminal or command prompt, navigate to the directory where you saved the file, and run the script:

    ```bash
    python system_monitor.py
    ```

    This will launch the System Monitor application window.

## Code Description

The application is structured into the following main parts:

-   **Importing Libraries:** Imports necessary libraries (`tkinter`, `psutil`, `socket`, `GPUtil`, `cpuinfo`).
-   **Data Fetching Functions:**
    -   `get_ip_address()`: Retrieves the local IP address.
    -   `get_cpu_info()`: Retrieves CPU name and usage.
    -   `get_ram_info()`: Retrieves RAM total and usage.
    -   `get_gpu_info()`: Retrieves GPU name and usage (if available).
-   **`SystemMonitorApp` Class:**
    -   Initializes the GUI with `tkinter`.
    -   Defines variables to store system information.
    -   Creates labels to display the information.
    -   `update_info()`: Periodically fetches system information and updates the labels.
    -   Uses `root.after()` to schedule the periodic update.
-   **Main Execution:**
    -   Creates the main `tkinter` window.
    -   Instantiates the `SystemMonitorApp` class.
    -   Starts the `tkinter` event loop.

## Notes

-   The application updates the system information every 1 second.
-   If `GPUtil` is not installed or no supported GPU is found, the GPU information will display "N/A".
-   Error handling is included to catch potential issues during data retrieval and display "N/A" or error messages in the GUI.
-   The GUI size and style can be customized by modifying the `geometry` and `style` attributes in the `SystemMonitorApp` class.
-   The IP address retreival is designed to handle loopback addresses, and network errors.
-   CPU name is retrieved using the `cpuinfo` library, which provides detailed information about the CPU.