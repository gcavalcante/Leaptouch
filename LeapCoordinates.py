leaplm = -410
leaprm = 430
leapum = 980
leapdm = 80
monlm = 0
monrm = 640
monum = 0
mondm = 480
leapw = ((leaprm - leaplm) / 2)
leaph = ((leapum - leapdm) / 2)
monw = ((monrm - monlm) / 2)
monh = ((mondm - monum) / 2)

debug = 1

P = [1.0, 0.0, 0.0]
Q = [0.0, 2.0, 0.0]
R = [0.0, 0.0, 3.0]
N = [0.0, 0.0, 0.0, 0.0, 0.0]

# Calculate borders from points
def calibratepoints(npoints):
	for p in npoints :
		print p

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

	print(planeequation(P,Q,R))   # 6,3,2,6,7

	N[0] = 3.0
	N[1] = 1.0
	N[2] = -2.0
	N[3] = 15
	N[4] = 14.0 ** 0.5
	# Both below shoud be the same
	print(N[4])
	print(distancetoplane(2.0,-3.0,1.0))

	p0 = [-410 ,567  ,-323]
	p1 = [-124 ,-235 ,-345]
	p2 = [-234 ,357  ,-336]
	p3 = [-235 ,-648 ,-376]
	p4 = [-454 ,235  ,-356] #UR
	p5 = [-572 ,-343 ,-385] #BR
	p6 = [346  ,572  ,-353]
	p7 = [373  ,-532 ,-363]
	p8 = [674  ,353  ,-326] #UL
	p9 = [574  ,-262 ,-328] #BL
	NP = [p0, p1, p2, p3, p4, p5, p6, p7, p8, p9]
	calibratepoints(NP)
