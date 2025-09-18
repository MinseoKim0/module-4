import time
import argparse
import RPi.GPIO as GPIO
from mod4_funcs import ultrasonic_init, ultrasonic_read

DEFAULT_TIM   = 5.0
DEFAULT_DELAY = 0.1
DEFAULT_TRIG  = 38
DEFAULT_ECHO  = 40

parser = argparse.ArgumentParser(description="Ultrasonic distance + velocity sampler (program4b)")
parser.add_argument("--tim", type=float, default=DEFAULT_TIM,
                    help=f"total run time in seconds (default {DEFAULT_TIM})")
parser.add_argument("--delay", type=float, default=DEFAULT_DELAY,
                    help=f"time between samples in seconds (default {DEFAULT_DELAY})")
parser.add_argument("--trig", type=int, default=DEFAULT_TRIG,
                    help=f"BOARD pin for TRIG (default {DEFAULT_TRIG})")
parser.add_argument("--echo", type=int, default=DEFAULT_ECHO,
                    help=f"BOARD pin for ECHO (default {DEFAULT_ECHO})")
parser.add_argument("--debug", action="store_true",
                    help="print measurement time per sample")
args = parser.parse_args()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
ultrasonic_init(args.trig, args.echo)

start = time.time()
next_time = start
count = 0

prev_dist = None
prev_time = None

while (time.time() - start) < args.tim:
    now = time.time()
    if now >= next_time:
        t0 = time.time()
        dist_cm = ultrasonic_read(args.trig, args.echo)
        t1 = time.time()

        velocity = None
        if prev_dist is not None and prev_time is not None:
            delta_d = dist_cm - prev_dist 
            delta_t = t1 - prev_time  
            if delta_t > 0:
                velocity = delta_d / delta_t  

        if args.debug:
            if velocity is not None:
                print(f"[{count:03d}] {dist_cm:.1f} cm  |  v={velocity:.2f} cm/s  | meas_time={t1 - t0:.4f} s")
            else:
                print(f"[{count:03d}] {dist_cm:.1f} cm  |  v=---  | meas_time={t1 - t0:.4f} s")
        else:
            if velocity is not None:
                print(f"{dist_cm:.1f} cm  |  v={velocity:.2f} cm/s")
            else:
                print(f"{dist_cm:.1f} cm")

        prev_dist = dist_cm
        prev_time = t1
        count += 1
        next_time = now + args.delay

    time.sleep(0.001)

GPIO.cleanup()
