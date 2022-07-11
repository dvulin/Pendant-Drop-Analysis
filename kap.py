# hej hej hej
import cv2
import numpy as np
from matplotlib import pyplot as plt
# ovo je moja izmjena
#smajla
#jope

kap = cv2.imread(r'C:\Users\karlo\Desktop\kap.png') #ucitavanje slike kapi
kruznica_kap = kap.copy()
kap_bw = cv2.threshold(kap, 128, 255, cv2.THRESH_BINARY)[1] #pretvaranje u crno bijelu sliku
#moja izmjena
####
gray_kap = cv2.cvtColor(kruznica_kap, cv2.COLOR_BGR2GRAY) 
contura_kap = cv2.Canny(gray_kap, 100, 255)
smooth_gray = cv2.GaussianBlur(contura_kap, (3, 3), 2, 2)
circles = cv2.HoughCircles(smooth_gray, cv2.HOUGH_GRADIENT, 1, 20,
              param1 = 60,
              param2 = 35,
              minRadius = 0,
              maxRadius = 0)
circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    cv2.circle(kruznica_kap,(i[0],i[1]),i[2],(125,125,0),1)
    cv2.circle(kruznica_kap,(i[0],i[1]),2,(0,125,125),1)
print('srediste, radijus kruga', circles)
print('radijus', circles[0][0][2])
radijusKruznice_R = circles[0][0][2]
#### pretvaranje slike kapi u grayscale, nalazenje konture kapi kako bi mogli koristiti funkciju HoughCircles
#### iscrtavanje nama zanimljive kruznice

height, width = kap_bw.shape[:2]

crna_sirina = 0
max_sirina = 0
sirina=0
max_red = 0

for i in range(height):
    for j in range(width):
        if kap_bw[i][j][0] == 0:
            crna_sirina += 1
        elif (i == 0) & (j == width-1):
            sirina_igle = crna_sirina ##odredjivanje sirine igle u prvom redu
            crna_sirina = 0 
        elif (j == width-1) & (crna_sirina >= max_sirina):
            max_sirina = crna_sirina ##maksimalna sirina kapi
            crna_sirina = 0 
        elif (j == width-1) & (crna_sirina > 0):
            zadnjiCrni_red = i #odredjivanje reda pojave zadnjeg crnog piksela
            crna_sirina = 0 

redPromjera_Ds = zadnjiCrni_red - max_sirina #odredjivanje reda promjera Ds
pxPromjer_Ds = 0

for j in range(width):
    if kap_bw[redPromjera_Ds][j][0] == 0:
        pxPromjer_Ds += 1

mjerilo = 0.0005/sirina_igle 				#pretpostavka da je sirina igle 0.5 milimetara , [mm/px]
promjer_De = max_sirina*mjerilo
promjer_Ds = pxPromjer_Ds*mjerilo
g = 9.80665
gustocaKap = 800 							#pretpostavljena gustoca 800kg/m^3

medjuPovrsinska_napetost = g*gustocaKap*promjer_De**2*(promjer_Ds/promjer_De)

print('height', height)
print('width', width)
print('sirina_igle', sirina_igle)
print('max_sirina, pxPromjer_De', max_sirina)
print('zadnjiCrni_red', zadnjiCrni_red)
print('mjerilo', mjerilo)
print('promjer_De', promjer_De)
print('promjer_Ds', promjer_Ds)
print('medjuPovrsinska_napetost', medjuPovrsinska_napetost)

plt.imshow(kap_bw, interpolation = 'bicubic')
plt.show() #crno bijela slika kapi s koordinatnim sustavom, za provjeru

cv2.imshow('slika', kap_bw)
cv2.imshow('pocetna_kap', kap)
#cv2.imshow('kontura', contura_kap)
#cv2.imshow('smooth', smooth_gray)
#cv2.imshow('kruznica_kap', kruznica_kap)

##cv2.imwrite('kruznica_kap.png', kap) 

cv2.waitKey(0)
cv2.destroyAllWindows()