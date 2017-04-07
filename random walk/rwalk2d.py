from numpy import random, exp, sqrt, pi, arange, array
import matplotlib.pyplot as plt
from Tkinter import *
import turtle

def start(e):
   for i in range(l+1-100):
     if i<=20: turtle.color(colormap[0])
     elif i<=40: turtle.color(colormap[1])
     elif i<=60: turtle.color(colormap[2])
     elif i<=80: turtle.color(colormap[3])
     elif i<=100: turtle.color(colormap[4])
     for j in range(l+1):
          turtle.pu();turtle.goto(2*j-2*l/2,2*i-2*l/2);turtle.pd()
          if y[l-i-100,l-j]==1:
               turtle.dot(3)


p =.25# input("Enter right walk probability: ")
# t = int(input("Enter walk time(second): "))
l =200# int(input("Enter walk lenght(steps number): "))
x = array([[0]*(l+1)]*(l+1-100))    #position
y = array([[0]*(l+1)]*(l+1-100))
y[l-100,:]=1

for n in range(100000):
     j = 5       #initial position of particle
     k = random.randint(0,201)
     x[j,k] = 1     #initial position should be 1 another ones 0
     for i in range(100000):
          r = random.random()
          if r<p:
              x[j,k]=0
              j+=1
              if y[j,k]==1:
                   y[j-1,k]=1
                   break
              x[j,k]=1
          elif 2*p>r>=p:
              x[j,k]=0
              j-=1
              if j<0: break
              if y[j,k]==1:
                   y[j-1,k]=1
                   break
              x[j,k]=1
          elif 2*p<=r<3*p:
              x[j,k]=0
              k+=1
              if k>l: break
              if y[j,k]==1:
                   y[j,k-1]=1
                   break
              x[j,k]=1
          elif 4*p>=r>3*p:
              x[j,k]=0
              k-=1
              if k<0: break
              if y[j,k]==1:
                   y[j,k+1]=1
                   break
              x[j,k]=1


root = Tk()
root.withdraw()
colormap = ['blue','red','green','black','yellow']
c = Canvas(root, width=700, height=700, bg="white")
c.pack(side=TOP, fill=BOTH, expand=1)
turtle = turtle.RawTurtle(c)
turtle.ht()
# turtle.color(colormap[2])
turtle.speed(1)
btn1 = Button(root, text='start')
btn1.bind('<Button-1>', start)
btn1.bind('<KeyPress-Return>', start)
btn1.pack(side=TOP)
root.deiconify()
root.mainloop()