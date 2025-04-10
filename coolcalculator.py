
import math
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Note to self: This would be a good usecase for tuples. Next time maybe put the data as Inputs= ("Shape", "Evnvironment", "Material", T_initial, T_env, Volume, Time))
# then create a list: Parameters = [transferc, m, heat_capacity, epsilon, A, T_initial, T_env, Volume, Time] and calculate everything with the list entries
# that would probably be a lot cleaner and easier to read

def validate_input(char):
    # Allow only digits
    return char.isdigit()


# stephan boltzmann constant
sigma = 5.67/(10**8)
# all input parameters are listed here:
Volume = 0
EnvTemp = 0
shape = "Sphere"
envi = "Air"
material = "Water"
Temp_initial= 100


Finallabel= None

# Function to calculate the temperature of the object after a given time
# using Newton's law of cooling and the Stefan-Boltzmann law for cooling in space

def calculate():


    Volume = float(Volumeentry.get()) / 1000000
    EnvTemp = float(EnvTempentry.get()) + 273.15
    shape = clicked.get()
    envi = clicked2.get()
    material = clicked3.get()
    Temp_initial= float(Tempentry.get()) + 273.15
    t=float(Timeentry.get())

    # get heat tranfer coefficients for different environments

    if envi == "Air":
        transferc = 25

    elif envi == "Water":
        transferc = 1000

    elif envi == "Space":
        transferc = 0.1

    #get surface area

    if shape == "Sphere":
        r= (3*Volume/(4*math.pi))**(1. /3)
        A= 3 *Volume/r

    elif shape == "Cylinder":
        cyl_height= float(Heightentry.get())/100
        r= math.sqrt(Volume/(cyl_height*math.pi))
        A= (2*math.pi*r*(r+cyl_height))

    elif shape == "Cube":
        A= 6*Volume**(2. /3)

    #get some material properties of the object

    if material == "Water":
        m= 997*Volume
        heat_capacity= 4186
        epsilon = 0.95

    elif material == "Glass":
        m= 2500*Volume
        heat_capacity= 840
        epsilon= 0.9

    elif material == "Copper":
        m= 8850*Volume
        heat_capacity= 385
        epsilon = 0.05



    

#cooling in space via blackbody radiation 
    if envi == "Space":
        big_constant = 3* sigma * epsilon * A /(m*heat_capacity)
        T= (big_constant*t + 1/(Temp_initial)**3)**(-1/3) - 273.15
    
    else:
        #Newtons law of cooling
        k= (transferc * A /(m*heat_capacity))
        T= EnvTemp+(Temp_initial - EnvTemp)*np.exp(-k*t) - 273.15
        
    T_rounded = round(T, 3)  

    global Finallabel

# Check if the object temperature is below absolute zero
    if Temp_initial < 0:
        if Finallabel:
            Finallabel.destroy()
        tk.messagebox.showerror("TooCoolForSchool.exe", "I enjoy your enthusiasm about testing cooling rates, I really do! \nBut now you've crossed the line. I can't allow this anymore. I'm sorry")

        Finallabel = tk.Label(root, text=f"Your {material} {shape} is now breaking the law! ",
                              font=('Helvetica', 15))
        Finallabel.place(x=500, y=200)
    else:
        if Finallabel:
            Finallabel.destroy()
        Finallabel = tk.Label(root, text=f"Your {material} {shape} is now at {T_rounded}\N{DEGREE SIGN}C! ",
                              font=('Helvetica', 15))
        Finallabel.place(x=500, y=200)

# check if environment temperature is below absolute zero (this implementation is horrible but it worked)
    if EnvTemp < 0:
        if Finallabel:
            Finallabel.destroy()
        tk.messagebox.showerror("2 parallel universes ahead of you",
                                "Your environment very cool...\nToo cool perhaps. Maybe enter something above 0 Kelvin")

        Finallabel = tk.Label(root, text=f"Your {material} {shape} is now gone! ",
                              font=('Helvetica', 15))
        Finallabel.place(x=500, y=200)
    else:
        if Temp_initial >= 0:
            if Finallabel:
                Finallabel.destroy()
            Finallabel = tk.Label(root, text=f"Your {material} {shape} is now at {T_rounded}\N{DEGREE SIGN}C! ",
                                font=('Helvetica', 15))
            Finallabel.place(x=500, y=200)

# Plot the temperature over time

