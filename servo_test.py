from adafruit_servokit import ServoKit
import time

kit = ServoKit(channels=16)

PAN_CHANNEL = 0
TILT_CHANNEL = 1

kit.servo[PAN_CHANNEL].actuation_range = 180 
kit.servo[TILT_CHANNEL].actuation_range = 180 
kit.servo[PAN_CHANNEL].set_pulse_width_range(500, 2500)
kit.servo[TILT_CHANNEL].set_pulse_width_range(500, 2500)

print("Starting...")

try:
    while True:
        for angle in range(0, 181, 5):
            kit.servo[PAN_CHANNEL].angle = angle
            kit.servo[TILT_CHANNEL].angle = angle
            time.sleep(0.02)

        for angle in range(180, -1, -5):
            kit.servo[PAN_CHANNEL].angle = angle
            kit.servo[TILT_CHANNEL].angle = angle
            time.sleep(0.02)

except KeyboardInterrupt:
    print("Exiting...")
