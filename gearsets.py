from damage import *
import itertools
from tqdm import tqdm
import sys

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
    self.unique = False
    if len(line) > 9:
      if line[9] == "true":
        self.unique = True

  def __str__(self):
    return ("Slot: " + self.slot).ljust(14) + " | " + \
    ("Name: " + (self.name)).ljust(40) + " | " + \
    ("wDamage: " + str(self.wDamage)).ljust(12)  + " | "+  \
    ("mainstat: " + str(self.mainstat)).ljust(12) + " | " + \
    ("crit: " + str(self.crit)).ljust(12) + " | " + \
    ("det: " + str(self.det)).ljust(12) + " | " + \
    ("dh: " + str(self.dh)).ljust(12) + " | " + \
    ("sps: " + str(self.sps)).ljust(12) + " | " + \
    ("piety: " + str(self.piety)).ljust(12)

getMainstat = lambda items: sum([i.mainstat for i in items])
getCrit = lambda  items: sum([i.crit for i in items])
getDet = lambda  items: sum([i.det for i in items])
getDh = lambda  items: sum([i.dh for i in items])
getSps = lambda items: sum([i.sps for i in items])
getPiety = lambda items: sum([i.piety for i in items])


#If we wanted to check to make sure we have the right sps
#validSpsRanges = [(849,914),(1449,1649)]
validSpsRanges = [(1,3500)]

def isValidGearset(sps, piety=0, minPiety=0):
  return any([sps >= low and sps <= high for (low, high) in validSpsRanges]) and piety >= minPiety

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
gear['ring2'] = [i for i in gear['ring'] if not i.unique]

pieces = list(gear.values())

#Generate all combinations of them

if all([len(i) == 1 for i in pieces]):
  gearSets = [[i[0] for i in pieces]]
else:
  gearSets = list(itertools.product(*pieces))




results = {}
for idx in tqdm(range(len(gearSets)),position=0,leave=True):
  sys.stdout.flush()
  option = gearSets[idx]
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
  if isValidGearset(sps,piety,900):
    d = damageCalc(pps, weaponDamage, 115, mainStat, addFood(crit, 101), addFood(det, 168), dh, sps, 5)
    results[d] = (option, "chicken")


  new_sps = addFood(sps, 101)
  if isValidGearset(new_sps,piety,900):
    pps = potencyPerSec(new_sps)
    d = damageCalc(pps, weaponDamage, 115, mainStat, addFood(crit, 168), det, dh, new_sps, 5)
    results[d] = (option, "salad")
  #Add Salad
  #print(d)
  
final_sets = sorted(results.items(), key=lambda x: x[0])
#for k, v in final_sets:
#print(k, getGcd(getSps(v[0])), getCrit(v[0]) + 364,getDet(v[0]) + 364,getDh(v[0]) + 364,getSps(v[0]) + 364, getPiety(v[0]) + 364)

print(len(final_sets))

for i in range(-5, 0, 1):
  damage, (best_set, food) = final_sets[i]
  print("\n".join([str(i) for i in list(best_set)]))
  

  
  mind = getMainstat(best_set)
  sps =  addFood(getSps(best_set) + 364, (101 if food == "salad" else 0))
  gcd = round(getGcd(sps),2)
  crit = addFood(getCrit(best_set) + 364, (101 if food == "chicken" else 168))
  det = addFood(getDet(best_set) + 364, (168 if food == "chicken" else 0))
  dh = getDh(best_set) + 364
  piety =getPiety(best_set) + 364

  print("Simmed Damage: " + str(damage))
  print("Mainstat: " + str(mind))
  print("GCD: " + str(gcd))
  print("Crit: "+ str(crit) + " | Crit Damage : " + str(getCritDamage(crit)) + " | Crit Rate: " + str(getCritRate(crit)))
  print("Det: " + str(det) + " | Det Multiplier: " + str(getDetMultiplier(det)))
  print("DH: " +  str(dh) + " | DH Rate: " + str(getDhRate(dh)))
  print("Sps: " + str(sps) + " | SPS Multiplier " + str(getSpsScalar(sps)))
  print("Piety: " + str(piety))
  print("Food: " + food)
