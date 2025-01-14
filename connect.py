import GUI  
import time  
import serial  
import serial.tools.list_ports  
import csv  
from collections import deque  # Importing a deque data structure for circular buffering
import threading
import matplotlib.animation as animation
import matplotlib.pyplot as plt  

start = 0
ser = None
buffer_length = 6000 
circular_buffer = deque(maxlen=buffer_length)  # Circular buffer for incoming data
voltage = 3.3 # Voltage value for scaling
array = [0, 0, 0]
processed_buffer = []


# Function to establish a serial connection with the specified port
def find_port():
    global ser
    portsFound = serial.tools.list_ports.comports()
    commPort = 'None'
    numConnection = len(portsFound)

    for i in range(0, numConnection):
        port = portsFound[i]
        strPort = str(port)

        if 'STLink' in strPort:
            splitPort = strPort.split(' ')
            commPort = (splitPort[0])

    connectPort = commPort
    if connectPort != 'None':
        try:
            ser = serial.Serial(connectPort, baudrate=1000000, bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE, timeout=1)
            print('Connected to ' + connectPort)

            # Sending a sequence of zeros and waiting for a response
            ser.write(b'\x00')
            response = ser.read_until(b'\x00', 1)
            if response == b'\x00':
                print('Communication established.')
                GUI.button_error.config(bg="#82CC6C") # Updating GUI button color
                # while True:
                #     data = ser.read_until(b'\n')
                #     if data:
                #         circular_buffer.append(data)
                #     else:
                #         time.sleep(0.01)
                #     if len(circular_buffer) == buffer_length:
                #         break
                # GUI.update_plot() # Updating the GUI plot
            else:
                print('Failed to establish communication.')
                GUI.button_error.config(bg="#FF5733") # Updating GUI button color
                return
            print('DONE')
        
        except serial.SerialException as e:
            print('Serial connection error:', str(e))
    else:
        print('Connection Issue!')


# Function to send a command to the microcontroller    
def send_command(command):
    ser.write(command)
    response = ser.read(1)
    return response   


def bufor():
    global circular_buffer
    global start
    response = send_command(b'\x00') # Send a command to establish communication
    if response == b'\x00':
        print('Communication established') 
        # GUI.button_error.config(bg="#82CC6C") # Updating GUI button color
    else:
        print('Failed to establish communication.') 
        # GUI.button_error.config(bg="#FF5733") # Updating GUI button color
        return   
    while start:
        data = ser.read()
        if data:
            circular_buffer.append(data) 
        
            for i in range(0, len(circular_buffer), 3):
                    value1 = ((ord(circular_buffer[i])) | (ord(circular_buffer[i + 1]) << 8)) & 0xFFF
                    scaled_value1 = (value1 * voltage) / (2 ** 12)
                    processed_buffer.append(scaled_value1)

                    value2 = ((ord(circular_buffer[i+1]) >> 4) | (ord(circular_buffer[i + 2]) << 4)) & 0xFFF
                    scaled_value2 = (value2 * voltage) / (2 ** 12)
                    processed_buffer.append(scaled_value2)

            circular_buffer.clear()
            print('Acquisition started!')     
    

# Function to start the data acquisition process
def start_acquisition():
    z = threading.Thread(target=bufor, args=())
    z.daemon = True
    z.start()
    
# Function to stop acquisition    
def stop_acquisition():
    # global stop_flag 
    # stop_flag = True # Set stop flag to stop acquisition
    global start
    global ser
    start = 0
    send_command(b'\x00') 
    print('Acquisition stopped!')
    ser.close()

