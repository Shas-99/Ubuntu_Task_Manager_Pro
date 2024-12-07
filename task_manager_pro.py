'''
    Ubuntu Task Manager Pro 
       by Shashank Kadam (2203115) 
          Om Narayan Sharma (2203122)

    Instructions- install required packages and run python3 task_manager_pro.py
    
    1. Install Tkinter (for GUI):
    sudo apt-get install python3-tk

    2. Install psutil (for process management):
    pip install psutil

    3. Install matplotlib (for plotting):
    pip install matplotlib

    4. Install numpy (for numerical operations):
    pip install numpy

    5. Install speedtest-cli (for network speed testing):
    pip install speedtest-cli

'''




#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox
import psutil
import threading
import time
import platform
import os
import signal
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import socket
import speedtest

class ModernUbuntuTaskManager:
    def __init__(self, master):
        self.master = master
        master.title("Ubuntu Task Manager Pro ")
        master.geometry("1200x800")
        master.configure(bg='#2c3e50')  

        self.title_label = tk.Label(
            master,
            text="Ubuntu Task Manager Pro",
            font=("Helvetica", 15, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        self.title_label.pack(pady=(0, 0))

        self.subtitle_label = tk.Label(
            master,
            text="by Shashank and Om",
            font=("Helvetica", 12, "italic"),
            bg="#2c3e50",
            fg="#bdc3c7"
        )
        self.subtitle_label.pack(pady=(2, 0))

        # Custom style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TNotebook', background='#34495e')
        self.style.configure('TNotebook.Tab', background='#2c3e50', foreground='white', padding=[10, 5])
        self.style.map('TNotebook.Tab', background=[('selected', '#3498db')])

        # Initializing notebook
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill='both', padx=15, pady=15)

        # Creating frames
        self.processes_frame = ttk.Frame(self.notebook)
        self.system_frame = ttk.Frame(self.notebook)
        self.performance_frame = ttk.Frame(self.notebook)
        self.network_frame = ttk.Frame(self.notebook)
        

        # Adding tabs
        self.notebook.add(self.processes_frame, text='System Processes')
        self.notebook.add(self.system_frame, text='System Resources')
        self.notebook.add(self.performance_frame, text='Performance Charts')
        self.notebook.add(self.network_frame, text='Network Insights')
        

        # Performance tracking
        self.cpu_history = [0] * 50
        self.mem_history = [0] * 50
        self.disk_history = [0] * 50
        self.network_history = {'sent': [0] * 50, 'recv': [0] * 50}

        # Tabs setup
        self.setup_processes_tab()
        self.setup_system_tab()
        self.setup_performance_tab()
        self.setup_network_tab()
       
        # Periodic updates
        self.start_periodic_updates()

    def setup_processes_tab(self):
        
        # Treeview for processes
        columns = ('PID', 'Name', 'CPU %', 'Memory %', 'Threads', 'Status')
        self.process_tree = ttk.Treeview(self.processes_frame, columns=columns, show='headings', selectmode='browse')
        
        # columns config
        for col in columns:
            self.process_tree.heading(col, text=col)
            self.process_tree.column(col, width=100, anchor='center')
        
        # scrollbar
        scrollbar = ttk.Scrollbar(self.processes_frame, orient='vertical', command=self.process_tree.yview)
        self.process_tree.configure(yscroll=scrollbar.set)

        # treeview and scrollbar
        self.process_tree.pack(side='left', expand=True, fill='both')
        scrollbar.pack(side='right', fill='y')

        # context menu
        self.process_menu = tk.Menu(self.master, tearoff=0)
        self.process_menu.add_command(label="End Process", command=self.end_process, foreground='red')
        self.process_menu.add_command(label="End Process Tree", command=self.end_process_tree, foreground='red')

        # right-click to show menu
        self.process_tree.bind('<Button-3>', self.show_process_menu)

        # Processes label
        self.total_processes_label = ttk.Label(self.processes_frame, text="Total Processes: 0")
        self.total_processes_label.pack(side='bottom', anchor='w', padx=10, pady=5)

        self.unknown_processes_label = ttk.Label(self.processes_frame, text="Unknown Processes: 0")
        self.unknown_processes_label.pack(side='bottom', anchor='w', padx=10, pady=5)    
       
        self.zombie_processes_label = ttk.Label(self.processes_frame, text="Zombie Processes: 0")
        self.zombie_processes_label.pack(side='bottom', anchor='w', padx=10, pady=5)

        self.idle_processes_label = ttk.Label(self.processes_frame, text="Idle Processes: 0")
        self.idle_processes_label.pack(side='bottom', anchor='w', padx=10, pady=5)
       
        self.sleeping_processes_label = ttk.Label(self.processes_frame, text="Sleeping Processes: 0")
        self.sleeping_processes_label.pack(side='bottom', anchor='w', padx=10, pady=5)
        
        self.stopped_processes_label = ttk.Label(self.processes_frame, text="Stopped Processes: 0")
        self.stopped_processes_label.pack(side='bottom', anchor='w', padx=10, pady=5)

        self.running_processes_label = ttk.Label(self.processes_frame, text="Running Processes: 0")
        self.running_processes_label.pack(side='bottom', anchor='w', padx=10, pady=5)
        

        
    def setup_system_tab(self):
        # System Information Labels
        system_info_frame = ttk.Frame(self.system_frame)
        system_info_frame.pack(padx=10, pady=10, fill='x')

        # OS Details
        os_label = ttk.Label(system_info_frame, text=f"OS: {platform.system()} {platform.release()}")
        os_label.pack(anchor='w')

        # CPU Info
        cpu_info = psutil.cpu_freq()
        cpu_label = ttk.Label(system_info_frame, text=f"CPU: {platform.processor()} ({os.cpu_count()} cores)")
        cpu_label.pack(anchor='w')

        # CPU Speed
        cpu_speed_label = ttk.Label(
            system_info_frame, 
            text=f"Base Clock -> Current: {cpu_info.current:.2f} MHz"
        )
        cpu_speed_label.pack(anchor='w')

        # Memory Info
        mem_info = psutil.virtual_memory()
        mem_label = ttk.Label(
            system_info_frame, 
            text=f"Memory: {mem_info.total // (1024**3)} GB (Available: {mem_info.available // (1024**3)} GB)"
        )
        mem_label.pack(anchor='w')

        # Disk Info
        disk_info = psutil.disk_partitions()
        disk_details = []
        counter = 1
        for partition in disk_info:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_details.append(
                f"Drive {counter}: {partition.device}, Filesystem: {partition.fstype}, "
                f"Total: {usage.total // (1024**3)} GB, Used: {usage.used // (1024**3)} GB, Free: {usage.free // (1024**3)} GB"
            )
            counter+=1

        disk_label = ttk.Label(
            system_info_frame, 
            text="\n".join(disk_details), 
            justify='left', 
            wraplength=800 
        )
        disk_label.pack(anchor='w', pady=(10, 0))

        # Resource Usage Progress Bars
        resource_frame = ttk.Frame(self.system_frame)
        resource_frame.pack(padx=10, pady=10, fill='x')

        ttk.Label(resource_frame, text="CPU Usage:").pack(anchor='w')
        self.cpu_progress = ttk.Progressbar(resource_frame, length=500, mode='determinate')
        self.cpu_progress.pack(anchor='w', fill='x', pady=5)
        self.cpu_usage_label = ttk.Label(resource_frame, text="0.0%")
        self.cpu_usage_label.pack(anchor='w', padx=10)

        # Memory Usage
        ttk.Label(resource_frame, text="Memory Usage:").pack(anchor='w')
        self.mem_progress = ttk.Progressbar(resource_frame, length=500, mode='determinate')
        self.mem_progress.pack(anchor='w', fill='x', pady=5)
        self.mem_usage_label = ttk.Label(resource_frame, text="0.0%")
        self.mem_usage_label.pack(anchor='w', padx=10)

        # Disk Usage
        ttk.Label(resource_frame, text="Disk Usage:").pack(anchor='w')
        self.disk_progress = ttk.Progressbar(resource_frame, length=500, mode='determinate')
        self.disk_progress.pack(anchor='w', fill='x', pady=5)
        self.disk_usage_label = ttk.Label(resource_frame, text="0.0%")
        self.disk_usage_label.pack(anchor='w', padx=10)

    def setup_performance_tab(self):
        # Performance charts using matplotlib
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(3, 1, figsize=(10, 8))
        self.fig.suptitle('System Performance')
        
        # CPU Performance Chart
        self.ax1.set_title('CPU Usage')
        self.ax1.set_ylim(0, 100)
        self.line1, = self.ax1.plot(self.cpu_history)
        self.ax1.set_ylabel('CPU Usage (%)')  
        self.ax1.set_xticks([])

        # Memory Performance Chart
        self.ax2.set_title('Memory Usage')
        self.ax2.set_ylim(0, 100)
        self.line2, = self.ax2.plot(self.mem_history)
        self.ax2.set_ylabel('Memory Usage (%)')  
        self.ax2.set_xticks([])

        # Disk Performance Chart
        self.ax3.set_title('Disk Usage')
        self.ax3.set_ylim(0, 100)
        self.line3, = self.ax3.plot(self.disk_history)
        self.ax3.set_ylabel('Disk Usage (%)') 
        self.ax3.set_xticks([])

        # Embeded matplotlib figure in Tkinter
        canvas = FigureCanvasTkAgg(self.fig, master=self.performance_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)

    def setup_network_tab(self):
        # Network information frame
        network_info_frame = ttk.Frame(self.network_frame)
        network_info_frame.pack(padx=10, pady=10, fill='x')

        # Network Details
        self.network_label = ttk.Label(network_info_frame, text="Network Details")
        self.network_label.pack(anchor='w')

        # Network Speed Test Button
        speed_test_btn = ttk.Button(network_info_frame, text="Run Speed Test", command=self.run_network_speedtest)
        speed_test_btn.pack(anchor='w', pady=10)
        
        # Speed Test Results Label
        self.speed_test_label = ttk.Label(network_info_frame, text="Click the button above to run Speed Test ")
        self.speed_test_label.pack(anchor='w', pady=10)

        # network performance chart
        self.network_fig, (self.network_ax) = plt.subplots(1, 1, figsize=(10, 4))
        self.network_fig.suptitle('Network Traffic')
        
        self.network_ax.set_title('Network Sent/Received')
        self.network_ax.set_ylim(0.01,5)  
        # self.network_ax.set_ylim(0, max(max(self.network_history['sent']), max(self.network_history['recv'])) * 1.1)

        sent_list = [ (x/400000) for x in self.network_history['sent']]
        rcv_list = [ (x/400000) for x in self.network_history['recv']]
        self.network_sent_line, = self.network_ax.plot(sent_list , label='Sent')
        self.network_recv_line, = self.network_ax.plot(rcv_list, label='Received')
        self.network_ax.legend()
        self.network_ax.set_ylabel("MBps") 
        self.network_ax.set_xticks([])

        # Embeded network matplotlib figure in Tkinter
        network_canvas = FigureCanvasTkAgg(self.network_fig, master=self.network_frame)
        network_canvas_widget = network_canvas.get_tk_widget()
        network_canvas_widget.pack(fill=tk.BOTH, expand=True)

    

    def run_network_speedtest(self):
        def perform_speedtest():
            self.speed_test_label.config(text="Running speed test... please wait")
            try:
                st = speedtest.Speedtest()
                download_speed = st.download() / 1_000_000  # Convert to Mbps
                upload_speed = st.upload() / 1_000_000  # Convert to Mbps
                ping = st.results.ping

                self.master.after(0, lambda: self.network_label.config(
                    text=f"Download: {download_speed:.2f} Mbps\n"
                         f"Upload: {upload_speed:.2f} Mbps\n"
                         f"Ping: {ping} ms"
                ))
                self.speed_test_label.config(text="Speed Test Complete!")
            except Exception as e:
                messagebox.showerror("Speed Test Error", str(e))

        threading.Thread(target=perform_speedtest, daemon=True).start()

    def show_process_menu(self, event):
        """Show context menu for processes"""
        selected_item = self.process_tree.identify_row(event.y)
        if selected_item:
            self.process_tree.selection_set(selected_item)
            self.process_menu.tk_popup(event.x_root, event.y_root)

    def end_process(self):
        """Terminate selected process"""
        selected_item = self.process_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "No process selected")
            return
        
        pid = self.process_tree.item(selected_item)['values'][0]
        try:
            os.kill(int(pid), signal.SIGKILL)
            messagebox.showinfo("Success", f"Process {pid} terminated")
        except Exception as e:
            messagebox.showerror("Error", f"Could not end process: {e}")

    def end_process_tree(self):
        """Terminate selected process and its children"""
        selected_item = self.process_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "No process selected")
            return
        
        pid = self.process_tree.item(selected_item)['values'][0]
        try:
            parent = psutil.Process(int(pid))
            for child in parent.children(recursive=True):
                child.terminate()
            parent.terminate()
            messagebox.showinfo("Success", f"Process tree for {pid} terminated")
        except Exception as e:
            messagebox.showerror("Error", f"Could not end process tree: {e}")

    def start_periodic_updates(self):
        """Start periodic system updates"""
        def update_loop():
            while True:
                # Update process list
                self.master.after(0, self.update_process_list)
                
                # # Update system resources
                # cpu_percent = psutil.cpu_percent()
                # mem_percent = psutil.virtual_memory().percent
                # disk_percent = psutil.disk_usage('/').percent

                # Update CPU usage
                cpu_percent = psutil.cpu_percent(interval=None)
                self.cpu_progress['value'] = cpu_percent
                self.cpu_usage_label.config(text=f"{cpu_percent:.1f}%")

                # Update memory usage
                mem_percent = psutil.virtual_memory().percent
                self.mem_progress['value'] = mem_percent
                self.mem_usage_label.config(text=f"{mem_percent:.1f}%")

                # Update disk usage
                disk_percent = psutil.disk_usage('/').percent
                self.disk_progress['value'] = disk_percent
                self.disk_usage_label.config(text=f"{disk_percent:.1f}%")
                            
                # Network traffic
                net_io = psutil.net_io_counters()
                
                # Update UI elements
                self.master.after(0, lambda: self.update_system_ui(
                    cpu_percent, self.mem_progress['value'], self.disk_progress['value'], 
                    net_io.bytes_sent, net_io.bytes_recv
                ))
                
                time.sleep(1)  # Update every second

        update_thread = threading.Thread(target=update_loop, daemon=True)
        update_thread.start()

    def update_system_ui(self, cpu_percent, mem_percent, disk_percent, bytes_sent, bytes_recv):
        """Update system UI components"""
        # Update progress bars
        self.cpu_progress['value'] = cpu_percent
        self.mem_progress['value'] = mem_percent
        self.disk_progress['value'] = disk_percent

        # Update performance history lists
        self.cpu_history = self.cpu_history[1:] + [cpu_percent]
        self.mem_history = self.mem_history[1:] + [mem_percent]
        self.disk_history = self.disk_history[1:] + [disk_percent]
        
        # Update network history (convert to KB/s)
        self.network_history['sent'] = self.network_history['sent'][1:] + [bytes_sent / 1024]
        self.network_history['recv'] = self.network_history['recv'][1:] + [bytes_recv / 1024]

        # Update performance charts
        self.line1.set_ydata(self.cpu_history)
        self.line2.set_ydata(self.mem_history)
        self.line3.set_ydata(self.disk_history)
        
        # Update network chart
        sent_list = [ (x/400000) for x in self.network_history['sent']]
        rcv_list = [ (x/400000) for x in self.network_history['recv']]
        self.network_sent_line.set_ydata(sent_list)
        self.network_recv_line.set_ydata(rcv_list)

        # Redraw charts
        self.ax1.relim()
        self.ax1.autoscale_view()
        self.ax2.relim()
        self.ax2.autoscale_view()
        self.ax3.relim()
        self.ax3.autoscale_view()
        
        self.network_ax.relim()
        self.network_ax.autoscale_view()

        self.fig.canvas.draw()
        self.network_fig.canvas.draw()


    def update_process_list(self):
        """Update the process list in the treeview and display process types"""
        # Clear existing items
        for i in self.process_tree.get_children():
            self.process_tree.delete(i)

        # Initialize process counts
        process_counts = {
            'total': 0,
            'running': 0,
            'sleeping': 0,
            'stopped': 0,
            'zombie': 0,
            'idle': 0,
            'unknown': 0
        }

        # Get and sort processes
        for proc in sorted(psutil.process_iter(['pid', 'name', 'status']), key=lambda x: x.info['pid']):
            process_counts['total'] += 1
            try:
                # Get CPU, memory usage, threads, and status
                cpu_percent = proc.cpu_percent()
                mem_percent = proc.memory_percent()
                threads = proc.num_threads()
                status = proc.info['status']

                # Increment the count for the specific process status
                if status in process_counts:
                    process_counts[status] += 1
                else:
                    process_counts['unknown'] += 1

                # Only add processes with some resource usage
                if cpu_percent > 0 or mem_percent > 0:
                    self.process_tree.insert('', 'end', values=(
                        proc.info['pid'],
                        proc.info['name'],
                        f"{cpu_percent:.2f}",
                        f"{mem_percent:.2f}",
                        threads,
                        status
                    ))

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        # Update labels for all process counts
        self.total_processes_label.config(text=f"Total Processes: {process_counts['total']}")
        self.running_processes_label.config(text=f"Running Processes: {process_counts['running']}")
        self.sleeping_processes_label.config(text=f"Sleeping Processes: {process_counts['sleeping']}")
        self.stopped_processes_label.config(text=f"Stopped Processes: {process_counts['stopped']}")
        self.zombie_processes_label.config(text=f"Zombie Processes: {process_counts['zombie']}")
        self.idle_processes_label.config(text=f"Idle Processes: {process_counts['idle']}")
        self.unknown_processes_label.config(text=f"Unknown Status Processes: {process_counts['unknown']}")

def main():
    root = tk.Tk()
    app = ModernUbuntuTaskManager(root)
    root.mainloop()

if __name__ == "__main__":
    main()
