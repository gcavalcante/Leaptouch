leaplm = -360
leaprm = 330
leapum = 580
leapdm = 272
monlm = 0
monrm = 2560
monum = 0
mondm = 1600
leapw = ((leaprm - leaplm))
leaph = ((leapum - leapdm))
monw = ((monrm - monlm) )
monh = ((mondm - monum))

def leaptoscreen(posx,posy):
	if posx >= leaplm and posx <= leaprm :
		monx = (posx - leaplm) * monw / leapw
	else :
		monx = -1
	if posy >= leapdm and posy <= leapum :
		mony = abs(posy - leapum) * monh / leaph
	else :
		mony = -1
	return [monx, mony]

def leapnormalizedz(posx, posy, posz):
	if 0 > 1 :
		normz = -1
	else :
		normz = blebleble

print(leaptoscreen(-411, 79))
print(leaptoscreen(431, 981))
print(leaptoscreen(-410, 80))
print(leaptoscreen(430, 980))
print(leaptoscreen(10, 530))
print(leaptoscreen(-360, 580))
