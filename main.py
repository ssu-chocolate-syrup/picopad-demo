import time
import picokeypad as keypad
from machine import UART, Pin

keypad.init()
keypad.set_brightness(1.0)

lit = 0
last_button_states = 0
colour_index = 0
color = [[0x05, 0x00, 0x00], [0x05, 0x00, 0x00], [0x05, 0x00, 0x00], [0x05, 0x00, 0x00],  # red
         [0x00, 0x05, 0x00], [0x00, 0x05, 0x00], [0x00, 0x05, 0x00], [0x00, 0x05, 0x00],  # green
         [0x00, 0x00, 0x05], [0x00, 0x00, 0x05], [0x00, 0x00, 0x05], [0x00, 0x00, 0x05],  # blue
         [0x05, 0x05, 0x00], [0x05, 0x05, 0x00], [0x05, 0x05, 0x00], [0x05, 0x05, 0x00]]  # yellow

NUM_PADS = keypad.get_num_pads()
print(f"num pads : {NUM_PADS}")

color[15][1] = 0x05
for find in range(NUM_PADS):
    keypad.illuminate(find, color[find][0], color[find][1], color[find][2])

while True:
    button_states = keypad.get_button_states()
    if last_button_states != button_states:
        last_button_states = button_states
        print(f"button states : {button_states}")

        if button_states > 0:
            button = 0
            for find in range(0, NUM_PADS):
                if button_states & 0x01 > 0:
                    print(f"Button Pressed is : {find}")
                    keypad.illuminate(button, 25, 25, 25)
                button_states >>= 1
                button += 1

        else:
            for find in range(0, NUM_PADS):
                keypad.illuminate(find, color[find][0], color[find][1], color[find][2])

    keypad.update()
    time.sleep(0.1)
