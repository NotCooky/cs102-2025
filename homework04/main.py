from life import GameOfLife
from life_gui import GUI

if __name__ == "__main__":
    life = GameOfLife((20, 20), randomize=True)

    gui = GUI(life=life, cell_size=20, speed=10)

    gui.run()
