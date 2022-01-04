#< Module that shows your hardware informations. >#

import requests as req
import GPUtil
import shutil
import psutil
import socket
import sys
import os

# Colors
red    = "\033[1;31m"
orange = "\033[0;33m"
green  = "\033[1;32m"
blue   = "\033[1;36m"
end    = "\033[0m"

# Get, show data
def ShowDisk():
    print(f"=== Disks ===")
    DisksList = __import__("re").findall(r"[A-Z]+:.*$",os.popen("mountvol /").read(),__import__("re").MULTILINE)
    
    for i in range(len(DisksList)):
        DiskName  = DisksList[i]
        DiskUsed  = round((shutil.disk_usage(DiskName).used/shutil.disk_usage(DiskName).total) * 100)
        DiskFree  = round((shutil.disk_usage(DiskName).free/shutil.disk_usage(DiskName).total) * 100)
        DiskTotal = round((shutil.disk_usage(DiskName)[0] / 1024 / 1024 / 1024))

        try:
            print(f" {DisksList[i]}")
            print(f"  Used : {green if DiskUsed < 34 else orange if DiskUsed > 34 and DiskUsed < 75 else red}{DiskUsed} % {end}")
            print(f"  Free : {green if DiskFree > 34 else orange if DiskFree < 34 and DiskFree > 75 else red}{DiskFree} % {end}")
            print(f"  Total: {blue}{DiskTotal} Gb\n {end}")

        except:
            print(f"{red}Disk: \"{DisksList[i]}:\" not found!{end}")
def ShowNet():
    print("\n=== Net ===")

    try:
        request = req.get("https://www.google.pl/")
        net_work = True
    except (requests.ConnectionError, requests.Timeout):
        net_work = False

    print(f" Working: {green if net_work == True else red}{net_work} {end}")
    print(f" Public : {blue}{req.get('https://api.ipify.org').text} {end}")
    print(f" Private: {blue}{socket.gethostbyname(socket.gethostname())}{end}")
def ShowCpu():
    print("\n\n=== Cpu ===")

    print(f" Cores  : {blue}{psutil.cpu_count(logical=True)} {end}")
    print(f" Frqncy : {blue}{psutil.cpu_freq().max} Mhz {end}")
    for i in range(8):
        CpuUsage = psutil.cpu_percent(interval=0.1)
    print(f" Usage  : {green if CpuUsage < 34 else orange if CpuUsage > 34 and CpuUsage < 75 else red}{CpuUsage} % {end}")
def ShowGpu():
    print("\n\n=== Gpu ===")

    gpus = GPUtil.getGPUs()
    for gpu in gpus:
        print(f" Name   : {blue}{gpu.name}{end}")
        print(f" Usage  : {green if round(gpu.load * 100) < 34 else orange if round(gpu.load * 100) > 34 and round(gpu.load * 100) < 75 else red}{round(gpu.load * 100)} % {end}")
        print(f" Memory : {blue}{gpu.memoryTotal} MB {end}")
def ShowRam():
    print("\n\n=== Ram ===")

    Ram_FreePercentage = (round(psutil.virtual_memory()[1] / 1024 / 1024 / 1024, 2)) / (round((psutil.virtual_memory()[0] / 1024 / 1024 / 1024), 2)) * 100
    Ram_UsedPercentage = 100 - Ram_FreePercentage

    print(f" Usage  : {green if psutil.virtual_memory()[2] < 34 else orange if psutil.virtual_memory()[2] > 34 and psutil.virtual_memory()[2] < 75 else red}{psutil.virtual_memory()[2]} % {end}")
    print(f" Free   : {green if Ram_FreePercentage > 34 else orange if Ram_FreePercentage > 34 and Ram_FreePercentage > 75 else red}{round(psutil.virtual_memory()[1] / 1024 / 1024 / 1024, 2)} Gb {end}")
    print(f" Used   : {green if Ram_UsedPercentage < 34 else orange if Ram_UsedPercentage > 34 and Ram_UsedPercentage < 75 else red}{round(psutil.virtual_memory()[3] / 1024 / 1024 / 1024, 2)} Gb {end}")
    print(f" Total  : {blue}{round((psutil.virtual_memory()[0] / 1024 / 1024 / 1024), 2)} Gb {end}")
def ShowAll():
    ShowDisk()
    ShowNet()
    ShowCpu()
    ShowGpu()
    ShowRam()

# Handle attributes

ShowAll()

print(end)
