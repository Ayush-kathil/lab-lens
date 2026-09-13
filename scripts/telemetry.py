import psutil
import csv
import time
import os
from pathlib import Path

class MemoryTelemetry:
    def __init__(self, run_dir):
        self.run_dir = Path(run_dir)
        self.run_dir.mkdir(parents=True, exist_ok=True)
        self.csv_path = self.run_dir / "memory.csv"
        self.start_time = time.time()
        self.peak_rss = 0
        self.peak_system_ram = 0
        self.batch_count = 0
        
        with open(self.csv_path, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "event", "epoch", "batch", "process_rss_mb", "system_available_mb", "system_used_mb", "system_percent"])
            
    def record(self, event, epoch=None, batch=None):
        process = psutil.Process(os.getpid())
        mem_info = process.memory_info()
        sys_mem = psutil.virtual_memory()
        
        rss_mb = mem_info.rss / (1024 * 1024)
        sys_avail = sys_mem.available / (1024 * 1024)
        sys_used = sys_mem.used / (1024 * 1024)
        sys_pct = sys_mem.percent
        
        self.peak_rss = max(self.peak_rss, rss_mb)
        self.peak_system_ram = max(self.peak_system_ram, sys_used)
        
        with open(self.csv_path, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([round(time.time() - self.start_time, 2), event, epoch if epoch is not None else "", batch if batch is not None else "", round(rss_mb, 2), round(sys_avail, 2), round(sys_used, 2), sys_pct])
            
    def attach(self, model):
        def on_train_start(trainer):
            self.record("train_start")
            
        def on_train_epoch_start(trainer):
            epoch = getattr(trainer, 'epoch', None)
            self.batch_count = 0
            self.record("epoch_start", epoch=epoch)
            
        def on_train_batch_end(trainer):
            epoch = getattr(trainer, 'epoch', None)
            self.batch_count += 1
            if self.batch_count % 20 == 0:
                self.record("batch_end_sample", epoch=epoch, batch=self.batch_count)
                
        def on_train_epoch_end(trainer):
            epoch = getattr(trainer, 'epoch', None)
            self.record("epoch_end", epoch=epoch)
            
        def on_val_start(validator):
            self.record("val_start")
            
        def on_val_end(validator):
            self.record("val_end")
            
        def on_train_end(trainer):
            self.record("train_end")
            
        model.add_callback("on_train_start", on_train_start)
        model.add_callback("on_train_epoch_start", on_train_epoch_start)
        model.add_callback("on_train_batch_end", on_train_batch_end)
        model.add_callback("on_train_epoch_end", on_train_epoch_end)
        model.add_callback("on_val_start", on_val_start)
        model.add_callback("on_val_end", on_val_end)
        model.add_callback("on_train_end", on_train_end)
