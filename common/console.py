
"""
Mensajes de la consola
"""


import os
from common.constants import (
    _GREEN, _RED, _BLUE, _NO_COLOR
)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input("\nPresione Enter para continuar...")

def center_message(message, secondMessage=None):
    rows, columns = os.popen('stty size', 'r').read().split()
    print(message.center(int(columns)))
    print(secondMessage.center(int(columns))) if secondMessage is not None else ''

def get_console_dimensions():
    rows, columns = os.popen('stty size', 'r').read().split()
    return rows, columns

def hero_combat(hero, remaining_heroes, hero_team_name, enemy, remaining_enemies, enemy_team_name):
    heroes_message = f"""
    Heroe Actual: {hero.name}
    HP: {hero.hp}
    Team: {hero_team_name}
    Alignment:  {_GREEN}Good{_NO_COLOR}
    Restantes: {remaining_heroes}
    """

    enemies_message = f"""
    Enemigo Actual: {enemy.name}
    HP: {enemy.hp}
    Team: {enemy_team_name}
    Alignment: {_RED}BAD{_NO_COLOR}
    Restantes: {remaining_enemies}
    """


    heroes  = heroes_message.split("\n")
    enemies = enemies_message.split("\n")

    rows, columns = get_console_dimensions()
    for left, right in zip(heroes, enemies):
        print(f"{left.ljust(int(columns)//2)}{right.rjust(int(columns)//2)}")