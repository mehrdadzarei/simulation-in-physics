from numpy import array, exp, ma
import matplotlib.pyplot as plt
import matplotlib.animation as animation

imp0 = 377.0                            # impedance of air
size = 200                              # length of space
loss_layer = 180                              # loss layer start from loss_layer
maxTime = 450                           # max time for simulation
loss = 0.01                             # loss of dielectric
ez = array([0.0]*size)                  # electric field
eztm = array([[0.0]*size]*maxTime)      # electric field in time and space
hy = array([0.0]*(size-1))              # magnetic field
hytm = array([[0.0]*size]*maxTime)  # magnetic field in time and space
sige = array([0.0]*size)                # relative permitivity, function of position
sigh = array([0.0]*size)                # relative permitivity, function of position
chye = array([0.0]*(size-1))                # relative permitivity, function of position
chyh = array([0.0]*(size-1))                # relative permitivity, function of position

for m in range(size):                   # initialize electric field coeficents
    if m < 100: 
        sige[m] = 1.0
        sigh[m] = imp0
    elif m < loss_layer: 
        sige[m] = 1.0
        sigh[m] = imp0/9.0
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
        
for qtime in range(maxTime):                            # step time
    # hy[size-1] = hy[size-2]                             # ABC's condition
    for m in range(size-1):                             # step position
        hy[m] = chyh[m]*hy[m] + chye[m] * (ez[m+1]-ez[m])                   # update magnetic field
        hytm[qtime, m] = hy[m]
    hy[49] -= exp(-(qtime-30)*(qtime-30)/100)/imp0      # TFSF boundary
    ez[0] = ez[1]                                       # ABC's condition
    # ez[size-1] = ez[size-2]                             # ABC's condition
    for m in range(1,size-1):                             # step position
        ez[m] = ez[m]*sige[m] + sigh[m]*(hy[m]-hy[m-1])           # update electric field
        eztm[qtime, m] = ez[m]
    ez[50] += exp(-(qtime-29)*(qtime-29)/100)           # source of electric field

if __name__ == '__main__':
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