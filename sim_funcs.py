import numpy as np
import math
from consts import *

def fibonacci_sphere(samples=1000):
    points = []
    phi = np.pi * (np.sqrt(5.) - 1.)
    for i in range(samples):
        y = 1 - (i / float(samples - 1)) * 2
        radius = np.sqrt(1 - y * y)
        theta = phi * i
        x = np.cos(theta) * radius
        z = np.sin(theta) * radius
        points.append((x, y, z))
    pts = np.array(points).T*R_OBJECT
    return pts[0], pts[1], pts[2]

def log_min_mass(rho, r_p):
    min_mass = (4/3)*np.pi*rho*(r_p)**3
    return np.log10(min_mass)

def conv_sph_to_cart(r,phi, theta):
    x = r*np.sin(phi)*np.cos(theta)
    y = r*np.sin(phi)*np.sin(theta)
    z = r*np.cos(phi)
    return x,y,z

def conv_cart_to_sph(x,y,z):
    r = np.sqrt(x**2 + y**2 + z**2)
    theta = []
    for x0, y0 in zip(x,y):
        theta.append(math.atan2(y0,x0))
    theta = np.degrees(theta)
    filt = np.where((theta<0))
    theta[filt] = 360 - np.abs(theta[filt])
    phi = np.degrees(np.arccos(z/r))
    return r,np.radians(phi),np.radians(theta)

def conv_lunar_to_ecliptic(x,y,z,vx,vy,vz):
    x_rot = x
    y_rot = y * np.cos(OBLIQ) - z * np.sin(OBLIQ)
    z_rot = y * np.sin(OBLIQ) + z * np.cos(OBLIQ)
    vx_rot = vx
    vy_rot = vy * np.cos(OBLIQ)
    vz_rot = vy * np.sin(OBLIQ)
    return x_rot, y_rot, z_rot, vx_rot, vy_rot, vz_rot


def init_grid():
    x,y,z = fibonacci_sphere(samples=N)
    r,phis,thetas = conv_cart_to_sph(x,y,z)
    return phis,thetas


def grun(m):
    c4,c5,c6,c7,c8,c9,c10 = 2.2e3, 15, 1.3e-9, 1e11, 1e27, 1.3e-16, 1e6
    y4,y5,y6,y7,y8,y9,y10=0.306,-4.38,2,4,-0.36, 2,-0.85
    a = np.power((c4*np.power(m,y4) + c5),y5)
    b = c6*np.power(m+c7*np.power(m,y6) + c8*np.power(m, y7),y8)
    c = c9*np.power(m + c10*np.power(m, y9),y10)
    return (a+b+c)*SEC_PER_YEAR
