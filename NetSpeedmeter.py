import psutil
import time
import threading
import tkinter as tk

def get_speed():
    old = psutil.net_io_counters()
    time.sleep(1)
    new = psutil.net_io_counters()

    download_bps = (new.bytes_recv - old.bytes_recv)
    upload_bps = (new.bytes_sent - old.bytes_sent)

    down_mbps = download_bps / (1024 **2)
    up_mbps = upload_bps / (1024 **2)
    down_kbps = download_bps / (1024 ** 1)
    up_kbps = upload_bps / (1024 ** 1)

    return down_mbps, up_mbps, down_kbps, up_kbps

def update_label():
    while True:
        down_mbps, up_mbps, down_kbps, up_kbps = get_speed()
        label.config(text=(
            f"↓ {down_mbps:.2f} MBps | {down_kbps:.0f} KBps\n"
            f"↑ {up_mbps:.2f} MBps | {up_kbps:.0f} KBps"
        ))
    time.sleep(1)

def start_move(event):
    root.x = event.x
    root.y = event.y

def do_move(event):
    x = root.winfo_pointerx() - root.x
    y = root.winfo_pointery() - root.y
    root.geometry(f"+{x}+{y}")


root = tk.Tk()
root.title("Net Speed Meter")
root.attributes("-topmost", True)
root.geometry("150x60+50+50")
root.resizable(True, True)

label = tk.Label(root, text="Starting...", font=("Arial", 12), justify="left")
label.pack(padx=10, pady=10)

threading.Thread(target=update_label, daemon=True).start()

root.mainloop()
