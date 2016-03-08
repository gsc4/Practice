import numpy as np
import pymbar 


if __name__ == "__main__":
    kb = 0.0083145  # kJ/mol K

    temps = [ x.rstrip("\n") for x in open("short_temps", "r").readlines() ]
    
    T = [ float(x) for x in temps ] 
    
    num_interpolations = 0

    # I made usecols be a list because it was mad when I was just supplying an int
    energies = [ np.loadtxt("{}_0/Etot.xvg".format(x), usecols=[1]) for x in temps ]
    N_k = [ len(x) for x in energies ]
    Etot = np.concatenate(energies) 

    u_kn = np.zeros((len(T), len(Etot)), float)

    #for loop to fill in u_kn
    for i in range(len(T)):
        B = 1/(kb*T[i])
        u_kn[i] = Etot*B

    print len(T)
    print len(Etot)
    print u_kn.shape
    print len(N_k) 

    mbar = pymbar.MBAR(u_kn, N_k)
    print mbar
    # compute observables

    # Cv = (1/kb*T^2)*( <E^2> - <E>^2)
    

    # <Q>

    # <A> = A(T)
