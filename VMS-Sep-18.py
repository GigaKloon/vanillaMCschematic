import os
from PIL import Image


class BlockEditor:
    def __init__(self, file):
        self.files = os.listdir()
        self.functions = []
        for i in self.files:
            if i.endswith('.mcfunction'):
                self.functions.append(i)
        self.file = file
        self.dump = ""

    def load(self):
        with open(self.file, "w") as f:
            f.write(self.dump)

    def fill(self, rel_x, rel_y, rel_z, rel_x1, rel_y1, rel_z1, block):
        command = "fill "
        for i in (rel_x, rel_y, rel_z, rel_x1, rel_y1, rel_z1):
            command += f"~{i} "
        command += block
        self.dump += command+"\n"

    def setblock(self, rel_x, rel_y, rel_z, block):
        command = "setblock "
        for i in (rel_x, rel_y, rel_z):
            command += f"~{i} "
        command += block
        self.dump += command + "\n"


class ParticleEditor:
    def __init__(self, file):
        self.files = os.listdir()
        self.functions = []
        for i in self.files:
            if i.endswith('.mcfunction'):
                self.functions.append(i)
        self.file = file
        self.dump = ""

    def bitmap_to_2d_array(self, image_path, threshold=128, g_l=False):
        img = Image.open(image_path).convert('L')
        width, height = img.size
        binary_array = []
        if g_l:
            for y in range(height):
                row = []
                for x in range(width):
                    pixel = img.getpixel((x, y))
                    # Convert pixel to binary based on the threshold
                    row.append(1 if pixel < threshold else 0)
                binary_array.append(row)
            return binary_array
        else:
            for y in range(height):
                row = []
                for x in range(width):
                    pixel = img.getpixel((x, y))
                    # Convert pixel to binary based on the threshold
                    row.append(1 if pixel < threshold else 0)
                binary_array.append(row)
            return binary_array

    def load(self):
        with open(self.file, "w") as f:
            f.write(self.dump)

    def particle(self, bitmap, particle_name, size_x, size_y, d_z, gl=True):
        width = len(self.bitmap_to_2d_array(bitmap))
        height = len(self.bitmap_to_2d_array(bitmap)[0])
        dx = width / (2*size_x)
        dy = height / (2*size_y) 
        particle_arrays = ""
        bitmap_array = self.bitmap_to_2d_array(bitmap, g_l=gl)
        for i in enumerate(bitmap_array):
            for j in enumerate(i[1]):
                if bitmap_array[i[0]][j[0]] == 1:
                    particle_arrays += (f"particle {particle_name} ~{round(i[0]/size_x-dx, 4)} ~{d_z} ~"
                                        f"{round(j[0]/size_y-dy, 4)}\n")
                    # print(f"size x: {size_x}, dx = {dx}")
                    # print(f"pos_x: {round(i[0]/size_x-dx, 4)}, size y: {round(j[0]/size_y-dy, 4)}")
        self.dump += particle_arrays


class EntityExecutor:
    def __init__(self, file):
        self.files = os.listdir()
        self.functions = []
        for i in self.files:
            if i.endswith('.mcfunction'):
                self.functions.append(i)
        self.file = file
        self.dump = ""

    def load(self):
        with open(self.file, "w") as f:
            f.write(self.dump)

    def execute(self, target, command):
        self.dump += f"execute as {target} at {command}\n"
