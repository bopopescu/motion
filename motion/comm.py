'''
Created on 18. 2. 2014

@author: ondra
'''

from pyBusPirateLite.I2Chigh import *  # @UnusedWildImport


class Comm(object):
    '''
    classdocs
    '''


    def __init__(self, path):
        '''
        Constructor
        '''
        self.i2c = I2Chigh(path, 115200)
        self.i2c.BBmode()
        self.i2c.enter_I2C()
        self.i2c.cfg_pins(I2CPins.POWER | I2CPins.PULLUPS)
        self.i2c.set_speed(I2CSpeed._100KHZ)
        self.i2c.timeout(0.2)
        
    def close(self):
        self.i2c.resetBP()

    def read_byte(self, i2caddr, regaddr):
        return self.i2c.get_byte(i2caddr, regaddr)
    
    def read_word(self, i2caddr, regaddr):
        return self.i2c.get_word(i2caddr, regaddr)
    
    def write_byte(self, i2caddr, regaddr, byte):
        self.i2c.set_byte(i2caddr, regaddr, byte)
    
    def write_word(self, i2caddr, regaddr, word):
        self.i2c.set_word(i2caddr, regaddr, word)
        
    def read_buf(self, i2caddr, regaddr, length):
        self.i2c.send_start_bit();
        stat = self.i2c.bulk_trans(2, [i2caddr<<1, regaddr]);
        self.i2c.send_start_bit();
        stat += self.i2c.bulk_trans(1, [i2caddr<<1 | 1]);
        
        buf = []
        for _ in range(length):
            buf.append(ord(self.i2c.read_byte()))
        
        self.i2c.send_nack();
        self.i2c.send_stop_bit();
        if stat.find(chr(0x01)) != -1:
            raise IOError, "I2C command on address 0x%02x not acknowledged!"%(i2caddr);
        return buf
    
    
    