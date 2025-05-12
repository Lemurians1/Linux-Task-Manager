# Linux Task Manager

This is a lightweight, PyQt5-based Task Manager for Linux that displays real-time process information and memory usage graphs. It allows you to monitor running processes, view system memory over time, and terminate selected processes—all in a modern GUI.

## Features

* **Process Monitoring**: Lists PID, process name, status, CPU%, memory%, and thread count.
* **End Task**: Select and terminate a process with graceful termination (SIGTERM) and forced kill (SIGKILL) fallback.
* **Memory Graph**: Live-updating RAM usage graph (last 2 minutes, updated every 2 seconds).
* **Tabbed UI**: Separate tabs for process table and memory graph.
* **No GPU/OpenGL Dependencies**: Runs in software rendering mode to maximize compatibility.

## Requirements

* Python 3.6+
* PyQt5
* psutil
* matplotlib

On Debian/Ubuntu-based systems:

```bash
sudo apt-get update
sudo apt-get install python3 python3-pyqt5 python3-psutil python3-matplotlib
```

Or with pip:

```bash
pip install PyQt5 psutil matplotlib
```

## Installation

1. Clone this repository or download the script:

   ```bash
   ```

cd linux-task-manager

````
2. Ensure dependencies are installed (see Requirements above).

## Usage

Run the application:
```bash
python3 task_manager.py
````

The main window includes two tabs:

1. **Processes**: Displays all running processes sorted by CPU usage. Select a row and click **End Task** to terminate.
2. **Memory Graph**: Shows live RAM usage (%) over time.

## Code Structure

* `task_manager.py`: Main application script containing:

  * `TaskManager` Qt widget class
  * Process table and kill logic
  * Matplotlib integration for memory graph
  * QTimer for periodic updates

## Security & Permissions

* You need sufficient permissions to terminate processes (may require sudo for system processes).
* The app runs under the current user; it does not escalate privileges.

## Troubleshooting

* **Blank Window / Crash**: Ensure `XDG_RUNTIME_DIR` and `LIBGL_ALWAYS_SOFTWARE` environment variables are set as in the script.
* **Permission Denied** when killing: Run as a user with appropriate permissions or avoid system-critical processes.

## Contributing

1. Fork the repository.
2. Create a branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m "Add new feature"`.
4. Push to the branch: `git push origin feature-name`.
5. Open a Pull Request.

