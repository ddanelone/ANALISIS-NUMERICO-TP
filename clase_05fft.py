import numpy as np
import matplotlib.pylab as plt

def DFT_slow(x):
    x = np.asarray(x, dtype=float)
    N = x.shape[0]
    n = np.arange(N)
    k = n.reshape((N, 1))
    M = np.exp(-2j * np.pi * k * n / N)
    return np.dot(M, x)

def DFT2_slow(x):
     
    N1 = x.shape[0]
    N2 = x.shape[1]
    n = np.vstack([1.0*np.arange(N1)/N1**0.5,1.0*np.arange(N2)/N2**0.5])
    k = np.vstack([1.0*np.arange(N1)/N1**0.5,1.0*np.arange(N2)/N2**0.5])
    M=np.zeros((N1,N2,N1,N2),dtype=complex)
    for i in range(N1):
        for j in range(N2):
            for l in range(N1):
                for m in range(N2):
                    M[i,j,l,m]=np.exp((-2j*np.pi)*(n[0][i]*k[0][j]+n[1][l]*k[1][m]))
    
    
    
    return np.tensordot(M, x)

def IDFT_slow(x):
    
    N = x.real.shape[0]
    n = np.arange(N)
    k = n.reshape((N, 1))
    M = np.exp(2j * np.pi * k * n / N)
    return np.dot(M, x/N)
  
def FFT(x):

    x = np.asarray(x, dtype=float)
    N = x.shape[0]
    
    if N % 2 > 0:
        raise ValueError("la cantidad de elementos de x debe ser una potencia de 2")
    elif N <= 32: 
        return DFT_slow(x)
    else:
        X_even = FFT(x[::2])
        X_odd = FFT(x[1::2])
        factor = np.exp(-2j * np.pi * np.arange(N) / N)
        return np.concatenate([X_even + factor[:N//2] * X_odd,
                               X_even + factor[N//2:] * X_odd])  
  

def FFT_vectorized(x,N_min_opt):

    x = np.asarray(x, dtype=float)
    N = x.shape[0]

    if np.log2(N) % 1 > 0:
        raise ValueError("la cantidad de elementos de x debe ser una potencia de 2")

    N_min = min(N, N_min_opt)
    

    n = np.arange(N_min)
    k = n[:, None]
    M = np.exp(-2j * np.pi * n * k / N_min)
    X = np.dot(M, x.reshape((N_min, -1)))


    while X.shape[0] < N:
        X_even = X[:, :X.shape[1]//2]
        X_odd = X[:, X.shape[1]//2:]
        factor = np.exp(-1j * np.pi * np.arange(X.shape[0])
                        / X.shape[0])[:, None]
        X = np.vstack([X_even + factor * X_odd,
                       X_even - factor * X_odd])

    return X.ravel()  

def np_FFT(x):
  
  return np.fft.fft(x)
def np_IFFT(x):
  
  return np.fft.ifft(x)
