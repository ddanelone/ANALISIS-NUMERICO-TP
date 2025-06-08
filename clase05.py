import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate
from scipy.interpolate import CubicSpline, PchipInterpolator, Akima1DInterpolator
from scipy import signal
from PIL import Image


#submuestreo


x=np.arange(-100,100,0.01)
senial100=np.sin(x*2*np.pi/5)+np.sin(x*2*np.pi/10)+np.sin(x*2*np.pi/20)

plt.plot(x,senial100)
plt.show()

size=senial100.shape[0]
signal_jw=np.fft.fft(senial100)
freq = np.fft.fftfreq(size, d=0.01)

plt.plot(freq, np.abs(signal_jw))
plt.show()

#muestreamos a 10 hz
x=np.arange(-100,100,0.1)
senial10=np.sin(x*2*np.pi/5)+np.sin(x*2*np.pi/10)+np.sin(x*2*np.pi/20)

#plt.plot(x,senial10)
#plt.show()

size=senial10.shape[0]
signal_jw=np.fft.fft(senial10)
freq = np.fft.fftfreq(size, d=.1)

plt.plot(freq, np.abs(signal_jw))
plt.show()

#muestreamos a 1 hz
x=np.arange(-100,100,1.)
senial1=np.sin(x*2*np.pi/5)+np.sin(x*2*np.pi/10)+np.sin(x*2*np.pi/20)

plt.plot(x,senial1)
plt.show()

size=senial1.shape[0]
signal_jw=np.fft.fft(senial1)
freq = np.fft.fftfreq(size, d=1)

plt.plot(freq, np.abs(signal_jw))
plt.show()

#muestreamos a 0.5 hz
x=np.arange(-100,100,2)
senial05=np.sin(x*2*np.pi/5)+np.sin(x*2*np.pi/10)+np.sin(x*2*np.pi/20)

plt.plot(x,senial05)
plt.show()

size=senial05.shape[0]
signal_jw=np.fft.fft(senial05)
freq = np.fft.fftfreq(size, d=2)

plt.plot(freq, np.abs(signal_jw))
plt.show()
plt.ion()


#interpolamos

plt.plot(x,senial05)#azul

x_new=np.arange(-100,100,0.01)
plt.plot(x_new,senial100)#naranja


signal_new=interpolate.PchipInterpolator(x, senial05)
y_new=signal_new(x_new)
plt.plot(x_new,y_new)#verde


signal_new=interpolate.CubicSpline(x, senial05)
y_new05=signal_new(x_new)
plt.plot(x_new,y_new05)#roja

#muestreamos a 0.333 hz
x=np.arange(-100,100,3)
senial03=np.sin(x*2*np.pi/5)+np.sin(x*2*np.pi/10)+np.sin(x*2*np.pi/20)

plt.plot(x,senial03)
plt.show()

size=senial03.shape[0]
signal_jw=np.fft.fft(senial03)
freq = np.fft.fftfreq(size, d=3)

plt.plot(freq, np.abs(signal_jw))


signal_new=interpolate.CubicSpline(x, senial03)
y_new=signal_new(x_new)
plt.plot(x_new,y_new)#azul
plt.plot(x_new,senial100)#naranja
plt.plot(x_new,y_new05)#verde

#########################################################3

#deconvolución1D
caa=np.fromfile('ca_amper.txt',sep=' ')
min_a=caa[:200].argmin()
max_a=caa[:200].argmax()

smp=abs(max_a-min_a)

delta_t=0.01/smp

size=caa.shape[0]
t_fin=delta_t*size
t=np.arange(0,t_fin,delta_t)

plt.plot(t,caa)

t_new=np.arange(0,5*t_fin,delta_t)

deltas=np.zeros_like(t_new)
deltas[0]=1
for i in range(4):
    deltas[abs(t_fin*(i+1)-t_new)<0.6*delta_t]=1

deltas.nonzero()

multi=signal.fftconvolve(caa,deltas)[:t_new.shape[0]]
plt.plot(t_new,multi)
plt.show()



#deconvolucionemos con el deconvolve

caa_rec=signal.deconvolve(multi, deltas)


#deconvolucionemos con fft

#IFdelta=np.fft.fft(deltas)
#IFdelta[np.abs(IFdelta)<1e-10]=1e10
#RIFdelta=1./IFdelta
#caa_rec=np.fft.ifft(np.multiply(np.fft.fft(multi),RIFdelta))


#si estoy seguro de no dividir por cero:
caa_rec=np.fft.ifft(np.divide(np.fft.fft(multi),np.fft.fft(deltas)))


#deconvolución 2d

imagen= np.asarray(Image.open('p2.png').convert('RGB'))


imager=np.asarray(imagen[:,:,0],dtype='float64')
imageg=np.asarray(imagen[:,:,1],dtype='float64')
imageb=np.asarray(imagen[:,:,2],dtype='float64')

plt.imshow(imageb,cmap='gray')


deltas=np.zeros_like(imageb)
ancho, alto=imager.shape

deltas[ancho//2,alto//2]=1
deltas[ancho//4,alto//4]=1
deltas[ancho//4,3*alto//4]=1
deltas[3*ancho//4,alto//4]=1
deltas[3*ancho//4,3*alto//4]=1
deltas.nonzero()
plt.imshow(deltas)

#convolucionamos con fft para que no salga tan caro

multi=np.fft.ifft2(np.multiply(np.fft.fft2(imageb),np.fft.fft2(deltas)))
plt.imshow(np.abs(multi),cmap='gray')


#deconvolucionamos

IFdelta=np.fft.fft2(deltas)
IFdelta[np.abs(IFdelta)<1e-10]=1e10
RIFdelta=1./IFdelta

im_rec=np.fft.ifft2(np.multiply(np.fft.fft2(multi),RIFdelta))


#no anda en 2D
#im_rec=signal.deconvolve(multi, deltas)

im_rec/=im_rec.max()/imageb.max()
plt.imshow(im_rec.astype(np.uint8),cmap='gray')


#https://stackoverflow.com/questions/17473917/is-there-a-equivalent-of-scipy-signal-deconvolve-for-2d-arrays
