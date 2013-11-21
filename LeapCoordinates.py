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

def leaptoscreen(posx,posy):
	if posx >= leaplm and posx <= leaprm :
		monx = (posx - leaplm) * monw / leapw
	else :
		monx = -1
	if posy >= leapdm and posy <= leapum :
		mony = (posy - leapdm) * monh / leaph
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
