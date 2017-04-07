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
    global ezoldleft, ezoldright, abccoefleft, abccoefright
    ezoldleft = 0.0
    ezoldright = 0.0
    temp = sqrt(sigh[0]*chye[0])
    abccoefleft = (temp - 1.0)/(temp + 1.0)
    temp = sqrt(sigh[size - 1] * chye[size - 2])
    abccoefright = (temp - 1.0)/(temp + 1.0)
            
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
    global ezoldleft, ezoldright, abccoefleft, abccoefright
    ez[0] = ezoldleft + abccoefleft * (ez[1] -  ez[0])    # ABC's condition
    ezoldleft = ez[1]
    ez[size-1] = ezoldright + abccoefright * (ez[size-2] - ez[size - 1])     # ABC's condition
    ezoldright = ez[size - 2]
    
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