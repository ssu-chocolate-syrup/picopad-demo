import time
import picokeypad
from machine import UART, Pin
import socket
from _thread import *
import network

SSID = 'nt'
PW = '00111111'

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PW)

while not wifi.isconnected():
    pass

HOST = '192.168.59.135'
PORT = 9999

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

def recv_data(client_socket):
    while True:
        data = client_socket.recv(1024)

start_new_thread(recv_data, (client_socket,))

keypad = picokeypad.PicoKeypad()
keypad.set_brightness(1.0)

lit = 0
last_button_states = 0
colour_index = 0

NUM_PADS = keypad.get_num_pads()
while True:
    button_states = keypad.get_button_states()
    if last_button_states != button_states:
        last_button_states = button_states
        if button_states > 0:
            if lit == 0xffff:
                lit = 0
                colour_index += 1
                if colour_index >= 6:
                    colour_index = 0
            else:
                button = 0
                for find in range(0, NUM_PADS):
                    # check if this button is pressed and no other buttons are pressed
                    if button_states & 0x01 > 0:
                        if not (button_states & (~0x01)) > 0:
                            message = "Hello World!"
                            client_socket.send(message.encode())
                            lit = lit | (1 << button)
                        break
                    button_states >>= 1
                    button += 1

    for i in range(0, NUM_PADS):
        if (lit >> i) & 0x01:
            if colour_index == 0:
                keypad.illuminate(i, 0x00, 0x20, 0x00)
            elif colour_index == 1:
                keypad.illuminate(i, 0x20, 0x20, 0x00)
            elif colour_index == 2:
                keypad.illuminate(i, 0x20, 0x00, 0x00)
            elif colour_index == 3:
                keypad.illuminate(i, 0x20, 0x00, 0x20)
            elif colour_index == 4:
                keypad.illuminate(i, 0x00, 0x00, 0x20)
            elif colour_index == 5:
                keypad.illuminate(i, 0x00, 0x20, 0x20)
        else:
            keypad.illuminate(i, 0x05, 0x05, 0x05)

    keypad.update()

    time.sleep(0.1)
