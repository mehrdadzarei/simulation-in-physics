from Tkinter import *
import turtle as tr
from PIL import ImageTk
import Pmw
import fractal

step = ("0", "1", "2", "3", "4", "5", "6", "7", "8","9","10","11","12","13","14","15","16")
fractals = ("Von Koch (step max 8)", "Heighway`s Dragon", "Serpinescy Triangle",
           "Von Koch (random)", "Serpinescy Triangle (random)", "Sarakhs")

def start(event):
   if typef.get()=='Von Koch (step max 8)':
      if int(stp.get())!=0:
         dim = fractal.koch(int(stp.get()))
         run_turtle(len(dim), dim)
      else:
         turtle.reset(); turtle.ht()
         turtle.pu(); turtle.goto(-150,-50); turtle.pd(); 
         turtle.goto(150,-50)
         turtle.pu(); turtle.goto(-150,-50); turtle.pd()
   elif typef.get()=='Heighway`s Dragon':
      if int(stp.get())!=0:
         dim = fractal.dragon(int(stp.get()))
         run_turtle(len(dim), dim)
      else:
         turtle.reset(); turtle.ht()
         turtle.pu(); turtle.goto(-150,-50); turtle.pd(); 
         turtle.goto(150,-50)
         turtle.pu(); turtle.goto(-150,-50); turtle.pd()
   elif typef.get()=='Serpinescy Triangle':
      turtle.reset();turtle.ht()
      turtle.speed(1)
      initialpoints = [[-100,-50],[0,100],[100,-50]]
      run_serpin(initialpoints,int(stp.get()))
   elif typef.get()=='Serpinescy Triangle (random)':
      points = fractal.serpin(int(stp.get()))
      rand(points)
   elif typef.get()=='Von Koch (random)':
      points = fractal.kochrand(int(stp.get()))
      rand(points)
   elif typef.get()=='Sarakhs':
      points = fractal.sarakhs(int(stp.get()))
      rand(points)

def close(event):
   quit()

def run_turtle(d, v):
   turtle.reset(); turtle.ht()
   turtle.pu(); turtle.goto(-150,-50); turtle.pd()
   j = 0
   for i in range(d):
      if j<50:
         turtle.color("blue")
      if 100>j>50:
         turtle.color("red")
      if 150>j>100:
         turtle.color("yellow")
      if 200>j>150:
         turtle.color("orange")
      if 250>j>200:
         turtle.color("green")
      if 300>j>250:
         turtle.color("gray")
      if 350>j>300:
         turtle.color("cyan")
      if 400>j>350:
         turtle.color("dim gray")
      if j==400: j=0
      j+=1
      turtle.goto(v[i]-(150,50))

def drawTriangle(points,color):
    turtle.fillcolor(color)
    turtle.up()
    turtle.goto(points[0][0],points[0][1])
    turtle.down()
    turtle.begin_fill()
    turtle.goto(points[1][0],points[1][1])
    turtle.goto(points[2][0],points[2][1])
    turtle.goto(points[0][0],points[0][1])
    turtle.end_fill()
def getMid(p1,p2):
    return ( (p1[0]+p2[0]) / 2, (p1[1] + p2[1]) / 2)
def run_serpin(points,degree):
   colormap = ['blue','red','green','white','yellow',
                'violet','orange']
   drawTriangle(points,colormap[degree])
   if degree > 0:
      run_serpin([points[0],
                        getMid(points[0], points[1]),
                        getMid(points[0], points[2])],
                        degree-1)
      run_serpin([points[1],
                        getMid(points[0], points[1]),
                        getMid(points[1], points[2])],
                        degree-1)
      run_serpin([points[2],
                        getMid(points[2], points[1]),
                        getMid(points[0], points[2])],
                        degree-1)#, myTurtle)   
   
def rand(triangle):
   turtle.reset(); turtle.ht()
   # turtle.pu(); turtle.goto(-100,-50); turtle.pd()
   for i in range(len(triangle)):
      turtle.pu(); turtle.goto(triangle[i]); turtle.pd()
      turtle.dot(3)


root = Tk()
root.withdraw()
root.title("Fractals")

frame1 = Frame(root)

c1 = Canvas(frame1, width=240, height=175)
im = ImageTk.PhotoImage(file="images.jpg")
c1.create_image(120, 73, image=im)
c1.pack(side=TOP)

typef = Pmw.ComboBox(frame1, label_text='Choose your Fractal:', labelpos='wn', listbox_width=15,
            dropdown=1, scrolledlist_items=fractals)
typef.pack(side=TOP, fill=BOTH, expand=0)
typef.selectitem(fractals[0])

stp = Pmw.ComboBox(frame1, label_text='Choose step:            ', labelpos='wn', listbox_width=10,
            dropdown=1, scrolledlist_items=step)
stp.pack(side=TOP, fill=BOTH, expand=0, pady=10)
stp.selectitem(step[0])

frame1.pack(side=LEFT, fill=BOTH, expand=0)

frame2 = Frame(root)

c2= Canvas(frame2, width=500, height=500, bg='white')
c2.pack(side=LEFT, fill=BOTH, expand=1)

turtle = tr.RawTurtle(c2)  # for turtle in windows

frame2.pack(side=LEFT, fill=BOTH, expand=1)

frame3 = Frame(frame1)

btn1 = Button(frame3, text='start')
btn1.bind('<Button-1>', start)
btn1.bind('<KeyPress-Return>', start)
btn1.pack(side=LEFT, padx=5, pady=5,ipadx=10, expand=1)

btn2 = Button(frame3, text='close')
btn2.bind('<Button-1>', close)
btn2.bind('<KeyPress-Return>', close)
btn2.pack(side=LEFT, padx=5, pady=5,ipadx=10, expand=1)

frame3.pack(side=BOTTOM, anchor=SE, fill=BOTH, expand=0)

root.deiconify()
root.mainloop()