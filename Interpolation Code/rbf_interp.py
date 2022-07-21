"""
@author: JG 
"rbf_interp.py"
Module intended to replace our current use of Scipy's interp2d member 
Utilizes the 'radial basis function' interpolant to derive a smooth image from a set of scattered points in any dimension. 
Based heavily on Numerical Recipes sect. 3.7

Caveats: 
This is computationally expensive as solving linear systems of n equations takes O(n^3)
Image can still be negative as weighting vector w can hold large negative values

Acknowledgements: 
Scipy.interpolate source code 
 * https://github.com/scipy/scipy/blob/main/scipy/interpolate/
Numerical Recipies section 3.7
"""

import numpy as np

class RBF_interp: 
    # Object for RBF interpolation
    # call constructor once then call interp method for each desired point
    
    def __init__(self, pts, vals, func = "multiquadric", scale = 1, norm = False): 
        # Constructor:
        # Initializes RBF values and w vector for known points 
        # @pts:     n x dim matrix for the data points
        # @vals:    length-n vector of known function values 
        # @func:    chosen radial basis function 
        # @scale:   smoothing factor within a given RBF
        #           function becomes increasingly flat as scale -> 0
        #           generally: avg pt separation < scale < "outer scale"
        # @norm:    bool of whether normalized RBF interp is requested 

        self.pts = pts
        self.dim = int(np.shape(pts)[1]) # number of columns 
        self.n = int(np.shape(pts)[0]) # number of rows 
        self.vals = vals
        self.fn = func
        self.scale = scale
        self.norm = norm
        
        # Now to populate the RBF matrix and "r.h.s." vector 
        # the r.h.s. vector is just known output vals in non-normalized case
        i = 0 
        j = 0
        rbf_mat = np.zeros((self.n, self.n)) 
        rhs = np.zeros(self.n) 
        for i in range(self.n): 
            sum_rbf = 0 
            for j in range(self.n): 
                rbf_mat[i][j] = self.rbf_fn(self.rad(self.pts[i], self.pts[j]))
                sum_rbf += rbf_mat[i][j]
            if norm: 
                rhs[i] = sum_rbf*self.vals[i]
            else: 
                rhs[i] = self.vals[i]
        
        # Then to solve the set of equations for weighting vector w
        self.w = np.linalg.solve(rbf_mat, rhs) 

        

    def interp(self, pt): 
        # returns the interpolated function value at a dim-dimensional point
        if len(pt) != self.dim: 
            raise ValueError('Invalid input size') 
        i = 0
        sum_w = 0 # sum of rbf_vals with weighting values w
        sum_ = 0 # sum of rbf_vals without w for use in normalized case 
        for i in range(self.n): 
            rbf_val = self.rbf_fn(self.rad(pt, self.pts[i]))
            sum_w += self.w[i]*rbf_val
            sum_ += rbf_val
        if self.norm: 
            return sum_w / sum_
        else: 
            return sum_w


    def rbf_fn(self, r): 
        # radial basis function 
        match self.fn: 
            case "multiquadric": 
                return np.sqrt(r**2 + self.scale**2)
            case "inv_multiquadric": 
                return np.power((r**2 + self.scale**2), -0.5) 
            case "thin_plate_spline": 
                return (r**2)*np.log10(r/self.scale)
            case "gaussian": 
                return np.exp(-0.5*(r**2 / self.scale**2)) 


    def rad(self, pt1, pt2):
        # calculates euclidean distance 
        sum_xi = 0
        i = 0
        for i in range(self.dim): 
            sum_xi += (pt1[i] - pt2[i])**2
        return np.sqrt(sum_xi) 


    def err(self): 
        # calculates average error for the interpolated function 
        # removes one known pt/val at a time, then finds error when plugged in
        pass


    def optimize(self): 
        # modifies self.scale such that self.err() is minimized 
        pass

