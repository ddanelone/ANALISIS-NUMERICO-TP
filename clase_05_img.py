import matplotlib as ml
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from scipy import signal
from sympy import *

image = np.asarray(Image.open('image.jpg').convert('RGB'))
plt.imshow(image, interpolation="none") 
plt.show() 

#descompongo en 3 canales
imager=image[:,:,0]
imageg=image[:,:,1]
imageb=image[:,:,2]

fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(20, 15))
ax[0,0].imshow(image, interpolation="none")
ax[0,0].set_title('Imagen Original')
ax[0,1].imshow(imager, cmap='gray', vmin=0, vmax=255)
ax[0,1].set_title('Canal rojo')
ax[1,0].imshow(imageg, cmap='gray', vmin=0, vmax=255)
ax[1,0].set_title('Canal verde')
ax[1,1].imshow(imageb, cmap='gray', vmin=0, vmax=255)
ax[1,1].set_title('Canal azul')
plt.show()

freqr = abs(np.fft.fft2(imager))
freqg = abs(np.fft.fft2(imageg))
freqb = abs(np.fft.fft2(imageb))

#freqr-=np.min(freqr.flatten())
#freqr*=(255/np.max(freqr.flatten())) 
#freqr=np.floor(freqr) 

#freqg-=np.min(freqg.flatten())
#freqg*=(255/np.max(freqg.flatten())) 
#freqg=np.floor(freqg) 

#freqb-=np.min(freqb.flatten())
#freqb*=(255/np.max(freqb.flatten())) 
#freqb=np.floor(freqb) 

fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(20, 15))
ax[0,0].imshow(image, interpolation="none")
ax[0,0].set_title('Imagen Original')
ax[0,1].imshow(freqr, cmap='gray')
ax[0,1].set_title('Canal rojo')
ax[1,0].imshow(abs(freqg), cmap='gray')
ax[1,0].set_title('Canal verde')
ax[1,1].imshow(np.log(abs(freqb)), cmap='gray')
ax[1,1].set_title('Canal azul')
plt.show()

#Desplazamiento

shape=freqr.shape
gridr=np.zeros(shape)
xmax=1.0*shape[0]#81
ymax=1.0*shape[1]#346



delta_desp=np.zeros_like(imager)
delta_desp[int(2*xmax/3),int(ymax/4)]=1

#imager_desp=signal.convolve2d(imager,delta_desp,'full')
imager_desp=signal.fftconvolve(imager,delta_desp,'full') #para comparar tiempos
#imager_desp=abs(np.fft.ifft2(np.fft.fft2(imager)*np.fft.fft2(delta_desp)))
#ojo con los tamanios
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(20, 15))
ax[0].imshow(imager, cmap='gray', vmin=0, vmax=255)
ax[0].set_title('Imagen Original')
ax[1].imshow(imager_desp, cmap='gray', vmin=0, vmax=255)
ax[1].set_title('Canal rojo desplazado')
plt.show()

#suavizado

kernel_9=np.ones((3,3))/9
imager_k9=signal.fftconvolve(imager,kernel_9,'same')

kernel_9a=np.ones((3,3))/8
kernel_9a[1,1]=0
imager_k9a=signal.fftconvolve(imager,kernel_9a,'same')

kernel_25=np.ones((5,5))/25
imager_k25=signal.fftconvolve(imager,kernel_25,'same')


fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(20, 15))
ax[0,0].imshow(imager, cmap='gray', vmin=0, vmax=255)
ax[0,0].set_title('Imagen Original')
ax[0,1].imshow(imager_k9, cmap='gray', vmin=0, vmax=255)
ax[0,1].set_title('Canal rojo suavizado k9')
ax[1,0].imshow(imager_k9a, cmap='gray', vmin=0, vmax=255)
ax[1,0].set_title('Canal rojo suavizado k9*')
ax[1,1].imshow(imager_k25, cmap='gray', vmin=0, vmax=255)
ax[1,1].set_title('Canal rojo suavizado k25')
plt.show()


