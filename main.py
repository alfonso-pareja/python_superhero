import requests
import time
import random
from common.console import (clear, pause, center_message, hero_combat)
from modules.SuperHero import SuperHero
from modules.Team import Team
from common.constants import (
    _API_KEY, _TOTAL_HEROES, _GREEN, _RED, _BLUE, _NO_COLOR, _WIN
)



def get_random_heroes(num_heroes):
    # Se obtienen aleatoriamente de la cantidad total de Super Heroes, una Lista de numeros de la longitud de num_heroes.
    # Los id de superheroes coinciden con su posicion en la lista
    hero_ids = random.sample(range(1, _TOTAL_HEROES + 1), num_heroes)
    heroes = []
    # Por cada id de la lista, se obtiene un super heroe
    for hero_id in hero_ids:
        response = requests.get(f"https://superheroapi.com/api/{_API_KEY}/{hero_id}")
        data = response.json()
        # Se crea el personaje
        hero = SuperHero(data['id'], data['name'], data['powerstats'], data['biography']['alignment'])
        print(f'Personaje: {hero.name}')
        heroes.append(hero)
    return heroes

def create_team(team_name):
    # Obtiene una lista de 5 heroes de forma aleatoria
    heroes = get_random_heroes(5)
    # Devuelve un nuevo Team creado con los super heroes obtenidos
    return Team(team_name, heroes)

def set_team_alignment(team1, team2):
    # Si ambos equipos tienen la misma alineación, se decide basado en la cantidad de héroes 'good'
    if team1.alignment == team2.alignment:
        # Se cuenta la cantidad de "good" para cada equipo
        team1_count = sum(1 for hero in team1.heroes if hero.alignment == 'good')
        team2_count = sum(1 for hero in team2.heroes if hero.alignment == 'good')

        # Si el team 1 contiene mas 'good' que team 2, se define team 1 como 'good' 
        if team1_count > team2_count:
            team1.alignment = 'good'
            team2.alignment = 'bad'
        elif team2_count > team1_count:
            # Si el team 2 contiene mas 'good' que team 1, se define team 2 como 'good' 
            team1.alignment = 'bad'
            team2.alignment = 'good'
        else:  
            # Si tienen la misma cantidad de héroes 'good', se decide al azar
            alignments = ['good', 'bad']
            random.shuffle(alignments)
            team1.alignment = alignments[0]
            team2.alignment = alignments[1]


    # Se aplican los bonus por cada team, enviando el alignment del team
    for hero in team1.heroes:
        hero.apply_team_bonus(team1.alignment)
    for hero in team2.heroes:
        hero.apply_team_bonus(team2.alignment)

    return team1, team2


def choice_hero(heroes):
    print("Selecciona tu Héroe:")
    # Se lista la posicion y nombre de cada heroe
    for i, hero in enumerate(heroes, start=1):
        print(f"{i}. {hero.name}")
    hero_choice = input("Seleccion: ")

    # Se controlan los errores encaso de que la seleccion no coincida con lo esperado
    try:
        selected_hero = heroes[int(hero_choice) - 1]
    except (ValueError, IndexError):
        selected_hero = heroes[0]
        print(f'{_RED}No seleccionaste ningún héroe, se seleccionó a {selected_hero.name}{_NO_COLOR}')
    return selected_hero


def choice_attack(hero):
    # Se visualizan por consola los ataques a utilizar
    print(f"Selecciona un ataque para {hero.name}:")
    print("1. Mental attack")
    print("2. Strong attack")
    print("3. Fast attack")
    attack_choice = input("Seleccion: ")

    # Se controlan los errores en caso de que la seleccion no coincida con lo esperado
    try:
        attack_choice = int(attack_choice)
        
        # Si la opcion ingresada no coincide con los numeros de la lista, se lanza un error
        if attack_choice < 1 or attack_choice > 3:
            raise ValueError
    # Se captura el error lanzado como ValueError
    except ValueError:
        # se selecciona por defecto el ataque 1
        attack_choice = 1
        print(f'{_RED}No seleccionaste ningún ataque, se seleccionó un ataque por defecto{_NO_COLOR}')
        time.sleep(1)

    return attack_choice

