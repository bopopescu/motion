'''
Created on 21. 2. 2014

@author: ondra
'''

class Compass(object):
    '''
    classdocs
    '''
    
    CRA = 0
    CRB = 1
    MR = 2
    SR = 9
    
    DATAXH = 3
    DATAXL = 4
    DATAZH = 5
    DATAZL = 6
    DATAYH = 7
    DATAYL = 8

    IDA = 10
    IDB = 11
    IDC = 12
    
    OUTPUT_RATE_0_75 = 0
    OUTPUT_RATE_1_5 = 1
    OUTPUT_RATE_3 = 2
    OUTPUT_RATE_7_5 = 3
    OUTPUT_RATE_15 = 4
    OUTPUT_RATE_30 = 5
    OUTPUT_RATE_75 = 6
    
    NO_BIAS = 0
    BIAS_POS_XY_NEG_Z = 1
    BIAS_NEG_XY_POS_Z = 2

    GAIN_0_9 = 0
    GAIN_1_2 = 1
    GAIN_1_9 = 2
    GAIN_2_5 = 3
    GAIN_4_0 = 4
    GAIN_4_6 = 5
    GAIN_5_5 = 6
    GAIN_7_9 = 7
    
    MODE_CONT = 0
    MODE_SINGLE = 1
    MODE_IDLE = 2
    MODE_SLEEP = 3
    

    def __init__(self, comm, addr, output_rate=OUTPUT_RATE_15, gain=GAIN_1_2, declination=0, inclination=0):
        '''
        Constructor
        '''
        self.comm = comm
        self.addr = addr
        self.gain = gain
    
        self.declination = declination
        self.inclination = inclination

        
        self.comm.write_byte(self.addr, self.CRA, output_rate << 2)
        
        self.comm.write_byte(self.addr, self.CRB, gain << 5)
        
        self.comm.write_byte(self.addr, self.MR, self.MODE_CONT)
        
    
    def get_data_int(self):        
        while not self.is_data_ready():
            pass
                
        x = self._to_signed16b(self.comm.read_word(self.addr, self.DATAXH))
        z = self._to_signed16b(self.comm.read_word(self.addr, self.DATAZH))
        y = self._to_signed16b(self.comm.read_word(self.addr, self.DATAYH))
        
        return (x, y, z)
    
    
    def get_id(self):
        ida = self.comm.read_byte(self.addr, self.IDA)
        idb = self.comm.read_byte(self.addr, self.IDB)
        idc = self.comm.read_byte(self.addr, self.IDC)
        
        return (ida, idb, idc)
    
    
    def _to_signed16b(self, num):
        if ((num & 0x8000) != 0):
            return num - 0xffff - 1
        else:
            return num

        
        
    def is_data_ready(self):
        val = self.comm.read_byte(self.addr, self.SR)
        return (val & 0x01) != 0
        
        
        