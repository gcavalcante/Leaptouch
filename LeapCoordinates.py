import numpy
from numpy import linalg

# leaplm = -410
# leaprm = 430
# leapum = 980
# leapdm = 80
# monlm = 0
# monrm = 2560
# monum = 0
# mondm = 1600
# leapw = ((leaprm - leaplm))
# leaph = ((leapum - leapdm))
# monw = ((monrm - monlm) )
# monh = ((mondm - monum))

debug = 1

# P = [1.0, 0.0, 0.0]
# Q = [0.0, 2.0, 0.0]
# R = [0.0, 0.0, 3.0]
# N = [0.0, 0.0, 0.0, 0.0, 0.0]

class Translator:

	def __init__(self):
		self.display = []
		self.leap = []

	def add_point(self, display, leap):
		self.display.append(display)
		self.leap.append(leap)

	def calculate(self):
		A = numpy.zeros((3,3))
		A[0] = self.BR - self.BL
		A[1] = self.TL - self.BL
		A[2] = numpy.cross(A[0], A[1])
		A[2] /= numpy.linalg.norm(A[2])

		self.A = A

	def project(self, p):
		q = p
		p = self.BL
		n = self.A[2]

		q_proj = q - numpy.dot(q - p, n) * n
		return q_proj

	def get_x(self, p):
		p = numpy.array(p) 

		proj = self.project(p) - self.BL
		#print p, proj

		return numpy.dot(proj, self.A[0]/numpy.linalg.norm(self.A[0])) / numpy.linalg.norm(self.A[0])


	def get_y(self, p):
		p = numpy.array(p) 

		proj = self.project(p) - self.BL
		#print p, proj

		return numpy.dot(proj, self.A[1]/numpy.linalg.norm(self.A[1])) / numpy.linalg.norm(self.A[1])

	def get_z(self, p):
		p = numpy.array(p)
		proj = self.project(p)
		d = proj - p
		return numpy.linalg.norm(d)

	# Calculate borders from points
	def calibratepoints(self, npoints):
		UL = [0.0,0.0,0.0]
		UR = [0.0,0.0,0.0]
		BL = [0.0,800000.0,0.0]
		BR = [0.0,800000.0,0.0]
		for p in npoints :
			if p[0] < 0 and p[1] > UL[1]:
				UL = p
			if p[0]	> 0 and p[1] > UR[1]:
				UR = p
			if p[0] < 0 and p[1] < BL[1]:
				BL = p
			if p[0]	> 0 and p[1] < BR[1]:
				BR = p
		self.TL = numpy.array(UL)
		self.TR = numpy.array(UR)
		self.BL = numpy.array(BL)
		self.BR = numpy.array(BR)
		self.calculate()

	def leaptransform(self, p):
		return [t.get_x(p), t.get_y(p), t.get_z(p)]

if debug:
	t = Translator()
	p0 = [-410 ,567  ,-323] #UL
	p1 = [-124 ,-235 ,-345]
	p2 = [-234 ,357  ,-336]
	p3 = [-235 ,-648 ,-376] #BL
	p4 = [-454 ,235  ,-356]
	p5 = [-572 ,-343 ,-385]
	p6 = [346  ,572  ,-353] #UR
	p7 = [373  ,-532 ,-363] #BR
	p8 = [674  ,353  ,-326]
	p9 = [574  ,-262 ,-328]
	NP = [p0, p1, p2, p3, p4, p5, p6, p7, p8, p9]
	t.calibratepoints(NP)
	EP = [p0, p3, p6, p7]
	for p in EP :
		print t.leaptransform(p)

# Leap to Screen correlation
# def leaptoscreen(posx, posy):
# 	if posx >= leaplm and posx <= leaprm :
# 		monx = (posx - leaplm) * monw / leapw
# 	else :
# 		monx = -1
# 	if posy >= leapdm and posy <= leapum :
# 		mony = abs(posy - leapum) * monh / leaph
# 	else :
# 		mony = -1
# 	return [monx, mony]

# if debug :
# 	print(leaptoscreen(-411, 79)) # -1, -1
# 	print(leaptoscreen(431, 981)) # -1, -1
# 	print(leaptoscreen(-410, 80)) # 0, 480
# 	print(leaptoscreen(430, 980)) # 640, 0
# 	print(leaptoscreen(10, 530))  # 320, 240

# 	print(leapratio(-411, 79)) # -1, -1
# 	print(leapratio(431, 981)) # -1, -1
# 	print(leapratio(-410, 80)) # 0, 480
# 	print(leapratio(430, 980)) # 640, 0
# 	print(leapratio(10, 530))  # 320, 240

# 	print(planeequation(P,Q,R))   # 6,3,2,6,7

# 	print
# 	print(distancetoplane(1.0,0.0,0.0))
# 	print(distancetoplane(0.0,2.0,0.0))
# 	print(distancetoplane(0.0,0.0,3.0))

# 	N[0] = 3.0
# 	N[1] = 1.0
# 	N[2] = -2.0
# 	N[3] = 15
# 	N[4] = 14.0 ** 0.5
# 	# Both below shoud be the same
# 	print(N[4])
# 	print(distancetoplane(2.0,-3.0,1.0))

# 	p0 = [-410 ,567  ,-323] #UL
# 	p1 = [-124 ,-235 ,-345]
# 	p2 = [-234 ,357  ,-336]
# 	p3 = [-235 ,-648 ,-376] #BL
# 	p4 = [-454 ,235  ,-356]
# 	p5 = [-572 ,-343 ,-385]
# 	p6 = [346  ,572  ,-353] #UR
# 	p7 = [373  ,-532 ,-363] #BR
# 	p8 = [674  ,353  ,-326]
# 	p9 = [574  ,-262 ,-328]
# 	NP = [p0, p1, p2, p3, p4, p5, p6, p7, p8, p9]
# 	print(calibratepoints(NP))