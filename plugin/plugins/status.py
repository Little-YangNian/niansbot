import psutil
import datetime
def sys_status():
    memorys = psutil.virtual_memory()
    cpu = psutil.cpu_percent()
    start_time = datetime.datetime.fromtimestamp(psutil.boot_time ()).strftime("%Y-%m-%d %H: %M: %S")
    precent = memorys.percent
    return f'Server Status:\nCPU: {cpu}%\nMemory: {precent}%\nStart Time:\n{start_time}'
