import connect  
from tkinter import *  
from tkinter.ttk import Combobox  
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  
import matplotlib.pyplot as plt  
from tkmacosx import Button  # Import the Button class from tkmacosx

# Create the main window
window = Tk()
window.geometry("1000x800")
window.title("")

# Create a figure and axes for the plot
fig, ax = plt.subplots(figsize=(4, 2))
line, = ax.plot([])
ax.set_xlabel('Time')
ax.set_ylabel('Signal')

# Create a canvas for the plot
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.get_tk_widget().place(x=100, y=80, width=800, height=450)

# Create buttons for various actions
button_on = Button(window, text="START", command=connect.start_acquisition)
button_on.place(x=350,y=550)
button_off = Button(window, text="STOP", command=connect.stop_acquisition)
button_off.place(x=475,y=550)
button_save = Button(window, text = "SAVE", command=connect.save)
button_save.place(x=600,y=550)
button_error = Button(window, bg="#82CC6C",height= 20, width=30)
button_error.place(x=920,y=715)
button_set = Button(window, text="SET PARAMETERS", command=connect.set_parameters)
button_set.place(x= 450,y=675)
button_connect = Button(window, text="CONNECT", command=connect.find_port)
button_connect.place(x=750, y=30)
button_draw = Button(window, text="DRAW", command=connect.draw)
button_draw.place(x=200, y=550)

# Create labels for parameters
gain = Label(window,text = "Gain",font=('Calibri',20))
gain.place(x=150,y =585)

bandwidth = Label(window,text = "Bandwidth",font=('Calibri',20))
bandwidth.place(x=600,y =585)

amplifier = Label(window,text = "LOW NOISE AMPLIFIER",font=('Helvetica bold',20))
amplifier.place(x=400,y =30)

# High pass bandwidth options
options1 = [1, 100, 1000, 10000]
# Low pass bandwidth options
options2 = [10000, 20000, 30000, 40000]
# Gain options
options3 = [1, 10, 100, 500]

# Function to handle combobox selection
def on_select(event=None):
    print(combo1.get(), combo2.get(), combo3.get())

# Create the combobox for the high pass bandwidth
combo1 = Combobox(window, values=options1)
combo1.current(0)  # Default option
combo1.bind('<<ComboboxSelected>>', on_select)
combo1.place(x=450,y= 620)

# Create the combobox for the low pass bandwidth
combo2 = Combobox(window, values=options2)
combo2.current(0)  # Default option
combo2.bind('<<ComboboxSelected>>', on_select)
combo2.place(x=700,y= 620)

# Create the combobox for the gain
combo3 = Combobox(window, values=options3)
combo3.current(0)  # Default option
combo3.bind('<<ComboboxSelected>>', on_select)
combo3.place(x=100,y= 620)

# Adjust the plot layout 
fig.tight_layout(pad=3.0)

# Draw the canvas
canvas.draw()
