import numpy as np
import random

def koch(stp):
   def f1(x0, x2, x3):     # first line 
      x1 = (x2-x3)*1/3+x0
      return x1

   def f2(x1, x3, x0):     # second line 
      x2 = [[0.5,-0.866],[0.866,0.5]]*(x3-x0).T*1/3+(x1).T
      # print x2
      return x2

   def f3(x2,x4, x0):      # third line 
      x3 = [[0.5,0.866],[-0.866,0.5]]*(x4-x0).T*1/3+(x2).T
      return x3
   
   def f4(x3,x4, x0):         # forth line 
      x4 = (x4-x0)*1/3+x3
      return x4

   if stp%2:  # for odd step
      l1, l2, p1, p2 = 2, 1, 1, 0
   else:      # for even step
      l1, l2, p1, p2 = 1, 2, 0, 1
   inf = {'0': (2,1), '1': (5, 4), '2': (17, 16), '3': (65, 64),
      '4':(257,256),'5':(1025,1024), '6': (4097,4096),'7':(16385,16384),'8': (589824,589823)}
   coords1 = np.matrix([[300.0,0.0]]*inf[`stp-p2`][0])
   coords2 = np.matrix([[300.0,0.0]]*inf[`stp-p1`][0])
   coords1[0] = [0.0,0.0]
   coords2[0] = [0.0,0.0]
   f = 3
   s = 4
   
   for step in range(stp):
    
      if f==step+3:
         cnt = 0      # for more points
         cnt1 = 0
         f += 2
         for i in range(inf[`stp-l2`][1]):
            coords1[cnt+1] = f1(coords1[cnt+0], coords2[cnt1+1], coords1[cnt])   # second point of line
            coords1[cnt+2] = f2(coords1[cnt+1], coords2[cnt1+1], coords1[cnt]).T     # .T is for make same shape  third point
            coords1[cnt+3] = f3(coords1[cnt+2], coords2[cnt1+1], coords1[cnt]).T    # forth point of line
            coords1[cnt+4] = f4(coords1[cnt+3], coords2[cnt1+1], coords1[cnt])       # last point
            cnt+=4
            cnt1+=1
      elif s==step+3:
         cnt = 0      # for more points
         cnt1 = 0
         s += 2
         for i in range(inf[`stp-l1`][1]):
            coords2[cnt+1] = f1(coords2[cnt+0], coords1[cnt1+1], coords2[cnt])   # second point of line
            coords2[cnt+2] = f2(coords2[cnt+1], coords1[cnt1+1], coords2[cnt]).T     # .T is for make same shape  third point
            coords2[cnt+3] = f3(coords2[cnt+2], coords1[cnt1+1], coords2[cnt]).T    # forth point of line
            coords2[cnt+4] = f4(coords2[cnt+3], coords1[cnt1+1], coords2[cnt])       # last point
            cnt+=4
            cnt1+=1
      else: pass
   if stp%2:      # for odd step
      return np.array(coords1)
   else:          # for even step
      return np.array(coords2)

def dragon(stp):
   def f1(x3, x0, t):     # first line 
      x2 = [[np.cos(t),-np.sin(t)],[np.sin(t),np.cos(t)]]*(x3-x0).T*1/np.sqrt(2) + x0.T
      # print x2
      return x2

   def f2(x2, x4, x0, t):      # second line 
      x3 = [[np.cos(t),np.sin(t)],[-np.sin(t),np.cos(t)]]*(x4-x0).T*1/np.sqrt(2)+(x2).T
      return x3

   if stp%2:  # for odd step
      l1, l2, p1, p2 = 2, 1, 1, 0
   else:      # for even step
      l1, l2, p1, p2 = 1, 2, 0, 1
   inf = {'0':1, '1':2, '2':4, '3':8,'4':16,'5':32, '6':64,'7':128,'8':256, '9':512,'10':1024,
         '11':2048,'12':4096,'13':8192,'14':16384,'15':32768,'16':65536}
   coords1 = np.matrix([[300.0,0.0]]*(inf[`stp-p2`]+1))
   coords2 = np.matrix([[300.0,0.0]]*(inf[`stp-p1`]+1))
   coords1[0] = [0.0,0.0]
   coords2[0] = [0.0,0.0]
   f = 3
   s = 4
   
   for step in range(stp):
    
      if f==step+3:
         cnt = 0      # for more points
         cnt1 = 0
         f += 2
         t = np.pi/4     # the angle should change it's sign
         for i in range(inf[`stp-l2`]):
            coords1[cnt+1] = f1(coords2[cnt1+1], coords1[cnt], t).T   # second point of line
            coords1[cnt+2] = f2(coords1[cnt+1], coords2[cnt1+1], coords1[cnt], t).T     # .T is for make same shape  third point
            cnt+=2
            cnt1+=1
            t *=-1
      elif s==step+3:
         cnt = 0      # for more points
         cnt1 = 0
         s += 2
         t = np.pi/4
         for i in range(inf[`stp-l1`]):
            coords2[cnt+1] = f1(coords1[cnt1+1], coords2[cnt], t).T   # second point of line
            coords2[cnt+2] = f2(coords2[cnt+1], coords1[cnt1+1], coords2[cnt], t).T     # .T is for make same shape  third point
            cnt+=2
            cnt1+=1
            t *=-1
      else: pass
   if stp%2:      # for odd step
      return np.array(coords1)
   else:          # for even step
      return np.array(coords2)

