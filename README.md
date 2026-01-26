## PyGameEngine

**PyGameEngine** is a custom game engine built in **Python**, focusing on **modularity**, **reusability**, and clean architectural design. 
And I want to suffer in PyGame...
It provides a structured foundation for developing 2D games while keeping core engine logic separate from gameplay rules.

This repository also serves as a long-term reference for game engine design decisions and performance considerations in Python.

---

## Features

- **Modular Architecture** – Engine components are easy to extend and reuse, such as Animation, Camera, Light, Physic and UI
- **Core Game Mechanics** – Physics, event handling, and motor functions
- **Structured Gameplay Logic** – Clear separation between engine and game logic
- **Built with PyGame** – Uses PyGame for rendering, input, and timing

---

## Requirements

| Library     | Version |
| ----------- | ------- |
| `pygame`    | 2.6.1   |
| `Pillow`    | 10.4.0  |
| `PyQt5`     | 5.15.11 |
| `repackage` | 0.7.3   |

---

## Installation

Clone the repository and navigate into the project directory:

```sh
git clone https://github.com/Osman-Kahraman/PyGameEngine.git
cd PyGameEngine
pip install -r requirements.txt
```

---

## Project Structure

```
PyGameEngine/
├── game_1/                     # Example game
│   ├── datas/                  # Game entities & world objects
│   │   ├── tiles.py            # Tile rendering & map logic
│   │   └── tiles.json          # Tile definitions & level data
│   │
│   ├── items/                  # Game entities & world objects
│   │   ├── character.py        # Player character logic
│   │   ├── enemy_1.py          # Enemy behavior & AI
│   │   ├── streetLight.py      # Environment / static objects
│   │   ├── info.py             # Item rendering
│   │   └── info.json           # Item metadata & configuration
│   │
│   └── images/                 # Global game assets
│
├── game_engine/                # Core game engine package
│   ├── items/                  # Game entities & world objects
│   │   └── template.py         # Base template for new game items
│   │
│   ├── ui/                     # UI & gameplay flow layer
│   │   ├── images/             # UI-related assets
│   │   ├── designer.py         # UI layout & scene composition
│   │   ├── game.py             # Core gameplay state & loop control
│   │   ├── home.py             # Home / menu screen logic
│   │   └── main.py             # Engine entry point
│   │
│   ├── package.py              # Engine motors (physics, update loop)
│   ├── event.py                # Centralized event handling
│   ├── game_state.py           # Global variable holder
│   └── news.txt                # Engine notes / dev logs
│
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies
├── LICENSE                     # MIT License
```

---

## Usage

After the installation of required libraries,
Run this project using this command:

```sh
python3 game_engine/ui/main.py
```
