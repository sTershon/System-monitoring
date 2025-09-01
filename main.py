import tkinter as tk
from tkinter import ttk
import psutil
import GPUtil
import threading
import time

class SystemMonitor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Монитор ресурсов by Tershon")
        self.geometry("400x350")
        self.configure(bg="#1e1e2f")

        # Заголовок
        title = tk.Label(self, text="Sistem Monitor", font=("Segoe UI", 16, "bold"), fg="white", bg="#1e1e2f")
        title.pack(pady=10)

        # CPU
        self.cpu_label = tk.Label(self, text="CPU: 0%", font=("Segoe UI", 12), fg="white", bg="#1e1e2f")
        self.cpu_label.pack()
        self.cpu_bar = ttk.Progressbar(self, orient="horizontal", length=300, mode="determinate")
        self.cpu_bar.pack(pady=5)

        # RAM
        self.ram_label = tk.Label(self, text="RAM: 0%", font=("Segoe UI", 12), fg="white", bg="#1e1e2f")
        self.ram_label.pack()
        self.ram_bar = ttk.Progressbar(self, orient="horizontal", length=300, mode="determinate")
        self.ram_bar.pack(pady=5)

        # GPU
        self.gpu_label = tk.Label(self, text="GPU: Нет данных", font=("Segoe UI", 12), fg="white", bg="#1e1e2f")
        self.gpu_label.pack()
        self.gpu_bar = ttk.Progressbar(self, orient="horizontal", length=300, mode="determinate")
        self.gpu_bar.pack(pady=5)

        # Футер
        footer = tk.Label(
            self,
            text="Автор: Tershon  |  GitHub: https://github.com/sTershon",
            font=("Segoe UI", 9, "italic"),
            fg="gray",
            bg="#1e1e2f",
            cursor="hand2"
        )
        footer.pack(side="bottom", pady=10)

        # Кликабельная ссылка
        footer.bind("<Button-1>", lambda e: self.open_github())

        # Запускаем обновление в отдельном потоке
        threading.Thread(target=self.update_data, daemon=True).start()

    def update_data(self):
        while True:
            # CPU
            cpu_usage = psutil.cpu_percent()
            self.cpu_label.config(text=f"CPU: {cpu_usage}%")
            self.cpu_bar["value"] = cpu_usage

            # RAM
            ram = psutil.virtual_memory()
            ram_usage = ram.percent
            self.ram_label.config(
                text=f"RAM: {ram_usage}% ({round(ram.used / 1024**3, 1)} / {round(ram.total / 1024**3, 1)} GB)"
            )
            self.ram_bar["value"] = ram_usage

            # GPU
            try:
                gpus = GPUtil.getGPUs()
                if gpus:
                    gpu = gpus[0]
                    gpu_usage = gpu.load * 100
                    self.gpu_label.config(
                        text=f"GPU: {gpu_usage:.1f}% ({gpu.memoryUsed} / {gpu.memoryTotal} MB)"
                    )
                    self.gpu_bar["value"] = gpu_usage
                else:
                    self.gpu_label.config(text="GPU: Не обнаружено")
            except:
                self.gpu_label.config(text="GPU: Нет данных")

            time.sleep(1)

    def open_github(self):
        import webbrowser
        webbrowser.open("https://github.com/sTershon")


if __name__ == "__main__":
    app = SystemMonitor()
    app.mainloop()
