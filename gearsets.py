from damage import *
import itertools

class Gear():
	def __init__(self, line):
		line = line.split(",")
		self.slot = line[0]
		self.name = line[1]
		self.wDamage = weaponDamage(line[2])
		self.mainstat = mainStatFloor(line[3], self.slot)
		self.crit = subStatFloor(line[4], self.slot)
		self.det = subStatFloor(line[5], self.slot)
		self.dh = subStatFloor(line[6], self.slot)
		self.sps = subStatFloor(line[7], self.slot)
		self.piety = subStatFloor(line[8], self.slot)

	def __str__(self):
		return ", ".join([str(x) for x in [self.slot,self.name,self.wDamage,
											self.mainstat,self.crit,self.det,
											self.dh,self.sps,self.piety]])

getCrit = lambda  items: sum([i.crit for i in items])
getDet = lambda  items: sum([i.det for i in items])
getDh = lambda  items: sum([i.dh for i in items])
getSps = lambda items: sum([i.sps for i in items])
getPiety = lambda items: sum([i.piety for i in items])



validSpsRanges = [(849,914),(1449,1649)]

def isValid(pieces):
	piety = 364 + sum([p.piety for p in pieces])
	print(piety)
	if piety < 600:
		return False
	else:
		return True
	sps = 364 + sum([p.sps for p in pieces])
	return any([sps > low and sps < high for low, high in validSpsRanges])


gear = {}

with open("gear/gear.txt",'r') as f:
	lines = f.read().split("\n")


for line in lines:
	if ',' in line:
		piece = Gear(line)
		if piece.slot in gear:
			gear[piece.slot].append(piece)
		else:
			gear[piece.slot] = [piece]

gear['ring2'] = gear['ring']



pieces = list(gear.values())
gearSets = list(itertools.product(*pieces))

results = {}
for option in gearSets:
	sps = sum([p.sps for p in option])
	crit = sum([p.crit for p in option])
	det = sum([p.det for p in option])
	dh = sum([p.dh for p in option])
	weaponDamage =sum([p.wDamage for p in option])
	mainStat = sum([p.mainstat for p in option])
	piety = sum([p.piety for p in option])
	pps = potencyPerSec(sps)
	#print(pps)
	d = damageCalc(pps, weaponDamage, 115, mainStat, det, crit, dh, sps, 5)

	#Add Chicken
	d = damageCalc(pps, weaponDamage, 115, mainStat, addFood(det, 168), addFood(crit, 101), dh, sps, 5)
	results[d] = (option, "chicken")

	d = damageCalc(pps, weaponDamage, 115, mainStat, det, addFood(crit, 168), dh, addFood(sps, 101), 5)
	results[d] = (option, "salad")
	#Add Salad
	#print(d)
	
final_sets = sorted(results.items(), key=lambda x: x[0])
for k, v in final_sets:
	print(k, getGcd(getSps(v[0])), getCrit(v[0]),getDet(v[0]),getDh(v[0]),getSps(v[0]) + 364, getPiety(v[0]) + 364)

print(len(final_sets))
damage, (best_set, food) = final_sets[-1]

print([i.name for i in list(best_set)], food)
