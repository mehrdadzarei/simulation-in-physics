from Tkinter import *
import turtle
from random import randint
from numpy import sum, array, log10, sqrt 
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def start(event):
   
   run()

def run():
  f = open("D:\\programming\\physics\\tfd\\w(t).txt", "w")
  k=1
  for t in range(5):
   turtle.color(colormap[t])
   for i in range(500):
      x = randint(0,99) 
      h[x]+=1
      h2[x] = h[x]**2
      aver1 = sum(h2)/100.0
      aver2 = (sum(h)/100.0)**2
      wt = sqrt(aver1 - aver2)
      f.write(`k`+"\t"+"%0.5s"%`wt`+"\n")
      k+=1
      # turtle.pu(); turtle.goto(3*x-150,3*h[x]); turtle.pd()
      # turtle.dot(5)
  f.close()
  plot()

def plot():
   with open("D:\\programming\\physics\\tfd\\w(t).txt", "r") as f:
      data = f.read()
   f.close
   data = data.split('\n')
   data.pop(-1)      #this is for delete last empty line, or use del
   t = [row.split('\t')[0] for row in data]
   h = [row.split('\t')[1] for row in data]
   t = array(t, dtype = float)
   h = array(h, dtype = float)
   popt, pcov = curve_fit(fun, t, h)
   print "c = %s, b = %s" %(popt[0], popt[1])
   fig, ax1 = plt.subplots()
   # ax1 = fig.add_subplot(111)
   ax1.plot(log10(t), log10(h), c='r', label="data")
   # plt.hold(True)
   ax1.plot(log10(t), log10(fun(t, popt[0], popt[1])), c='b', label="fit curve")
   ax1.legend(loc=2)
   ax1.set_xlabel('t')
   ax1.set_ylabel('W')
   plt.show()

def fun(t, c, b):
   w = c*t**b
   return w

h = [0]*200
h2 = [0]*200

root = Tk()
root.withdraw()
colormap = ['blue','red','green','black','yellow']
c = Canvas(root, width=400, height=500, bg="white")
c.pack(side=TOP, fill=BOTH, expand=1)
turtle = turtle.RawTurtle(c)
turtle.ht()
btn1 = Button(root, text='start')
btn1.bind('<Button-1>', start)
btn1.bind('<KeyPress-Return>', start)
btn1.pack(side=TOP)
root.deiconify()
root.mainloop()