def kochrand(stp):
   
   def f1(x0, x):     # first line 
      x1 = (x-x0)*1/3+x0
      return x1

   def f2(x0, x, x1):     # second line 
      x2 = [[0.5,-0.866],[0.866,0.5]]*(x-x0).T*1/3+(x0).T+(x1*1/3).T
      # print x2
      return x2

   def f3(x0,x, x1):      # third line 
      x3 = [[0.5,0.866],[-0.866,0.5]]*(x-x0).T*1/3+(x0).T+((x1+[0,100])*1/2).T
      return x3
   
   def f4(x0,x, x1):         # forth line 
      x4 = (x-x0)*1/3+x0+(x1*2/3)
      return x4

   coords = np.matrix([[-100.0,0.0],[200.0,0.0]])
   points = np.matrix([[0.0,0.0]]*1000)
   
   for i in range(1000):
      r = np.matrix([[random.uniform(-100,200),0]])
      c = random.choice([1,2,3,4])
      points[i] = f1(coords[0], r)
      for j in range(stp):     
         c = random.choice([1,2,3,4])
         if c==1:
            points[i] = f1(coords[0], points[i])
         elif c==2:
            points[i] = f2(coords[0], points[i], coords[1]).T
         elif c==3:
            points[i] = f3(coords[0], points[i], coords[1]).T
         elif c==4:
            points[i] = f4(coords[0], points[i], coords[1])
      
      
   return np.array(points)      

def serpin(stp):
   
   def f1(x, x0):
      return (x-x0)*1/2+(x0+x0*1/2)
      
   def f2(x, x0, x1):
      return (x-x0)*1/2+(x0+x1*1/2)
   
   def f3(x, x0, x2):
      return (x-x0)*1/2+(x2*1/2+x0)
   
   coords = np.matrix([[-50.0,0.0],[50.0,150.0],[150.0,0.0]])
   points = np.matrix([[0.0,0.0]]*1000)
   
   for i in range(1000):
      r = np.matrix([[random.random(),random.random()]])
      c = random.choice([1,2,3])
      points[i] = f1(r,coords[0])
      for j in range(stp):     
         c = random.choice([1,2,3])
         if c==1:
            points[i] = f1(points[i],coords[0])
         elif c==2:
            points[i] = f2(points[i],coords[0], coords[1])
         elif c==3:
            points[i] = f3(points[i],coords[0], coords[2])
      
   return np.array(points)
   
def sarakhs(stp):
   
   def f1(x, x2):
      return [[np.cos(np.pi/8),-np.sin(np.pi/8)],[np.sin(np.pi/8),np.cos(np.pi/8)]]*(x2-x).T*5/6+(x2).T
      
   def f2(x, x2):
      return [[np.cos(np.pi/4),-np.sin(-np.pi/4)],[np.sin(-np.pi/4),np.cos(np.pi/4)]]*(x2-x).T*1/6+(x2).T*1/8
   
   def f3(x, x2):
      return [[np.cos(np.pi/4),-np.sin(np.pi/4)],[np.sin(np.pi/4),np.cos(np.pi/4)]]*(x2-x).T*5/6+(x2).T*7/8
   
   coords = np.matrix([[-50.0,-50.0],[-50.0,50.0],[50.0,50.0],[50.0,-50.0]])
   points = np.matrix([[0.0,0.0]]*200)
   
   for i in range(200):
      r = np.matrix([[random.random(),random.random()]])
      c = random.choice([1,2,3])
      points[i] = f1(r,coords[2]).T
      for j in range(stp):     
         c = random.choice([1,2,3])
         if c==1:
            points[i] = f1(points[i],coords[2]).T
         elif c==2:
            points[i] = f2(points[i],coords[2]).T
         elif c==3:
            points[i] = f3(points[i],coords[2]).T
      
   return np.array(points)   
