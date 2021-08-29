import threading
import psutil
import subprocess as sp
import re
from threading import Thread
import time
import serial


ser = serial.Serial('/dev/ttyACM0')

def get_cpu_info():
    while True:
        cpu_utilization = int(psutil.cpu_percent(interval=2))
        cpu_frequency = psutil.cpu_freq().current
        cpu_temp = int(psutil.sensors_temperatures()['coretemp'][0].current)
        print(f'CPU Util:{cpu_utilization}, CPU Freq: {cpu_frequency}, CPU_Temp: {cpu_temp}')
        data = bytearray([cpu_utilization,cpu_temp])
        ser.write(data)
        time.sleep(1)
              


def get_gpu_info():
    while True:
        gpu_info = sp.run(
                'nvidia-smi --format=csv --query-gpu=utilization.gpu,temperature.gpu,utilization.memory', 
                shell=True, capture_output=True, text=True).stdout

        # Output looks like:
        # 'utilization.gpu [%], temperature.gpu, utilization.memory [%]\n6 %, 44, 6 %\n'
        values = re.search(r'\n(.*?)\n', gpu_info).group(1).replace("%","").split(',')
        gpu_utilization = int(values[0])
        gpu_temperature = int(values[1])
        gpu_memory = int(values[2])
        print(f"GPU Util: {gpu_utilization}, GPU Temp: {gpu_temperature}, GPU Memory: {gpu_memory}")
        data = bytearray([gpu_utilization,gpu_temperature,gpu_memory])
        ser.write(data)
        time.sleep(1)



def get_system_memory():
    while(True):
        total_memory = psutil.virtual_memory().total
        available_memory = psutil.virtual_memory().available
        memory_used = int(((total_memory-available_memory)/total_memory) * 100)
        print (f"System Memory: {memory_used}")
        data = bytearray([memory_used])
        ser.write(data)
        time.sleep(1)
        





def main():
    x = Thread(target=get_system_memory)
    y = Thread(target=get_cpu_info)
    z = Thread(target=get_gpu_info)
    x.start()
    y.start()
    z.start()
    



if __name__ == "__main__":
    main()