from math import floor,ceil

def damageCalc(potencyPerSec, weaponDamage, jobMod, mainStat, crit, det, direct, spellSpeed, classNum):
	#mainstat damage, 1% + per number of classes
	mainStat = floor(mainStat * (1 + 0.01 * classNum))
	
	#weapon damage
	damage = floor(potencyPerSec * (weaponDamage + floor(292 * jobMod/1000)) * (100 + floor((mainStat - 292) * 1000/2336))/100)
	
	#Det Damage
	damage = floor(damage * (1000 + floor(130 * (det - 292)/2170))/1000)
	
	#SPS Damage
	damage = floor(damage * (1000 + floor(130 * (spellSpeed - 364)/2170))/1000/100)

	#Trait Damage
	damage = floor(damage * 1.3)

	#crit damage
	critDamage = floor(damage * (1000 + floor(200 * (crit - 364)/2170 + 400))/1000)

	#dh damage, 25%
	directDamage = floor(damage * 1250/1000)

	#cdh damage
	critDirectDamage = floor(critDamage * 1250/100)

	#crit rate
	critRate = floor(200 * (crit - 364)/2170 + 50)/1000

	#dh rate
	dhRate = floor(550 * (direct - 364)/2170)/1000

	critDirectRate = critRate * dhRate

	normalRate = 1 - critRate - dhRate - critDirectRate

	return damage * normalRate + critDamage * (critRate-critDirectRate) + \
	directDamage * (dhRate - critDirectRate) + critDirectDamage * critDirectRate


def addFood(stat, val, cap=0.1):
	return stat + min(val, stat * cap)

#Can't find formula, so manual benchmarks
gcd_benchmarks = [381,448,515,581,648,715,782,849,915,982,1049,116,1182,1249,1316,1383,1449,1516,1583,1650,1717,1783,1850,1917,1984,2050]

def getGcd(sps):
	gcd = 2.5
	for i in gcd_benchmarks:
		if sps >= i:
			gcd -= .01
		else:
			return gcd
	return gcd

def cycleLen(gcd, casterTax = 0.1):
	if (30 % gcd > 1.5):
		return 6 * ceil(30/gcd) * gcd
	else:
		return 6 * floor(30/gcd) * gcd

def spsScalar(sps):
	return (1000 + floor(130 * (sps - 364)/2170))/1000

def potencyCalc(sps, gcd, cycleLen, gcdDamage=240, dot=40, extra=190):
	#190 potency is 2 free eds and a ruin 2 +ed
	base_damage = extra * 3 * cycleLen/180
	if ((30 -gcd) % gcd > 1.5):
		base_damage += 6 * (ceil(30/gcd) -1) * gcdDamage
		base_damage += 6 * 10 * spsScalar(sps) * dot
	else:
		base_damage += 6 * (floor(30/gcd) - 1) * gcdDamage
		base_damage += 6 * 9 * spsScalar(sps) * dot
		base_damage += 6 * ((3 - (30 % gcd))/3) * spsScalar(sps) * dot
	return base_damage


def potencyPerSec(sps, casterTax=0.1):
	gcd = getGcd(sps)
	cycle = cycleLen(gcd, casterTax)
	return potencyCalc(sps, gcd, cycle)/cycle

subStats = {
	"weapon": 280,
	"hat": 160,
	"chest": 260,
	"hands": 160,
	"legs": 260,
	"shoes": 160,
	"accessory":120
}

accessories = {
	"earrings",
	"neck",
	"wrist",
	"ring",
	"waist"
}

mainStats = {
	"weapon": 308,
	"hat": 176,
	"chest": 286,
	"hands": 176,
	"legs": 286,
	"shoes": 176,
	"accessory":132
}

weaponDamages = {
	"weapon": 135
}

def subStatFloor(stat, slot):
	if slot in accessories:
		slot = "accessory"
	return min(int(stat), subStats[slot])

def mainStatFloor(stat, slot):
	if slot in accessories:
		slot = "accessory"
	return min(int(stat), mainStats[slot])

def weaponDamage(stat):
	return min(int(stat), weaponDamages["weapon"])