#first destroy existing plot 
    plt.close('all')

    data_t = np.linspace(start=0, stop=int(t), num=1000)
    if envi == "Space":
        data_Temp= (big_constant*data_t + 1/(Temp_initial)**3)**(-1/3) - 273.15
    else:
        data_Temp = EnvTemp+(Temp_initial - EnvTemp)*np.exp(-k*data_t) - 273.15

    

    fig, ax = plt.subplots(figsize=(8,5))
    ax.plot(data_t, data_Temp)

    ax.set_title("Temperature over time")
    ax.set_xlabel("Time in seconds")
    ax.set_ylabel("Temperature in \N{DEGREE SIGN}C")

    canvas = FigureCanvasTkAgg(fig, master=root)  # root is the tk.Tk() window

    # Get the canvas widget and pack it into the tkinter window
    canvas.get_tk_widget().place(x=20, y=320)


# Make a height entry if cylinder is selected
def on_dropdown_change(event=None):
    global Heightentry
    global Heightlabel
    # Get the selected value from the dropdown
    shape = clicked.get()

    if Heightentry:
        Heightentry.destroy()
        Heightlabel.destroy()
    # Check if the selected value matches the condition
    if shape == "Cylinder":

        Heightlabel = tk.Label(root, text="Height(cm):", font=('Helvetica', 15))
        Heightlabel.place(x=20, y=250)

        Heightentry = tk.Entry(root, width=10, font=('Helvetica', 12), validate="key", validatecommand=(validate_cmd, "%P"))
        Heightentry.place(x=162, y=255)

        pass

Heightentry=None
Heightlabel=None


# INTERFACE

# dropdown shape
root = tk.Tk()

root.geometry("900x900")

clicked = tk.StringVar()

Shapelabel = tk.Label(root,  text="Shape:", font=('Helvetica', 15))
Shapelabel.place(x=20, y=100)

drop = tk.OptionMenu(root, clicked,  "Sphere", "Cylinder", "Cube" , command=on_dropdown_change)
drop.place(x=160, y=100)
clicked.set("Sphere")

# dropdown material
clicked3 = tk.StringVar()

Matlabel = tk.Label(root, text="Material:", font=('Helvetica', 15))
Matlabel.place(x=20, y=50)

drop = tk.OptionMenu(root, clicked3, "Water", "Glass", "Copper")
drop.place(x=160, y=50)
clicked3.set("Water")

# Validating input to fix bug
def validate_input(value_if_allowed):
    if value_if_allowed == "":
        return True
    try:
        float(value_if_allowed)
        return True
    except ValueError:
        if value_if_allowed in ("-", ".", "-.", ".-"):
            return True
        else:
            return False

# Create a validation function
validate_cmd = root.register(validate_input)

# Title:
Titlelabel = tk.Label(root, text="Cool Calculator", font=('Helvetica 20 bold'))
Titlelabel.place(x=20, y=0)

# Volume label
Volumelabel = tk.Label(root, text="Volume(cm\u00b3):", font=('Helvetica', 15))
Volumelabel.place(x=20, y=150)

Volumeentry = tk.Entry(root, width=10, font=('Helvetica', 12), validate="key", validatecommand=(validate_cmd, "%P"))
Volumeentry.place(x=162, y=155)

Templabel = tk.Label(root, text="Temp_Obj(\N{DEGREE SIGN}C):", font=('Helvetica', 15))
Templabel.place(x=20, y=200)

Tempentry = tk.Entry(root, width=10, font=('Helvetica', 12), validate="key", validatecommand=(validate_cmd, "%P"))
Tempentry.place(x=162, y=205)

submit_button = tk.Button(root, text="Calculate", command=calculate)
submit_button.place(x=700, y=250)

# dropdown menu
Envilabel = tk.Label(root, text="Environment:", font=('Helvetica', 15))
Envilabel.place(x=500, y=50)

clicked2 = tk.StringVar()

drop2 = tk.OptionMenu(root, clicked2, "Air", "Water", "Space" )
drop2.place(x=660, y=50)
clicked2.set("Air")

Templabel = tk.Label(root, text="Temperature(\N{DEGREE SIGN}C):", font=('Helvetica', 15))
Templabel.place(x=500, y=100)

EnvTempentry = tk.Entry(root, width=10, font=('Helvetica', 12), validate="key", validatecommand=(validate_cmd, "%P"))
EnvTempentry.place(x=662, y=105)

Timelabel = tk.Label(root, text="Time(s):", font=('Helvetica', 15))
Timelabel.place(x=500, y=150)

Timeentry = tk.Entry(root, width=10, font=('Helvetica', 12), validate="key", validatecommand=(validate_cmd, "%P"))
Timeentry.place(x=662, y=155)

# this fixes another bug where the code could only be run once

def on_close():
    print("Window closed.")
    plt.close('all')  # Close all matplotlib figures
    root.destroy()  # Destroy the Tkinter root window
    
root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
