import random

class Character:
    def __init__(self, name, max_health, attack_power, defense, speed):
        self.name = name
        self.health = max_health
        self.max_health = max_health
        self.attack_power = attack_power
        self.defense = defense
        self.speed = speed

    def attack(self, target):
        damage = self.attack_power
        dealt = target.take_damage(damage)
        print(f" {self.name} attacks {target.name}! Deals {dealt} damage.")

    def take_damage(self, amount):
        dmg = max(1, amount - self.defense)
        self.health -= dmg
        return dmg
    
    def is_alive(self):
        return self.health > 0

class Warrior(Character):
    rage = 0
    rage_threshold = 100
    def __init__(self, name):
        super().__init__(name, 130, 22, 12, 6)

    def __str__(self):
        return f"Warrior"

    def take_damage(self, amount):
        dmg = max(1, amount - self.defense)
        self.health -= dmg
        self.rage += dmg
        print(f"{self.name} gains {dmg} rage! Rage: {self.rage}/{self.rage_threshold}")
        return dmg

    def attack(self, target):
        if self.rage >= self.rage_threshold:
                    damage = self.attack_power + 10
                    print(
                        f"{self.name} attacks with rage! +10 bonus attack power."
                    )
                    dealt = target.take_damage(damage)
                    self.rage = 0
        
                    print(
                        f"{self.name} (Warrior) strikes {target.name} with rage! Deals {dealt} damage."
                    )
        elif self.health < 0.30 * self.max_health:
            damage = self.attack_power * 2
            print( f"{self.name} enters Berserk Mode! Attack power doubled." )
            dealt = target.take_damage(damage)
            print( f"{self.name} (Warrior) strikes {target.name} with double power! Deals {dealt} damage." )

        else:
            damage = self.attack_power
            dealt = target.take_damage(damage)
            print( f"{self.name} (Warrior) strikes {target.name}! Deals {dealt} damage." )

class Mage(Character):
    mana = 100
    def __init__(self, name):
        super().__init__(name, 90, 30, 5, 8)

    def __str__(self):
        return f"Mage"

    def attack(self, target):
        if self.mana >= 20:
            mana_cost = 20
            self.mana -= mana_cost
            raw_damage = self.attack_power * 1.5
            dealt = target.take_damage(raw_damage)
            self.health -= 5
            self.health = max(0, self.health)
            print( f"{self.name} (Mage) casts Fireball on {target.name}! Deals {dealt} damage but loses 5 health." )
        else:
            dealt = target.take_damage(self.attack_power)
            print( f"{self.name} (Mage) attacks {target.name}! Deals {dealt} damage." )

class Archer(Character):
    critical_chance = 0.30
    def __init__(self, name):
        super().__init__(name, 100, 24, 7, 12)

    def __str__(self):
        return f"Archer"

    def attack(self, target):
        if random.random() < self.critical_chance:
            damage = self.attack_power * 2
            dealt = target.take_damage(damage)
            print( f"{self.name} (Archer) lands a Critical Hit on " f"{target.name}! Deals {dealt} damage." )
        else: 
            damage = self.attack_power 
            dealt = target.take_damage(damage) 
            print( f"{self.name} (Archer) shoots an arrow at " f"{target.name}! Deals {dealt} damage." )

thor = Warrior("Thor")
gandalf = Mage("Gandalf")
alex = Archer("Alex")
print(thor)
# alex1 = Archer("Alex1")

# thor.attack(gandalf)
# print(gandalf.health)

# alex.attack(thor)
# print(thor.health)

fighters = [thor, gandalf, alex]
turn_order = sorted(fighters, key = lambda x:x.speed, reverse=True)
print([i.name for i in turn_order])

def choose_op(attacker, fighters):
    living_enemies = [f for f in fighters if f is not attacker and f.is_alive()]
    return random.choice(living_enemies) if living_enemies else None


while sum(f.is_alive() for f in fighters) > 1:
        turn_order = sorted(fighters, key=lambda f: f.speed, reverse=True)

        for fighter in turn_order:
            if not fighter.is_alive():
                continue

            if sum(f.is_alive() for f in fighters) <= 1:
                break

            target = choose_op(fighter, fighters)
            if target is None:
                break

            fighter.attack(target)

            if not target.is_alive():
                print(f"{target.name} is defeated!")

champion = [f for f in fighters if f.is_alive()]
print(f"{champion[0].name} ({champion[0]}) wins the battle!")