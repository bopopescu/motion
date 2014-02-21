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
from motion.compass import Compass

class CommHelper():
    def __enter__(self):
        self.comm = Comm("/dev/ttyUSB0")
        return self.comm
    
    def __exit__(self, typee, value, traceback):
        self.comm.close()



if __name__ == '__main__':
    with CommHelper() as comm:
        
#         acc = Accelerometer(comm, 0x53, calibrate=True)
#  
#         for _ in range(1000):
#             data = acc.get_data()
#             print("%f %f %f %f" % (data[0], data[1], data[2], math.sqrt(data[0]**2 + data[1]**2 + data[2]**2)))


#         cProfile.run('acc.get_data()')

        
#         gyro = Gyro(comm, 0x68, fil=Gyro.FILTER_42_SR_1K, smpl_div=49, calibrate=True)
          
#         print(bin(gyro.get_whoami()))


        com = Compass(comm, 0x1e, output_rate=Compass.OUTPUT_RATE_1_5)
        
        for _ in range(100):
            time.sleep(1/1.5)
            print(com.get_data_int())
            
            
