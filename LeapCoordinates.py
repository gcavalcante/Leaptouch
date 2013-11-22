leaplm = -410
leaprm = 430
leapum = 980
leapdm = 80
monlm = 0
monrm = 2560
monum = 0
mondm = 1600
leapw = ((leaprm - leaplm))
leaph = ((leapum - leapdm))
monw = ((monrm - monlm) )
monh = ((mondm - monum))

debug = 1

P = [1.0, 0.0, 0.0]
Q = [0.0, 2.0, 0.0]
R = [0.0, 0.0, 3.0]
N = [0.0, 0.0, 0.0, 0.0, 0.0]

# Calculate borders from points
def calibratepoints(npoints):
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
	return [UL, UR, BL, BR]

# Leap to Screen correlation
def leaptoscreen(posx, posy):
	if posx >= leaplm and posx <= leaprm :
		monx = (posx - leaplm) * monw / leapw
	else :
		monx = -1
	if posy >= leapdm and posy <= leapum :
		mony = abs(posy - leapum) * monh / leaph
	else :
		mony = -1
	return [monx, mony]

# Leap to Screen ratio
def leapratio(posx, posy):
	if posx >= leaplm and posx <= leaprm :
		monx = (posx - leaplm) * monw / leapw
	else :
		monx = -1
	if posy >= leapdm and posy <= leapum :
		mony = abs(posy - leapum) * monh / leaph
	else :
		mony = -1
	return [monx, mony]

# Plane equation in the form of Ax + By + Cz = D.
# Also computes S = SQRT(A^2 + B^2 + C^2)
# N = [A,B,C,D,S]
def planeequation(P, Q, R):
	N = [0,0,0,0,0]
	U = [Q[0] - P[0], Q[1] - P[1], Q[2] - P[2]]
	V = [R[0] - P[0], R[1] - P[1], R[2] - P[2]]
	N[0] = (U[1] * V[2]) - (U[2] - V[1]) # A
	N[1] = (U[2] * V[0]) - (U[0] * V[2]) # B
	N[2] = (U[0] * V[1]) - (U[1] * V[0]) # C
	N[3] = (N[0] * P[0]) + (N[1] * P[1]) + (N[2] * P[2]) # D 
	N[4] = ((N[0] ** 2) + (N[1] ** 2) + (N[2] ** 2)) ** 0.5
	return N

# Distance from point P(posx, posy, posz) to plane in N
def distancetoplane(posx, posy, posz) :
	return abs((N[0] * posx) + (N[1] * posy) + (N[2] * posz) - N[3]) / N[4]

if debug :
	print(leaptoscreen(-411, 79)) # -1, -1
	print(leaptoscreen(431, 981)) # -1, -1
	print(leaptoscreen(-410, 80)) # 0, 480
	print(leaptoscreen(430, 980)) # 640, 0
	print(leaptoscreen(10, 530))  # 320, 240

	print(leapratio(-411, 79)) # -1, -1
	print(leapratio(431, 981)) # -1, -1
	print(leapratio(-410, 80)) # 0, 480
	print(leapratio(430, 980)) # 640, 0
	print(leapratio(10, 530))  # 320, 240

	print(planeequation(P,Q,R))   # 6,3,2,6,7

	N[0] = 3.0
	N[1] = 1.0
	N[2] = -2.0
	N[3] = 15
	N[4] = 14.0 ** 0.5
	# Both below shoud be the same
	print(N[4])
	print(distancetoplane(2.0,-3.0,1.0))

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
	print(calibratepoints(NP))
