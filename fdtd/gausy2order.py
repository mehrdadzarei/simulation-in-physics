from numpy import array, exp, power, ma, sqrt
import matplotlib.pyplot as plt
import matplotlib.animation as animation

imp0 = 377.0                            # impedance of air
size = 200                              # length of space
loss_layer = 200                              # loss layer start from loss_layer
maxTime = 550                           # max time for simulation
loss = 0.02                             # loss of dielectric
epsr = 9.0                              # relative permitivity
cs = 1.0                                # Courant number
ez = array([0.0]*size)                  # electric field
eztm = array([[0.0]*size]*maxTime)      # electric field in time and space
hy = array([0.0]*(size-1))              # magnetic field
hytm = array([[0.0]*size]*maxTime)  # magnetic field in time and space
sige = array([0.0]*size)                # relative permitivity, function of position
sigh = array([0.0]*size)                # relative permitivity, function of position
chye = array([0.0]*(size-1))                # relative permitivity, function of position
chyh = array([0.0]*(size-1))                # relative permitivity, function of position
ezoldleft1 = array([0.0]*3)
ezoldleft2 = array([0.0]*3)
ezoldright1 = array([0.0]*3)
ezoldright2 = array([0.0]*3)
abccoefleft = array([0.0]*3)
abccoefright = array([0.0]*3)

def gridInit():
    for m in range(size):                   # initialize electric field coeficents
        if m < 100: 
            sige[m] = 1.0
            sigh[m] = imp0
        elif m < loss_layer: 
            sige[m] = 1.0
            sigh[m] = imp0/epsr
        else:
            sige[m] = (1.0-loss)/(1+loss)
            sigh[m] = imp0/9.0/(1+loss)

    for m in range(size-1):
        if m < loss_layer:
            chyh[m] = 1.0
            chye[m] = 1.0/imp0
        else:
            chye[m] = 1.0/imp0/(1.0+loss)
            chyh[m] = (1.0-loss)/(1.0+loss)

def abcInit():
    temp1 = sqrt(sigh[0]*chye[0])
    temp2 = 1.0/temp1 + 2.0 + temp1
    abccoefleft[0] = -(1.0 / temp1 - 2.0 + temp1) / temp2
    abccoefleft[1] = -2.0 * (temp1 - 1.0 / temp1) / temp2
    abccoefleft[2] = 4.0 * (temp1 + 1.0 / temp1) / temp2
    temp1 = sqrt(sigh[size - 1] * chye[size - 2])
    temp2 = 1.0/temp1 + 2.0 + temp1
    abccoefright[0] = -(1.0 / temp1 - 2.0 + temp1) / temp2
    abccoefright[1] = -2.0 * (temp1 - 1.0 / temp1) / temp2
    abccoefright[2] = 4.0 * (temp1 + 1.0 / temp1) / temp2
            
def updateH():
    for m in range(size-1):                             # step position
        hy[m] = chyh[m]*hy[m] + chye[m] * (ez[m+1]-ez[m])                   # update magnetic field
        hytm[qtime, m] = hy[m]

def ezInc(time, delay, location, width):
    if width <= 0: 
        print "your width of wave is wrong, enter another width (> 0): "
        exit()
    return exp(-power((time-delay-location/cs)/width,2))
        
def tfsfUpdate(time, delay, srcp, width):
    if srcp <= 0: 
        print "your source position is wrong, enter another position (> 0): "
        exit()
    hy[srcp] -= ezInc(time, delay, 0.0, width) * chye[srcp]     # TFSF boundary
    ez[srcp+1] += ezInc(time + 0.5, delay, -0.5, width)      # TFSF boundary
    
def abc():
    ez[0] = abccoefleft[0] * (ez[2] +  ezoldleft2[0]) +\
        abccoefleft[1] * (ezoldleft1[0] +  ezoldleft1[2] -\
        ez[1] - ezoldleft2[1]) +\
        abccoefleft[2] * ezoldleft1[1] - ezoldleft2[2]
    ez[size-1] = abccoefright[0] * (ez[size - 3] +  ezoldright2[0]) +\
        abccoefright[1] * (ezoldright1[0] +  ezoldright1[2] -\
        ez[size - 2] - ezoldright2[1]) +\
        abccoefright[2] * ezoldright1[1] - ezoldright2[2]
    for i in range(3):
        ezoldleft2[i] = ezoldleft1[i]
        ezoldleft1[i] = ez[i]
        
        ezoldright2[i] = ezoldright1[i]
        ezoldright1[i] = ez[size - 1 - i]
    
def updateE():
    for m in range(1,size-1):                             # step position
        ez[m] = ez[m]*sige[m] + sigh[m]*(hy[m]-hy[m-1])           # update electric field
        eztm[qtime, m] = ez[m]

def plot():
    fig, ax = plt.subplots()
    hyline, = ax.plot(hytm[0,:])
    ezline, = ax.plot(eztm[0,:])

    # Setting the axes properties
    # ax.set_xlim3d([0.0, 1.0])
    ax.set_xlabel('X')

    ax.set_ylim([-1.1, 1.1])
    ax.set_ylabel('Hy/Ez (V/m)')

    ax.set_title('Propegation fields')

    def animate(i):
        hyline.set_ydata(hytm[i,:])  # update the data
        ezline.set_ydata(eztm[i,:])  # update the data
        return hyline,ezline

    # Init only required for blitting to give a clean slate.
    def init():
        hyline.set_ydata(ma.array(range(size), mask=True))
        return hyline,

    ani = animation.FuncAnimation(fig, animate, range(maxTime), init_func=init,
                              interval=100, blit=True)

    plt.grid()
    plt.show()
        
if __name__ == '__main__':
    gridInit()
    abcInit()
    srcp = input("Enter the source position: ")         # source position
    delay = input("Enter the delay of wave: ")         # delay of wave
    width = input("Enter the width of wave: ")         # width of wave
    for qtime in range(maxTime):                            # step time    
        updateH()
        tfsfUpdate(qtime, delay, srcp, width)
        updateE()
        abc()
    plot()