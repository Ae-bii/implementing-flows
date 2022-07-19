import math
import numpy as np

e = math.e
pi = math.pi

class Potentialf:
    def bump_f(z, center):
        value = 0
        r = abs(z - center)
        alpha = 0.5  # Consistent with the density 
        if r < 1/alpha:
            value = math.pow(e, -(1/(1-(alpha*r)**2)))
        return value
    
    def giulio_f(z, center):
        r = abs(z - center)
        alpha = 1.5  # Consistent with the density 
        return r * math.erf(r/alpha) + (alpha/math.sqrt(pi)) * math.pow(e, -(r/alpha) ** 2)
    
    def gaussian_f(z, z_center):
        r = abs(z - z_center)
        alpha = 1
        return math.pow(e, -((alpha*r)**2))
    
    def multiquadric_f(z, z_center):
        r = abs(z - z_center)
        alpha = 1
        return math.sqrt(1+(alpha*r)**2)
    
    def inverseQuadratic_f(z, z_center):
        r = abs(z - z_center)
        alpha = 1
        return 1/(1+(alpha*r)**2)
    
    def inverseMultiquadric_f(z, z_center):
        r = abs(z - z_center)
        alpha = 1
        return 1/math.sqrt(1+(alpha*r)**2)
    
    def polyharmonicSpline_f(z, z_center, k):
        r = abs(z - z_center)
        if k%2 == 0:
            return r**(k-1)*np.log(r**r) 
        else:
            return r**k
    
    def thinPlateSpline_f(z, z_center):
        r = abs(z - z_center)
        return r**2*np.log(r)
    
    