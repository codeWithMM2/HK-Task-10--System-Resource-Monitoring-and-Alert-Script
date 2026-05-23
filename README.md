# 🐍 Project 10: System Resource Monitoring & Alert Script

A robust, CLI-based Python application designed to monitor system resources (CPU, RAM, and Disk usage) in real-time. It features dynamic ASCII progress bars, persistent data logging, an automated alert system via desktop notifications and email, and visual analytics graphs.

---

## 🎯 Project Objective
The goal of this project is to simulate real-world DevOps/SysAdmin infrastructure monitoring tools. It tracks system performance metrics continuously and alerts the administrator immediately if any resource usage exceeds the user-defined safety thresholds.

---

## ✨ Features

### 🖥️ Core Functionalities
* **Real-Time Resource Monitoring:** Continuous tracking of CPU, RAM, and Disk metrics utilizing the `psutil` library.
* **Interactive CLI Menu:** A clean command-line interface to start monitoring, set custom thresholds, view history logs, or generate analytics.
* **Dynamic Visual Bars:** Live feedback using clean ASCII bars (`[#####-----]`) with conditional status tags (`[OK]` / `[!!]`).

### 🌟 Bonus & Advanced Features
* **Automated Alert System:** Generates instant **Desktop Notifications** (via `plyer`) the exact moment a threshold is crossed.
* **Email Integration:** Optional secure Gmail alerts sent directly to the administrator using `smtplib` (MIME protocol).
* **Persistent Logging System:** Automatically captures snapshots with timestamps and appends them to a structured CSV file (`system_log.csv`).
* **Visual Analytics Graph:** Generates a professional data visualization plot using `matplotlib` and `pandas` to analyze system performance over time.

---

## ⚙️ Functional Architecture

* **`setup_log()` & `save_to_log()`**: Handles structural initialization and appends data to the CSV logging layer.
* **`get_stats()`**: Safely polls hardware resource percentages.
* **`monitor_loop()`**: Multithreaded background process ensuring real-time execution without freezing the main menu.
* **`show_graph()`**: Analytical engine that maps historical metrics into a visual plot graph.

---

## 🛠️ Installation & Setup

### 1. Clone or Download the Project
Download the source code files into a local directory on your machine.

### 2. Install Dependencies
Run the following command in your terminal/command prompt to install the required Python libraries:
```bash
pip install psutil plyer

### 3. Run the application
Execute the script via your system terminal for proper screen-clearing rendering:

Bash
python System monitor.py

## Demo video:
You can see the working in:
Monitor system demo video.mp4
