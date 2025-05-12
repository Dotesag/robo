import random
from vehicle.Vehicle import Vehicle
import asyncio
from connection.SocketConnection import SocketConnection
import json
import struct
import time
from vehicle.yellow_line_follow import analyze_yellow_line

class BinaryDataHandler:
    def __init__(self, vehicle: Vehicle, connection: SocketConnection):
        self.connection = connection
        self.vehicle = vehicle

    async def start_driving(self):

        # self.example_1()
        # self.example_2()
        # self.example_3()
        self.example_4()

    def save_image(self, image_data):
        filename = f"D:/temp/{str(int(time.time()))}_{str(random.random())}.webp"

        with open(filename, 'wb') as f:
            f.write(image_data)

        return analyze_yellow_line(filename)

    # пример использования setMotorPower и rotate

    def example_4(self):
        l_force = 50
        r_force = 50
        
        while True:
            self.vehicle.setMotorPower(l_force, r_force)
            # time.sleep(0.0001)

            # скриншот с камеры 6
            self.connection.send_data("camera6")
            image_data = self.connection.receive_data()
            sol = self.save_image(image_data)
            print(sol)

            self.vehicle.rotate(sol)
            # time.sleep(0.5)
                

async def control_vehicle(vehicle: Vehicle, connection: SocketConnection):
    data_handler = BinaryDataHandler(vehicle, connection)
    await data_handler.start_driving()
