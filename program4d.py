import time
import argparse
import smbus
from mod4_funcs import MPU_Init, MPU_Read, movingAvg

parser = argparse.ArgumentParser(description="MPU6050 logger (program4d)")
parser.add_argument("--tim", type=float, default=5.0,
                    help="total run time in seconds (default 5.0)")
parser.add_argument("--delay", type=float, default=0.1,
                    help="time between samples in seconds (default 0.1)")
parser.add_argument("--out", type=int, choices=range(1, 7), default=1,
                    help="1:Ax  2:Ay  3:Az  4:Gx  5:Gy  6:Gz  (default 1)")
parser.add_argument("--debug", action="store_true",
                    help="print to screen only when debug is true")
parser.add_argument("--file", default="data.txt",
                    help="output filename (default data.txt)")
args = parser.parse_args()

labels = {1: "Ax", 2: "Ay", 3: "Az", 4: "Gx", 5: "Gy", 6: "Gz"}
units  = {1: "g",  2: "g",  3: "g",  4: "°/s", 5: "°/s", 6: "°/s"}
label = labels[args.out]
unit  = units[args.out]

bus = smbus.SMBus(1)
MPU_Init(bus)

times = [] 
values = []  
mavals = [] 

start = time.time()
next_time = start
count = 0

while (time.time() - start) < args.tim:
    now = time.time()
    if now >= next_time:
        val = MPU_Read(bus, args.out)  
        values.append(val)

        idx = len(values) - 1  
        ma  = movingAvg(values, idx, numvals=3)
        mavals.append(ma)

        t = now - start
        times.append(t)

        if args.debug:
            print(f"{t:0.2f}\t{val:0.2f}\t{ma:0.2f}  ({label} {unit})")

        count += 1
        next_time = now + args.delay

    time.sleep(0.001)

with open(data.txt, "w") as f:
    for t, v, ma in zip(times, values, mavals):
        f.write(f"{t:0.2f}\t{v:0.2f}\t{ma:0.2f}\n")
