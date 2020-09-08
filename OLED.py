import smbus

Bus = smbus.SMBus(1)
address = 0x3c
Brightness = 0xBF

def Write_Command(data):
    Bus.write_byte_data(address,0x00,data)

def write_Data(data):
    Bus.write_byte_data(address,0x40,data)

def Set_Command_Lock(d):
    Write_Command(0xFD)
    Write_Command(d)

def Set_Display_on_off(d):
    Write_Command(d)

def Set_Display_Clock(d):
    Write_Command(0xA5)
    Write_Command(d)

def Set_Multiplexer_Ratio(d):
    Write_Command(0xA8)
    Write_Command(d)

def Set_Display_Offset(d):
    Write_Command(0xD3)
    Write_Command(d)

def Set_Start_Line(d):
    Write_Command(0x40|d)

def Set_Low_Power(d):
    Write_Command(0x08)
    Write_Command(d)

def Set_Addressing_mode(d):
    Write_Command(0x20)
    Write_Command(d)

def Set_Segment_Remap(d):
    Write_Command(d)

def Set_Comman_Remap(d):
    Write_Command(d)

def Set_Common_Config(d):
    Write_Command(0xDA)
    Write_Command(d)

def Set_Contrast_Control(d):
    Write_Command(0x81)
    Write_Command(d)

def Set_Precharge_Period(d):
    Write_Command(0xD9)
    Write_Command(d)

def Set_VCOMH(d):
    Write_Command(0xD8)
    Write_Command(d)

def Set_Entire_Display(d):
    Write_Command(d)

def Set_Inverse_Display(d):
    Write_Command(d)

def Set_Start_Colum(d):
    Write_Command(0x00+d%16)
    d = int(d/16)
    Write_Command(0x10+d)

def Set_Start_Page(d):
    Write_Command(0xB0|d)

def Fill_RAM(data):
    for i in range(8):
        Set_Start_Page(i)
        Set_Start_Colum(0x00)
        for j in range(128):
            Bus.write_byte_data(address,0x40,data)
def Fill_Block(data,a,b,c,d):
    for i in range(b+1):
        Set_Start_Page(i)
        Set_Start_Column(c)
        
    for j in range(d):
        Bus.write_byte_data(address,0x40,data)

def Test_Pixel(data):
    for i in range(8):
        Set_Start_Page(i)
        Set_Start_Colum(0x00)
        for j in range(128):
            Bus.write_byte_data(address,0x40,data)

def Checkerboard():
    for i in range(3):
        Set_Start_Page(i)
        Set_Start_Colum(0x00)
        
    for j in range(1):
        #Bus.write_byte_data(address,0x40,0x00)
        Bus.write_byte_data(address,0x40,0xFF)
array = [0]*1040
WIDTH = 128
HEIGHT = 64
def Draw_Pixel(x,y):
    flag = int(y/8)
    n = y%8
    
    var = array[x+(flag)*WIDTH]<<n
    array[x+(flag)*WIDTH] |= var
    
def Flush():
    Bus.write_i2c_block_data(address,0x00,[0x00,0x10,0x40])
    #twrbackup = TWBR
    TWBR = 12
    twrbackup = TWBR
    flagie = int(WIDTH*HEIGHT/8)
    for q in range(flagie):
        for w in range(16):
            Bus.write_byte_data(address,0x40,array[q])
            q = q+1
        q = q-1
    #TWBR = twbrbackup
    
def setup():
    Set_Command_Lock(0x12)
    Set_Display_on_off(0xAE)
    Set_Display_Clock(0xA0)
    Set_Multiplexer_Ratio(0x3F)
    Set_Display_Offset(0x00)
    Set_Start_Line(0x00)
    Set_Low_Power(0x05)      #// Set Low Power Display Mode (0x04/0x05)
    Set_Addressing_mode(0x02)  #  // Set Page Addressing Mode (0x00/0x01/0x02)
    Set_Segment_Remap(0xA1)   #// Set SEG/Column Mapping (0xA0/0xA1)
    Set_Comman_Remap(0xC8)    #// Set COM/Row Scan Direction (0xC0/0xC8)
    Set_Common_Config(0x12)  # // Set Alternative Configuration (0x02/0x12)
    Set_Contrast_Control(Brightness); #// Set SEG Output Current
    Set_Precharge_Period(0x25)  #// Set Pre-Charge as 2 Clocks & Discharge as 5 Clocks
    Set_VCOMH(0x34)     # // Set VCOM Deselect Level
    Set_Entire_Display(0xA4) #  // Disable Entire Display On (0xA4/0xA5)
    Set_Inverse_Display(0xA6) #  // Disable Inverse Display On (0xA6/0xA7)

    Fill_RAM(0x00)      #// Clear Screen

    Set_Display_on_off(0xAF)


setup()
#Fill_RAM(0xAA)
#Checkerboard()
#Write_Data(0xFF)
Draw_Pixel(50,40)
Flush()
