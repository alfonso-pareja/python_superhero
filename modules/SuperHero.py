import random

class SuperHero:
    def __init__(self, id, name, stats, alignment):
        self.id = id
        self.name = name
        self.alignment = alignment
        self.actual_stamina = random.randint(0, 10)
        self.stats = self.process_stats(stats)
        self.hp = self.calculate_hp()
        self.FB = 1

    def process_stats(self, stats):
        processed_stats = {}
        for stat, value in stats.items():
            # Si el stat viene null, se considera como 0
            if value == 'null':
                value = 0
            processed_stats[stat] = (2 * int(value) + self.actual_stamina) / 1.1
        return processed_stats

    def calculate_hp(self):
        return int(((self.stats['strength'] * 0.8 + self.stats['durability'] * 0.7 + self.stats['power']) / 2) * (1 + (self.actual_stamina / 10))) + 100

    def apply_team_bonus(self, team_alignment):
        # Se aplica el bonus segun el alignment del heroe y team en el que se encuentra
        if team_alignment == self.alignment:
            self.FB = 1 + random.randint(0, 9)
        elif self.alignment == 'neutral':
            self.FB = 1
        else:
            self.FB = (1 + random.randint(0, 9)) ** (-1)

    def attack(self):
        # Se selecciona un ataque al azar
        attack_type = random.choice(['mental', 'strong', 'fast'])

        if attack_type == 'mental':
            return self.mental_attack()
        elif attack_type == 'strong':
            return self.strong_attack()
        else:
            return self.fast_attack()

    def mental_attack(self):
        return (self.stats['intelligence'] * 0.7 + self.stats['speed'] * 0.2 + self.stats['combat'] * 0.1) * self.FB

    def strong_attack(self):
        return (self.stats['strength'] * 0.6 + self.stats['power'] * 0.2 + self.stats['combat'] * 0.2) * self.FB

    def fast_attack(self):
        return (self.stats['speed'] * 0.55 + self.stats['durability'] * 0.25 + self.stats['strength'] * 0.2) * self.FB

    def receive_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    # def __str__(self):
    #     return f'{self.name} [HP: {self.hp}]'
