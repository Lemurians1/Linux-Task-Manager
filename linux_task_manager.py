import os
import sys
import psutil
import warnings
import getpass
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QMessageBox, QHeaderView, QTabWidget
)
from PyQt5.QtCore import QTimer, Qt

# Matplotlib for RAM graph
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Suppress PyQt5 user warnings
warnings.filterwarnings("ignore", category=UserWarning, module="PyQt5")

# Set proper runtime directory for Qt (owned by current user)
user = getpass.getuser()
user_runtime_dir = f"/tmp/runtime-{user}"
os.makedirs(user_runtime_dir, mode=0o700, exist_ok=True)
os.environ["XDG_RUNTIME_DIR"] = user_runtime_dir

# Disable GPU-based OpenGL
os.environ["LIBGL_ALWAYS_SOFTWARE"] = "1"

class TaskManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Linux Task Manager")
        self.resize(900, 600)
        layout = QVBoxLayout(self)

        # Tabs
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Processes tab
        self.process_tab = QWidget()
        p_layout = QVBoxLayout(self.process_tab)
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["PID", "Name", "Status", "CPU %", "Memory %", "Threads"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        p_layout.addWidget(self.table)
        btn_layout = QHBoxLayout()
        self.kill_button = QPushButton("End Task")
        self.kill_button.clicked.connect(self.end_task)
        btn_layout.addWidget(self.kill_button)
        p_layout.addLayout(btn_layout)
        self.tabs.addTab(self.process_tab, "Processes")

        # Memory graph tab
        self.mem_tab = QWidget()
        m_layout = QVBoxLayout(self.mem_tab)
        self.fig = Figure(figsize=(5,3))
        self.canvas = FigureCanvas(self.fig)
        m_layout.addWidget(self.canvas)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("RAM Usage (%) over time")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Memory %")
        self.mem_data = []
        self.time_data = []
        self.max_points = 60
        self.tabs.addTab(self.mem_tab, "Memory Graph")

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(2000)

        self.update()

    def update(self):
        self.update_tasks()
        self.update_memory_graph()

    def update_tasks(self):
        processes = []
        for proc in psutil.process_iter(['pid','name','status','cpu_percent','memory_percent','num_threads']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
        self.table.setRowCount(len(processes))
        for row, proc in enumerate(processes):
            self.table.setItem(row,0,QTableWidgetItem(str(proc['pid'])))
            self.table.setItem(row,1,QTableWidgetItem(proc.get('name','N/A')))
            self.table.setItem(row,2,QTableWidgetItem(proc.get('status','N/A')))
            self.table.setItem(row,3,QTableWidgetItem(f"{proc['cpu_percent']:.1f}"))
            self.table.setItem(row,4,QTableWidgetItem(f"{proc['memory_percent']:.1f}"))
            self.table.setItem(row,5,QTableWidgetItem(str(proc.get('num_threads','N/A'))))

    def update_memory_graph(self):
        mem = psutil.virtual_memory().percent
        if len(self.mem_data) >= self.max_points:
            self.mem_data.pop(0)
            self.time_data.pop(0)
        self.mem_data.append(mem)
        t = len(self.time_data)*2 if self.time_data else 0
        self.time_data.append(t)
        self.ax.clear()
        self.ax.plot(self.time_data, self.mem_data)
        self.ax.set_title("RAM Usage (%) over time")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Memory %")
        self.canvas.draw()

    def end_task(self):
        selected = self.table.selectionModel().selectedRows()
        if not selected:
            QMessageBox.warning(self, "No Selection", "Please select a process to end.")
            return
        for sel in selected:
            pid=int(self.table.item(sel.row(),0).text())
            try:
                p=psutil.Process(pid)
                p.terminate()
                p.wait(timeout=3)
            except psutil.TimeoutExpired:
                try:
                    p.kill()
                except Exception as e:
                    QMessageBox.critical(self,"Error",f"Failed to kill process {pid}: {e}")
            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                QMessageBox.critical(self,"Error",f"Unable to end process {pid}: {e}")
        self.update_tasks()

if __name__=="__main__":
    app=QApplication(sys.argv)
    manager=TaskManager()
    manager.show()
    sys.exit(app.exec_())

# Requirements:
# sudo apt install python3 python3-pyqt5 python3-psutil python3-matplotlib
