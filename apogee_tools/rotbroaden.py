# !/usr/bin/env python
# 
# Adding the features of warning and shifting the peak of LSF to the center
# of the numpy array
#
# Aug 14, 2017 Dino Chih-Chun Hsu first built
# Aug 16, 2017 added warning

def lsf_rotate(deltaV, Vsini, epsilon = False, velgrid = False):
	"""Create a 1-d convolution kernel to broaden a spectrum from a rotating star
	Can be used to derive the broadening effect (line spread function; LSF) 
	due to  rotation on a synthetic stellar spectrum. Assumes constant 
	limb darkening across the disk.
	Adapted from rotin3.f in the SYNSPEC software of Hubeny & Lanz 
	.http://nova.astro.umd.edu/index.html    Also see Eq. 17.12 in 
	"The Observation and Analysis of Stellar Photospheres" by D. Gray (1992)
	Written,           W. Landsman          November 2001
	Ported to Python,  C. Theissen          June 2017
	Args:
	    deltaV (float):   Numeric scalar giving the step increment (in km/s) in the output 
	        rotation kernel. 
	    Vsini (float):    The rotational velocity projected  along the line of sight (km/s)
	    epislon (bool; optional): Numeric scalar giving the limb-darkening coefficient, 
	        default = 0.6 which is typical for  photospheric lines. The
	        specific intensity I at any angle theta from the specific intensity
	        Icen at the center of the disk is given by:
	 
	        Example: I = Icen*(1-epsilon*(1-cos(theta))
	    velgrid (bool; optional): Returns a vector with the same number of elements as LSF
	Returns:
	    LSF: The convolution kernel vector for the specified rotational velocity.
			The  number of points in LSF will be always be odd (the kernel is
			symmetric) and equal to  either ceil(2*Vsini/deltav) or 
			ceil(2*Vsini/deltav) +1 (whichever number is odd). LSF will 
			always be of type float.
	
			To actually compute the broadening. the spectrum should be convolved
			with the rotational LSF. 
		velgrid (optional): if keyword 'velgrid' is True, returns a vector with
			the same number of elements as LSF.
	"""

	"""
	if N_params() LT 1 then begin
	     print 'Syntax - rkernel = lsf_rotate(deltav, vsini)'
	     print '      Input Keyword: Epsilon'
	     print '      Output Keyword: Velgrid'
	     return,-1
	endif
	"""
    
	# For Vini smaller than deltaV, return to a new Vsini that is the same as deltaV
	# The resulting LSF is a delta function, with the same amplitude when Vsini = deltaV
	if Vsini < deltaV :
		print("Warning: Vsini ({Vsini} km/s) is smaller than deltaV ({deltaV} km/s)\
, leading to a LSF with a delta function ".format(Vsini=Vsini, deltaV=deltaV))
		Vsini = deltaV
    
	if epsilon == False: 
		epsilon = 0.6
	e1 = 2. * (1. - epsilon)
	e2 = np.pi * epsilon/2.
	e3 = np.pi * (1. - epsilon/3.)

	npts = np.ceil(2.*Vsini/deltaV)

	if npts % 2 == 0: 
		npts = npts +1
	nwid = npts / 2. - 0.5 # Only add -0.5 to shift the peak into the center of the array
	x    = (np.arange(npts)- nwid)
	x    = x * deltaV / Vsini 

	x1 = abs(1.0 - x**2)

	if velgrid: 
		velgrid = x * Vsini
		return (e1*np.sqrt(x1) + e2*x1)/e3, velgrid

	else:
		return (e1*np.sqrt(x1) + e2*x1)/e3


