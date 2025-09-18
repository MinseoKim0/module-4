import time
import argparse
import RPi.GPIO as GPIO
from mod4_funcs import ultrasonic_init, ultrasonic_read

DEFAULT_TIM   = 5.0 
DEFAULT_DELAY = 0.1  
DEFAULT_TRIG  = 38     
DEFAULT_ECHO  = 40     

parser = argparse.ArgumentParser(description="Ultrasonic distance sampler (program4a)")
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

while (time.time() - start) < args.tim:
    now = time.time()
    if now >= next_time:
        t0 = time.time()
        dist_cm = ultrasonic_read(args.trig, args.echo)
        t1 = time.time()

        if args.debug:
            print(f"[{count:03d}] {dist_cm:.1f} cm  |  meas_time: {t1 - t0:.4f} s")
        else:
            print(f"{dist_cm:.1f} cm")

        count += 1
        next_time = now + args.delay

    time.sleep(0.001)

GPIO.cleanup()
