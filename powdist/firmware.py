import RPi.GPIO as GPIO
import time

pins = [14, 15, 16, 18, 20, 21, 24, 25]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


def main():
    for x in pins:
        print('Setting pin {0} as output'.format(x))
        GPIO.setup(x, GPIO.OUT)

    for x in pins:
            print('Setting pin {0} high'.format(x))
            GPIO.output(x, GPIO.HIGH)

    while True:
        for x in pins:
            pin_status = GPIO.input(x)
            if(pin_status is 1):
                print('Pin {0} set low when should be high.  Setting pin {0} high.'.format(x))
                GPIO.output(x, GPIO.HIGH)
            else:
                print('Pin {0} set high.'.format(x))

        time.sleep(10)


if __name__ == "__main__":
    main()