# Function to set parameters
def set_parameters():
    gain_value = int(GUI.combo3.get()) # Get selected gain value from the GUI
    # Define bit values for each gain option
    gain_1 = 0b000001
    gain_10 = 0b000010
    gain_100 = 0b000100
    gain_500 = 0b001000
    
    # Determine which gain value to use based on the selected scale value
    if gain_value == 1:
        gain = gain_1
    elif gain_value == 10:
        gain = gain_10
    elif gain_value == 100:
        gain = gain_100
    else:
        gain = gain_500
    
    # Send the gain value to the microcontroller
    send_command(gain)

    band_value_1 = int (GUI.combo1.get()) # Get selected band value from the GUI
    band_value_2 = int (GUI.combo2.get())

    # Define bit values for each bandwidth option
    band_1_10k = 0b000011
    band_1_20k = 0b000111
    band_1_30k = 0b001111
    band_1_40k = 0b011111
    band_10_10k = 0b111111
    band_10_20k = 0b111110
    band_10_30k = 0b111100
    band_10_40k = 0b111000
    band_100_10k = 0b110000
    band_100_20k = 0b100000
    band_100_30k = 0b000000
    band_100_40k = 0b101000
    band_1k_10k = 0b101100
    band_1k_20k = 0b101110
    band_1k_30k = 0b101111
    band_1k_40k = 0b101101

    # Determine which bandwidth value to use based on the selected band values
    if band_value_1 == 1 and band_value_2 == 10000:
        bandwidth = band_1_10k
    elif band_value_1 == 1 and band_value_2 == 20000:
         bandwidth = band_1_20k
    elif band_value_1 == 1 and band_value_2 == 30000:
         bandwidth = band_1_30k    
    elif band_value_1 == 1 and band_value_2 == 40000:
         bandwidth = band_1_40k    
    elif band_value_1 == 10 and band_value_2 == 10000:
         bandwidth = band_10_10k   
    elif band_value_1 == 10 and band_value_2 == 20000:
         bandwidth = band_10_20k    
    elif band_value_1 == 10 and band_value_2 == 30000:
         bandwidth = band_10_30k  
    elif band_value_1 == 10 and band_value_2 == 40000:
         bandwidth = band_10_40k 
    elif band_value_1 == 100 and band_value_2 == 10000:
         bandwidth = band_100_10k   
    elif band_value_1 == 100 and band_value_2 == 20000:
         bandwidth = band_100_20k    
    elif band_value_1 == 100 and band_value_2 == 30000:
         bandwidth = band_100_30k  
    elif band_value_1 == 100 and band_value_2 == 40000:
         bandwidth = band_100_40k   
    elif band_value_1 == 1000 and band_value_2 == 10000:
         bandwidth = band_1k_10k   
    elif band_value_1 == 1000 and band_value_2 == 20000:
         bandwidth = band_1k_20k    
    elif band_value_1 == 1000 and band_value_2 == 30000:
         bandwidth = band_1k_30k  
    elif band_value_1 == 1000 and band_value_2 == 40000:
         bandwidth = band_1k_40k    

    send_command(bandwidth)           
      
# Function to save the data from the circular buffer to a CSV file
def save_to_csv():
        filename = 'data.csv'
        global processed_buffer
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            header = ['Timestamp', 'Gain', 'Bandwidth'] 
            writer.writerow(header)
            while True:
                writer.writerow(processed_buffer)
        
        print("Data saved to CSV file!")

def save():
    x = threading.Thread(target=save_to_csv, args=())
    x.daemon = True
    x.start()

def animate(i, dataList, ser):
    ser.write(b'g')                                     # Transmit the char 'g' to receive the Arduino data point
    arduinoData_string = ser.readline().decode('ascii') # Decode receive Arduino data as a formatted string
    #print(i)                                           # 'i' is a incrementing variable based upon frames = x argument

    try:
        arduinoData_float = float(arduinoData_string)   # Convert to float
        dataList.append(arduinoData_float)              # Add to the list holding the fixed number of points to animate

    except:                                                                          
        pass

    dataList = dataList[-50:]                           # Fix the list size so that the animation plot 'window' is x number of points
    
    ax.clear()                                          
    ax.plot(dataList)                                   
    
    ax.set_ylim([0, 1200])                              
    ax.set_title("Arduino Data")                        
    ax.set_ylabel("Value")                              


def draw():
    global ax
    
    dataList = []                                        
    fig = plt.figure()                                      
    ax = fig.add_subplot(111)                              

    ani = animation.FuncAnimation(fig, animate, frames=100, fargs=(dataList, ser), interval=100) 

    plt.show()         
    y = threading.Thread(target= ani , args=())
    y.daemon = True
    y.start()