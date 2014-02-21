'''
Created on 18. 2. 2014

@author: ondra
'''

class Accelerometer(object):
    '''
    classdocs
    '''
    DEVID = 0x00
    
    OFSX = 0x1e
    OFSY = 0x1f
    OFSZ = 0x20
    
    BW_RATE = 0x2c
    POWER_CTL = 0x2d
    DATA_FORMAT = 0x31

    DATAX0 = 0x32
    DATAX1 = 0x33
    DATAY0 = 0x34
    DATAY1 = 0x35
    DATAZ0 = 0x36
    DATAZ1 = 0x37
    
    
    DATA_RATE_0_1 = 0b0000
    DATA_RATE_0_2 = 0b0001
    DATA_RATE_0_39 = 0b0010
    DATA_RATE_0_78 = 0b0011
    DATA_RATE_1_56 = 0b0100
    DATA_RATE_3_13 = 0b0101
    DATA_RATE_6_25 = 0b0110
    DATA_RATE_12_5 = 0b0111
    DATA_RATE_25 = 0b1000
    DATA_RATE_50 = 0b1001
    DATA_RATE_100 = 0b1010
    DATA_RATE_200 = 0b1011
    DATA_RATE_400 = 0b1100
    DATA_RATE_800 = 0b1101
    DATA_RATE_1600 = 0b1110
    DATA_RATE_3200 = 0b1111
        
    def __init__(self, comm, addr, data_rate=DATA_RATE_100, calibrate=False):
        self.comm = comm
        self.addr = addr
        
        # Set max resolution (16g) and full res        
        self.comm.write_byte(self.addr, self.DATA_FORMAT, 0x0b)

        self.comm.write_byte(self.addr, self.BW_RATE, data_rate)

        # Measure bit on
        self.comm.write_byte(self.addr, self.POWER_CTL, 0x08)
                
        if calibrate:
            self.calibrate()
        
    def calibrate(self):

        self.comm.write_byte(self.addr, self.OFSX, 0)
        self.comm.write_byte(self.addr, self.OFSY, 0)
        self.comm.write_byte(self.addr, self.OFSZ, 0)
        
        num_samples = 50

        x = 0
        y = 0
        z = 0
        
        for _ in range(num_samples):
            cur = self.get_data_int()
            x += cur[0]
            y += cur[1]
            z += cur[2]
            
        x = (float(x) / num_samples)
        y = (float(y) / num_samples)
        z = (float(z) / num_samples - 256)
        
        dx = int(round(x/4)) 
        dy = int(round(y/4))
        dz = int(round(z/4))

        ddx = self._to_unsigned8b(-dx)
        ddy = self._to_unsigned8b(-dy)
        ddz = self._to_unsigned8b(-dz)

        self.comm.write_byte(self.addr, self.OFSX, ddx)
        self.comm.write_byte(self.addr, self.OFSY, ddy)
        self.comm.write_byte(self.addr, self.OFSZ, ddz)


    
    def get_avg_data(self, n):
        x = 0
        y = 0
        z = 0
        for _ in range(n):
            data = self.get_data()
            x += data[0]
            y += data[1]
            z += data[2]
            
        x = x / n
        y = y / n
        z = z / n
        
        return (x, y, z)
    
                    
    def get_devid(self):
        return self.comm.read_byte(self.addr, self.DEVID)
    
    def get_offset(self):
        return (self.comm.read_byte(self.addr, self.OFSX),
                self.comm.read_byte(self.addr, self.OFSY),
                self.comm.read_byte(self.addr, self.OFSZ))
        
    def get_data_int(self):
        
        while not self.is_data_ready():
            pass
                
        rawx = (self.comm.read_word(self.addr, self.DATAX0))
        x = self._to_signed16b(((rawx & 0x00ff) << 8) | ((rawx & 0xff00) >> 8))
        rawy = (self.comm.read_word(self.addr, self.DATAY0))
        y = self._to_signed16b(((rawy & 0x00ff) << 8) | ((rawy & 0xff00) >> 8))
        rawz = (self.comm.read_word(self.addr, self.DATAZ0))
        z = self._to_signed16b(((rawz & 0x00ff) << 8) | ((rawz & 0xff00) >> 8))

        return (x, y, z)
            
    def get_data(self):
        (x, y, z) = self.get_data_int()
        
        return (x*0.00377, y*0.00377, z*0.0039)
            
    def is_data_ready(self):
        return (self.comm.read_byte(self.addr, 0x30) & 0x80) != 0

    
    def _to_signed16b(self, num):
        if ((num & 0x8000) != 0):
            return num - 0xffff - 1
        else:
            return num
        
    def _to_unsigned8b(self, num):
        if (num < 0):
            return num + 0xff + 1
        else:
            return num
        
        
    
    