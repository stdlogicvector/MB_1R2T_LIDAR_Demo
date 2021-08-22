import serial
import pygame
import math
from enum import Enum
 
class State(Enum):
    SYNC0 = 0
    SYNC1 = 1
    HEADER = 2
    DATA = 3

pygame.init()
pygame.display.set_caption('LIDAR Demo')
font = pygame.font.Font(None, 30)
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
screen.fill((0, 0, 0))

com = serial.Serial(port='COM13', 
                            baudrate=158700, 
                            parity=serial.PARITY_NONE, 
                            stopbits=serial.STOPBITS_ONE, 
                            bytesize=serial.EIGHTBITS, 
                            timeout=None)
 
state = State.SYNC0
package_type = 0
package_size = 0
package_start = 0
package_stop = 0
last_angle = 0

running = True

while running:
    if state == State.SYNC0:
        sync = com.read(1)

        if len(sync) < 1:
            continue

        if sync[0] == 0xAA:
            state = State.SYNC1
        else:
            state = State.SYNC0

    elif state == State.SYNC1:
        sync = com.read(1)

        if len(sync) < 1:
            state = State.SYNC0
            continue

        if sync[0] == 0x55:
            state = State.HEADER
        else:
            state = State.SYNC0

    elif state == State.HEADER:
        header = com.read(8)

        if (len(header) < 8):
            state = State.SYNC0
        else:
            # Decode Header
            package_type = header[0]
            package_size = header[1]
            package_start = (header[3] << 8) | header[2]
            package_stop  = (header[5] << 8) | header[4]

            state = State.DATA

    elif state == State.DATA:
        if package_size > 0:
            data = com.read(package_size * 3)
        else:
            state = State.SYNC0
            continue

        if len(data) < (package_size*3):
            state = State.SYNC0
            continue

        if package_type & 0x01: # Bad Package
            state = State.SYNC0
            continue

        diff = package_stop - package_start
        if package_stop < package_start:
            diff = 0xB400 - package_start + package_stop

        step = 0
        if diff > 1:
            step = diff / (package_size-1)

        # Decode Data
        for i in range(package_size):
            intensity = data[i*3 + 0]

            distance = (data[i*3 + 2] << 8) | data[i*3 + 1]
            distancef = distance / 40.0

            angle = (package_start + step * i) % 0xB400
            anglef = (angle / 0xB400) * (math.pi * 2)

            if anglef < last_angle: # New Frame
                pygame.display.flip()
                clock.tick()
                screen.fill((0, 0, 0))
                fps = font.render(str(int(clock.get_fps()))+' fps', True, pygame.Color('white'))
                screen.blit(fps, (20, 20))
            
            last_angle = anglef

            anglef = math.pi*2 - anglef

            x = math.cos(anglef) * distancef * (+1) + 400
            y = math.sin(anglef) * distancef * (-1) + 400

            if distance < 64840:
                screen.set_at((int(x),int(y)), (intensity,255-intensity,intensity))

        state = State.SYNC0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

com.close