def simulate_battle(teamHeroes, teamEnemies):
    clear()
    center_message(">>>> Comienza la Batalla <<<<")
    heroes  = teamHeroes.heroes
    enemies = teamEnemies.heroes
    while True:
        # Seleccion del Heroe
        hero = choice_hero(heroes)
        print(" ")

        # Seleccion del ataque
        attack_choice = choice_attack(hero)

        if attack_choice == 1:
            attack_method = hero.mental_attack
        elif attack_choice == 2:
            attack_method = hero.strong_attack
        elif attack_choice == 3:
            attack_method = hero.fast_attack
        else:
            attack_method = hero.mental_attack

        # Team 2 Selecciona Personaje y Ataque de forma aleatoria
        enemy = random.choice(enemies)
        attack_method2 = random.choice([enemy.mental_attack, enemy.strong_attack, enemy.fast_attack])

        # Console Messages
        clear()
        hero_combat(hero, len(teamHeroes.heroes), teamHeroes.name, enemy, len(teamEnemies.heroes), teamEnemies.name)

        # Aplicar el daño causado al enemigo
        damage = round(attack_method(), 1)
        enemy.receive_damage(damage)

        # Console Messages
        clear()
        hero_combat(hero, len(teamHeroes.heroes), teamHeroes.name, enemy, len(teamEnemies.heroes), teamEnemies.name)
        center_message(f" >> {_GREEN}{hero.name} uso {attack_method.__name__} en {enemy.name} y causo {damage} de daño{_NO_COLOR}  <<")
        center_message(f"{enemy.name} HP: {enemy.hp}")
        time.sleep(1)

        # Si el Enemigo quedo sin HP
        if enemy.hp <= 0:
            # Console Messages
            pause()
            clear()
            hero_combat(hero, len(teamHeroes.heroes), teamHeroes.name, enemy, len(teamEnemies.heroes), teamEnemies.name)
            center_message(f"{_BLUE}{hero.name} ha derrotado a {enemy.name}!{_NO_COLOR}")

            # Se elimina el enemigo de la lista de personajes para su team
            enemies.remove(enemy)
            if not enemies:
                # Console Messages
                clear()
                print("\n")
                center_message(f"Los héroes triunfan, el {teamHeroes.name} venció! {_WIN}")
                break

        # Console Messages
        pause()
        clear()
        hero_combat(hero, len(teamHeroes.heroes), teamHeroes.name, enemy, len(teamEnemies.heroes), teamEnemies.name)
        
        # Aplicar el daño causado al Heroe
        damage = round(attack_method2(), 1)
        hero.receive_damage(damage)
        
        # Console Messages
        clear()
        hero_combat(hero, len(teamHeroes.heroes), teamHeroes.name, enemy, len(teamEnemies.heroes), teamEnemies.name)
        center_message(f" >> {_RED}{enemy.name} uso {attack_method2.__name__} en {hero.name} y causo {damage} de daño{_NO_COLOR}  <<")
        center_message(f"{hero.name} HP: {hero.hp}")
        time.sleep(1)

        # Si el Heroe quedo sin HP
        if hero.hp <= 0:
            # Console Messages
            clear()
            hero_combat(hero, len(teamHeroes.heroes), teamHeroes.name, enemy, len(teamEnemies.heroes), teamEnemies.name)
            center_message(f"{_BLUE}{enemy.name} ha derrotado a {hero.name}!{_NO_COLOR}")
            pause()

            # Se elimina al Heroe de la lista de personajes para su team
            heroes.remove(hero)
            if not heroes:
                # Console Messages
                clear()
                print("\n")
                center_message(f"Los enemigos triunfan en esta batalla. El {teamEnemies.name} gana! {_WIN}")
                break

        time.sleep(1)




def main():
    clear()
    print(f'{_BLUE}Creando personajes para el Equipo 1!{_NO_COLOR}\n')

    # Creando primer grupo de personajes
    team1 = create_team('Equipo 1')
    time.sleep(1)
    clear()

    print(f'{_BLUE}Creando personajes para el Equipo 2!{_NO_COLOR}\n')

    # Creando segundo grupo de personajes
    team2 = create_team('Equipo 2')
    time.sleep(1)
    clear()

    # Se asigna el alignment para el team
    team1, team2 = set_team_alignment(team1, team2)
    
    messageTeam1 = f"""
        {_GREEN}Equipo 1 creado!{_NO_COLOR}
        Aligment: {team1.alignment.capitalize()}
        Personajes: {", ".join(personaje.name for personaje in team1.heroes)}
    """
    messageTeam2 = f"""
        {_GREEN}Equipo 2 creado!{_NO_COLOR}
        Aligment: {team2.alignment.capitalize()}
        Personajes: {", ".join(personaje.name for personaje in team2.heroes)}
    """
    
    print(messageTeam1)
    print(messageTeam2)
    print("\n")
    pause()

    # Para conocer siempre al Heroe o Enemigo en la batalla, se envia en orden de (heroe, enemigo) a la funcion
    if team1.alignment == 'good' and team2.alignment == 'bad':
        simulate_battle(team1, team2)
    else:
        simulate_battle(team2, team1)

if __name__ == "__main__":
    main()
