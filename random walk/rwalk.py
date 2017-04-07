from numpy import random, exp, sqrt, pi, arange
import matplotlib.pyplot as plt

p =.5# input("Enter right walk probability: ")
# t = int(input("Enter walk time(second): "))
l =20# int(input("Enter walk lenght(steps number): "))
x = [0]*(l+1)    #position
# j = 10       #initial position
x[19] = 1     #initial position sould be 1 another 0
life = 0
for t in range(1000):
 j=19
 for i in range(500):
   r = random.random()
   if r<p:
      x[j]=0
      j+=1
      x[j]=1
   else:
      x[j]=0
      j-=1
      x[j]=1
   if j==0: 
      life += i
      break
   if j==20: 
      life += i
      break
print life/1000
# avrx = (2*p-1)*t
# sigma2 = 4*p*(1-p)*t
# k = arange(0,100,1)
# prob = 1/sqrt(2*pi*sigma2)*exp(-(k-avrx-50)**2/(2*sigma2))
# fig, ax = plt.subplots()
# ax.plot(k,prob)
# ax.grid()
# print j,"\t",avrx,"\t",sqrt(sigma2)
# plt.show()