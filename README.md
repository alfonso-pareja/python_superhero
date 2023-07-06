# SuperHero Battle Simulator

Este proyecto fue desarrollado como respuesta a la prueba técnica para el proceso de selección en Toku.


## Instalación

Para instalar las dependencias necesarias para este proyecto, puedes usar pip:

```bash
pip install -r requirements.txt
```

## Uso
Para iniciar el proyecto, ejecuta el siguiente script main.py:
```bash
python main.py
```

## Descripción del Proyecto
Al iniciar el proyecto, se crean dos equipos, cada uno compuesto por cinco Superhéroes obtenidos de manera aleatoria desde la API 'https://api.'. Para cada Superhéroe creado, se calculan sus respectivas estadísticas de acuerdo con las especificaciones proporcionadas. El alineamiento de cada equipo se define según la mayoría de personajes con alineamiento 'good' o 'bad'.

Una vez creados los equipos, da inicio la batalla. Para el equipo 'Good', se debe seleccionar el personaje y el ataque, mientras que para el equipo 'Bad', tanto el personaje como el ataque se definen aleatoriamente.

En la terminal, se visualiza constantemente el equipo 'Good' a la izquierda, mostrando detalles del personaje en acción, sus puntos de vida (HP) y los personajes restantes en su equipo. A la derecha, se muestra la misma información correspondiente al equipo 'Bad'. En el centro de la terminal, se visualizan los ataques lanzados por cada personaje y el daño causado.

De esta manera, los personajes de cada equipo se enfrentan en una serie de batallas por turnos, y la victoria se otorga al equipo que logra eliminar a todos los miembros del equipo rival.