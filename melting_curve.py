import numpy as np
import pymbar
import matplotlib
matplotlib.use("Agg") 
import matplotlib.pyplot as plt

if __name__ == "__main__":

    #### READ FILES, SET CONSTANTS, AND GET THINGS READY ####    

    # My boy boltzmann has a very special numberr
    kb = 0.0083145  # kJ/mol K

    # Collect list of temperatures from file
    temps = [ x.rstrip("\n") for x in open("short_temps", "r").readlines() ]
    
    # Turn list of temperatures into array of floats
    T = np.array(temps, float) 

    # Get energies from Etot.xvg files use these to create vector N_k
    energies = [ np.loadtxt("{}_0/Etot.xvg".format(x), usecols=[1]) for x in temps ]
    N_k = np.array([ len(x) for x in energies ])
    
    # Put energies in array named Etot 
    Etot = np.array(energies, float)
    
    # Read Q values for calculations later
    Q = [np.loadtxt("{}_0/Q.dat".format(x.rstrip("\n"))) for x in temps] 
    Q_kln = np.empty((len(T), Etot.shape[0], Etot.shape[1]), float)
    Q_kln[:] = np.array(Q, float)    

    # Beta for calculating reduced potentials
    B = 1/(kb*T) 

    # Initialize vector to hold reduced potentials
    u_kln = np.zeros((len(T), Etot.shape[0], Etot.shape[1]), float)    
    
    # Loop to fill in u_kln
    for i in range(len(T)):
        u_kln[i] = Etot*B[i]    

    # Initialize mbar
    mbar = pymbar.mbar.MBAR(u_kln, N_k)
    
    #### COMPUTE OBSERVABLES ####
    
    # For some reason we need to use unreduced potentials, aka Etot over and over
    E_kln = np.empty((len(T), Etot.shape[0], Etot.shape[1]), float)
    E_kln[:] = Etot
    
    # Calculate expectations for E
    (Eavg, dEavg) = mbar.computeExpectations(E_kln)


    # Calculate expectations for E^2
    (E2avg, dE2avg) = mbar.computeExpectations(E_kln**2)


    # Cv = (1/kb*T^2)*( <E^2> - <E>^2)
    Cv = kb*B**2*(E2avg - Eavg**2)   


    # <Q>
    (Qavg, dQavg) = mbar.computeExpectations(Q_kln)


    # <A> = A(T)
    # didn't do this one
   
    #### MAKE GRAPHS ####
    
    # Generate plot of Cv vs T
    plt.plot(T,Cv)
    plt.title('Cv vs T')
    plt.xlabel('T (K)')
    plt.ylabel('Cv')

    plt.savefig("Cv vs T")
    
    plt.clf()
 
    # Generate plot of Q vs T
    plt.plot(T,Qavg)
    plt.title('Q vs T')
    plt.xlabel('T (K)')
    plt.ylabel('Q')
    plt.savefig("Q vs T")

