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
    DLPF_FS = 0x16
    
    
    TEMPH = 0x1b
    TEMPL = 0x1c

    DATAXH = 0x1d
    DATAXL = 0x1e
    DATAYH = 0x1f
    DATAYL = 0x20
    DATAZH = 0x21
    DATAZL = 0x22

    def __init__(self, comm, addr):
        '''
        Constructor
        '''
        self.comm = comm
        self.addr = addr
        
        self.comm.write_byte(self.addr, self.PWRM, 0x80)
        self.comm.write_byte(self.addr, self.DLPF_FS, 0x19)
        
        
    def get_whoami(self):
        return self.comm.read_byte(self.addr, self.WHOAMI)
    
    def get_data(self):
        temp = (self.comm.read_word(self.addr, self.TEMPH))
        ttemp = ((temp & 0x00ff) << 8) | ((temp & 0xff00) >> 8)
        ttt = self._to_signed16b(ttemp)
        

        tx = (self.comm.read_word(self.addr, self.DATAXH))
        ttx = ((tx & 0x00ff) << 8) | ((tx & 0xff00) >> 8)
        x = self._to_signed16b(ttx) 
        ty = (self.comm.read_word(self.addr, self.DATAYH))
        tty = ((ty & 0x00ff) << 8) | ((ty & 0xff00) >> 8)
        y = self._to_signed16b(tty) 
        tz = (self.comm.read_word(self.addr, self.DATAZH))
        ttz = ((tz & 0x00ff) << 8) | ((tz & 0xff00) >> 8)
        z = self._to_signed16b(ttz) 
        
        return (ttt, x, y, z)


    def _to_signed16b(self, num):
        if ((num & 0x8000) != 0):
            return num - 0xffff - 1
        else:
            return num
