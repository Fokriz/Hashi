# Hashi Game

[![N|Solid](https://www.pygame.org/images/logo_lofi.png)](https://www.pygame.org/news)



Hashi Game is random generator of Hashi puzzle.
  - Random generate puzzle
  - 15x15 or 25x25 or 35x35 puzzels
  - Magic

# Hashi Rules!

Hashi is played on a rectangular grid with no standard size, although the grid itself is not usually drawn. Some cells start out with (usually encircled) numbers from 1 to 8 inclusive; these are the "islands". The rest of the cells are empty.

The goal is to connect all of the islands by drawing a series of bridges between the islands. The bridges must follow certain criteria:

- They must begin and end at distinct islands, travelling a straight line in between.
- They must not cross any other bridges or islands.
- They may only run orthogonally (i.e. they may not run diagonally).
- At most two bridges connect a pair of islands.
- The number of bridges connected to each island must match the number on that island.
- The bridges must connect the islands into a single connected group.

More about [Hashi](https://en.wikipedia.org/wiki/Hashiwokakero)



## Installation

Hashi Game requires [Python 3](https://www.python.org/) and [PyGame](https://www.pygame.org/wiki/GettingStarted#Pygame%20Installation) lib to run.

Install pygame.

```sh
$ python3 -m pip install -U pygame
```

Run  the Hashi Game.

```sh
$ cd HashiGame
$ python3 HashiGame.py
```

## How to play?

- Click on a Number for select.
- Selected Number is yellow.
- Click on the second Number for make connect.
- You can repeat for make double connect or destroy the connect.
- If the number of connections to a Number is equal to this Number, then the Number is green.


### About project
This project was developed by [Fokriz](https://github.com/Fokriz) and [WuuPmd](https://github.com/WuuPmd) for [Dmitriy Fedorov](https://github.com/dm-fedorov).