'''
Created on 18. 2. 2014

@author: ondra
'''

import time

from motion.comm import Comm
from motion.acc import Accelerometer
import math
from motion.gyro import Gyro
import cProfile

class CommHelper():
    def __enter__(self):
        self.comm = Comm("/dev/ttyUSB0")
        return self.comm
    
    def __exit__(self, typee, value, traceback):
        self.comm.close()



if __name__ == '__main__':
    with CommHelper() as comm:
        
        acc = Accelerometer(comm, 0x53, calibrate=True)

        for _ in range(1000):
            data = acc.get_data()
            print("%f %f %f %f" % (data[0], data[1], data[2], math.sqrt(data[0]**2 + data[1]**2 + data[2]**2)))


#         cProfile.run('acc.get_data()')

        
#         gyro = Gyro(comm, 0x68)
        
#         print(bin(gyro.get_whoami()))
#         
#         for i in range(1, 10):
#             print(gyro.get_data())