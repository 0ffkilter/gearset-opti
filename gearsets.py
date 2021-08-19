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
		return ("Slot: " + self.slot).ljust(14) + " | " + \
    ("Name " + (self.name)).ljust(40) + " | " + \
    ("wDamage: " + str(self.wDamage)).ljust(12)  + " | "+  \
    ("mainstat: " + str(self.mainstat)).ljust(12) + " | " + \
    ("crit: " + str(self.crit)).ljust(12) + " | " + \
    ("det: " + str(self.det)).ljust(12) + " | " + \
    ("dh: " + str(self.dh)).ljust(12) + " | " + \
    ("sps: " + str(self.sps)).ljust(12) + " | " + \
    ("piety: " + str(self.piety)).ljust(12)

getCrit = lambda  items: sum([i.crit for i in items])
getDet = lambda  items: sum([i.det for i in items])
getDh = lambda  items: sum([i.dh for i in items])
getSps = lambda items: sum([i.sps for i in items])
getPiety = lambda items: sum([i.piety for i in items])


#If we wanted to check to make sure we have the right sps
validSpsRanges = [(849,914),(1449,1649)]

def isValid(pieces):
	piety = 364 + sum([p.piety for p in pieces])
	#print(piety)
	if piety < 600:
		return False
	else:
		return True

gear = {}

with open("gear/gear.txt",'r') as f:
	lines = f.read().split("\n")


for line in lines:
	if ',' in line and not line.startswith("#"):
		print(line)
		piece = Gear(line)
		if piece.slot in gear:
			gear[piece.slot].append(piece)
		else:
			gear[piece.slot] = [piece]

#Duplicate rings cuz we need 2 of them
gear['ring2'] = gear['ring']

pieces = list(gear.values())

#Generate all combinations of them
gearSets = list(itertools.product(*pieces))

results = {}
for option in gearSets:
	sps = sum([p.sps for p in option]) +364
	crit = sum([p.crit for p in option]) + 364
	det = sum([p.det for p in option]) + 364
	dh = sum([p.dh for p in option]) + 364
	weaponDamage =sum([p.wDamage for p in option])
	mainStat = sum([p.mainstat for p in option])
	piety = sum([p.piety for p in option]) + 364
	#print(sps)
	pps = potencyPerSec(sps)
	#print(pps)

	#Add Chicken
	d = damageCalc(pps, weaponDamage, 115, mainStat, addFood(crit, 101), addFood(det, 168), dh, sps, 5)
	results[d] = (option, "chicken")

	d = damageCalc(pps, weaponDamage, 115, mainStat, addFood(crit, 168), det, dh, addFood(sps, 101), 5)
	results[d] = (option, "salad")
	#Add Salad
	#print(d)
	
final_sets = sorted(results.items(), key=lambda x: x[0])
#for k, v in final_sets:
#print(k, getGcd(getSps(v[0])), getCrit(v[0]) + 364,getDet(v[0]) + 364,getDh(v[0]) + 364,getSps(v[0]) + 364, getPiety(v[0]) + 364)

print(len(final_sets))

for i in range(-1, 0, 1):
  damage, (best_set, food) = final_sets[i]
  print("\n".join([str(i) for i in list(best_set)]))
  print(food)
  print(damage, getGcd(getSps(best_set)),
   getCrit(best_set) + 364,
   getDet(best_set) + 364,
   getDh(best_set) + 364,
   getSps(best_set) + 364,
   getPiety(best_set) + 364)
