'''
Created on 18. 2. 2014

@author: ondra
'''

class Gyro(object):
    '''
    classdocs
    '''

    WHOAMI = 0x00
    
    PWRM = 0x3e
    SMPL = 0x15
    DLPF_FS = 0x16
    
    ICONF = 0x17
    ISTAT = 0x1a
    
    TEMPH = 0x1b
    TEMPL = 0x1c

    DATAXH = 0x1d
    DATAXL = 0x1e
    DATAYH = 0x1f
    DATAYL = 0x20
    DATAZH = 0x21
    DATAZL = 0x22
    
    off_x = 0
    off_y = 0
    off_z = 0
    
    FILTER_256_SR_8K = 0
    FILTER_188_SR_1K = 1
    FILTER_98_SR_1K = 2
    FILTER_42_SR_1K = 3
    FILTER_20_SR_1K = 4
    FILTER_10_SR_1K = 5
    FILTER_5_SR_1K = 6
    

    def __init__(self, comm, addr, fil=FILTER_98_SR_1K, smpl_div=9, calibrate=False):
        '''
        Constructor
        '''
        self.comm = comm
        self.addr = addr
        
        self.comm.write_byte(self.addr, self.PWRM, 0x80)
        self.comm.write_byte(self.addr, self.PWRM, 0x01)
        
        self.comm.write_byte(self.addr, self.SMPL, smpl_div)
        print(bin(self.comm.read_byte(self.addr, self.SMPL)))
        self.comm.write_byte(self.addr, self.DLPF_FS, 0x18 | fil)
        print(bin(self.comm.read_byte(self.addr, self.DLPF_FS)))
        
        while (self.comm.read_byte(self.addr, self.ISTAT) & 0x04) == 0:
            pass
        
        if calibrate:
            self.calibrate()
        
        
    def calibrate(self):
        num_samples = 100
        
        x = 0
        y = 0
        z = 0
        
        for _ in range(num_samples):
            cur = self.get_data_int()
            x += cur[1]
            y += cur[2]
            z += cur[3]
            
        x /= num_samples
        y /= num_samples
        z /= num_samples
        
        print(x, y, z)
        
        self.off_x = -x
        self.off_y = -y
        self.off_z = -z
        
        
        
    def get_whoami(self):
        return self.comm.read_byte(self.addr, self.WHOAMI)
    
    def get_data_int(self):
        
        while (self.comm.read_byte(self.addr, self.ISTAT) & 0x01) == 0:
            pass
               
        temp = self._to_signed16b(self.comm.read_word(self.addr, self.TEMPH))
        

        x = self._to_signed16b(self.comm.read_word(self.addr, self.DATAXH)) + self.off_x 
        y = self._to_signed16b(self.comm.read_word(self.addr, self.DATAYH)) + self.off_y
        z = self._to_signed16b(self.comm.read_word(self.addr, self.DATAZH)) + self.off_z
        
        return (temp, x, y, z) 
        
    def get_data(self):
        
        (temp, x, y, z) = self.get_data_int()    
    
        return (35 + (float(temp)+13200)/280, x/14.375, y/14.375, z/14.375)


    def _to_signed16b(self, num):
        if ((num & 0x8000) != 0):
            return num - 0xffff - 1
        else:
            return num
