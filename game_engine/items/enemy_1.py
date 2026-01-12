
import repackage

repackage.up()
from items.template import *

self = Temp("enemy_1")

@self.decorate
def update(tiles):
    exec('''
if self.health <= 0:
    self.anim = self.Ölme
    self.run = False
else:
    x_coord, y_coord = self.info("character")["coords"]
    x_size, y_size = self.info("character")["sizes"]
    if (x_coord + x_size) <= self.coords[0] + 175:
        self.coords[0] -= 2
        self.anim = self.Hareket_Etme
        self.direction = "Left"
    elif x_coord >= (self.coords[0] + self.image_sizes[0]) - 175:
        self.coords[0] += 2
        self.anim = self.Hareket_Etme
        self.direction = "Right"
    else:
        if Pin.değişken_6 == "Sola Kayma" or Pin.değişken_6 == "Sağa Kayma":
            pass
        else:
            self.info("character")["health"] -= 2.5
            self.anim = self.Sabit_Durma
    ''')