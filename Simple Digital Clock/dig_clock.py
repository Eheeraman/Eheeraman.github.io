from tkinter import *
import time
clk = Tk()
clk.title("Clock")
clk.geometry("1350x700+0+0") # set the display
clk.config(bg = "#1E1E1E")


def clock():
    hr = str(time.strftime("%H"))
    min = str(time.strftime("%M"))
    sec = str(time.strftime("%S"))
#   print(hr, min, sec) <---- Keep for testing
    
    # 24-hour to 12-hour format conversion and AM/PM detection
    if int(hr) >= 12:
        dn = "PM"
        hr = str(int(hr) - 12) if int(hr) > 12 else hr
    else:
        dn = "AM"
        hr = hr if int(hr) > 0 else "12"  # Adjust 00 to 12 for AM
    
    hr_title.config(text=hr)
    min_title.config(text=min)
    sec_title.config(text=sec)
    dn_title.config(text=dn)
    
    hr_title.after(200, clock) # Makes clock update every second

# Hour section
hr_title = Label(clk, text = "12", font = ("Times 20 bold", 75, 'bold'), bg = "#3371ff", fg = "white")
hr_title.place(x = 350, y = 200, width = 150, height = 150)

hr_title_txt = Label(clk, text = "HOURS", font = ("Times 20 bold", 20, "bold"), bg = "#3371ff", fg = "white")
hr_title_txt.place(x = 350, y = 145, width = 150, height = 50)

# Minute section
min_title = Label(clk, text = "12", font = ("Times 20 bold", 75, 'bold'), bg = "#2196F3", fg = "white")
min_title.place(x = 520, y = 200, width = 150, height = 150)

min_title_txt = Label(clk, text = "MINUTES", font = ("Times 20 bold", 20, "bold"), bg = "#2196F3", fg = "white")
min_title_txt.place(x = 520, y = 145, width = 150, height = 50)

# Second section
sec_title = Label(clk, text = "12", font = ("Times 20 bold", 75, 'bold'), bg = "#26d7af", fg = "white")
sec_title.place(x = 690, y = 200, width = 150, height = 150)

sec_title_txt = Label(clk, text = "SECONDS", font = ("Times 20 bold", 20, "bold"), bg = "#26d7af", fg = "white")
sec_title_txt.place(x = 690, y = 145, width = 150, height = 50)

# AM/PM Section
dn_title = Label(clk, text = "AM", font = ("Times 20 bold", 70, 'bold'), bg = "#8d33ff", fg = "white")
dn_title.place(x = 860, y = 200, width = 150, height = 150)

dn_title_txt = Label(clk, text = "NOON", font = ("Times 20 bold", 20, "bold"), bg = "#8d33ff", fg = "white")
dn_title_txt.place(x = 860, y = 145, width = 150, height = 50)


# Title box section
title_txt = Label(clk, text="DIGITAL CLOCK", font=("Times 20 bold", 40, 'bold'), bg="#891a81", fg="white")
title_txt.place(x = 450, y = 85, width = 450, height = 50)



# Calls the clock function to begin
clock()
clk.mainloop()