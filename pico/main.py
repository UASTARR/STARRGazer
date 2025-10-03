from machine import Pin, PWM

def setup():
    # --- Setup two PWM outputs ---
    pwm1 = PWM(Pin(7))   # Pin for buzzer/motor 1
    pwm2 = PWM(Pin(28))    # Pin for buzzer/motor 2

    # Optional enable + direction pins
    en1 = Pin(8, Pin.OUT)
    dir1 = Pin(9, Pin.OUT)
    en2 = Pin(27, Pin.OUT)
    dir2 = Pin(26, Pin.OUT)

    # Start with both off
    pwm1.duty_u16(0)
    pwm2.duty_u16(0)

def set_pwm(pwm, freq):
    if abs(freq) <= 1:        # off
        pwm.duty_u16(0)
    else:
        pwm.freq(abs(freq))   # set frequency
        pwm.duty_u16(32768)   # 50% duty

def update(f1, f2):
    # Update PWM
    set_pwm(pwm1, f1)
    set_pwm(pwm2, f2)

    # Update enable + direction pins
    en1.value(1 if abs(f1) <= 1 else 0) 
    dir1.value(0 if f1 < 0 else 1) # different dir for x axis
    en2.value(1 if abs(f2) <= 1 else 0)
    dir2.value(1 if f2 < 0 else 0)

# --- Main Program Loop ---
def run():
    f1, f2 = 0, 0   # current values
    try:
        while True:
                user_input = input("Enter (f1,f2): ")  # example: (1000,2000)
                if not user_input.strip():
                    continue
                parts = user_input.strip()[1:-1].split(",")
                f1 = int(parts[0])
                f2 = int(parts[1])
                update(f1, f2)
    except Exception as e:
        update(0,0)
        print("Parse error:", e)


if __name__ == "__main__":
    setup()
    run()
