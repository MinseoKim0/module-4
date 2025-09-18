import time
import argparse
import smbus
from mod4_funcs import MPU_Init, MPU_Read

parser = argparse.ArgumentParser(description="MPU6050 sampler (program4c)")
parser.add_argument("--tim", type=float, default=5.0,
                    help="total run time in seconds (default 5.0)")
parser.add_argument("--delay", type=float, default=0.1,
                    help="time between samples in seconds (default 0.1)")
parser.add_argument("--out", type=int, choices=range(1, 7), default=1,
                    help="1:Ax  2:Ay  3:Az  4:Gx  5:Gy  6:Gz  (default 1)")
parser.add_argument("--debug", action="store_true",
                    help="print measurement time per sample")
args = parser.parse_args()

labels = {1: "Ax", 2: "Ay", 3: "Az", 4: "Gx", 5: "Gy", 6: "Gz"}
units  = {1: "g",  2: "g",  3: "g",  4: "°/s", 5: "°/s", 6: "°/s"}
label = labels[args.out]
unit  = units[args.out]

bus = smbus.SMBus(1)
MPU_Init(bus)

print(f"Reading {label} from MPU6050 — {args.delay}s interval for {args.tim}s")

start = time.time()
next_time = start
count = 0

while (time.time() - start) < args.tim:
    now = time.time()
    if now >= next_time:
        t0 = time.time()
        val = MPU_Read(bus, args.out)
        t1 = time.time()

        if args.debug:
            print(f"[{count:03d}] {label}: {val:0.3f} {unit}  |  meas_time={t1 - t0:0.4f} s")
        else:
            print(f"{label}: {val:0.3f} {unit}")

        count += 1
        next_time = now + args.delay

    time.sleep(0.001)
