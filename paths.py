import os
import copy

import numpy as np
import matplotlib.pyplot as plt

from time import sleep, time



clear = lambda: os.system('cls')


def main():

    population_ = 5

    x = os.get_terminal_size()[0]
    y = os.get_terminal_size()[1]

    size_ = (1080, 1920)
    #size_ = (y - 1, int(x/2) - 1)
    map = np.zeros(size_)

    field_ = generate_field(size_)
    #print(field_)
    blobs_ = generate_blobs(population_, size_)

    #print_field(field_, size_, blobs_)

    simulate(field_, size_, blobs_, map)



def simulate(field, size, blobs, map):

    run = 0
    steps = 100000
    i=0

    #t0 = time()
    for j in range(steps):

    #while run == 0:
        i+=1
        for k in range(len(blobs)):
            try:
                x, y = move_blob(blobs[k], size, field)
            except TypeError:
                blobs.pop(k)
                blobs.append(create_blob(size))
            map[x,y] += 1
            place = field[x][y]
            if place == "0":
                field[x][y] = "1"
            elif place == "1":
                field[x][y] = "2"
            elif place == "2":
                field[x][y] = "3"
            elif place == "3":
                field[x][y] = "4"
            elif place == "4":
                field[x][y] = "5"
            else:
                field[x][y] = "6"

        # if i%1 == 0:
        #     print_field(field, size, blobs)
        #     sleep(0.1)

    save_png(map, "test")

    #t1 = time()
    #print(t1-t0, (t1-t0) / steps)

    # 100 steps, 2 blobs: 3.756828784942627 0.03756828784942627
    # 100 steps, 20 blobs: 4.194448232650757 0.04194448232650757


def move_blob(blob, size, field):

    x = np.random.uniform(-1,1)#int(-1,high=2)
    y = np.random.uniform(-1,1)#int(-1,high=2)

    v_x, v_y = get_field(blob, field)

    a,b,c = 0.5, 1.5, 1 # good: 1.4, 1.2, 0.9 best: 0.5, 1.5, 1

    dx = a*x + b*blob[2] + c*v_x
    dy = a*y + b*blob[3] + c*v_y

    blob[0] += round(dx/np.sqrt(dx**2+dy**2))
    blob[1] += round(dy/np.sqrt(dx**2+dy**2))

    # if blob[0] >= size[0]:
    #     blob[0] -= size[0]
    #
    # if blob[1] >= size[1]:
    #     blob[1] -= size[1]
    #
    # if blob[0] < 0:
    #     blob[0] += size[0]
    #
    # if blob[1] < 0:
    #     blob[1] += size[1]

    if blob[0] >= size[0] or blob[1] >= size[1] or blob[0] < 0 or blob[1] < 0:
        return None

    return blob[0], blob[1]

def get_field(blob, field):
    x, y = blob[0], blob[1]
    v_x, v_y = 0, 0
    try:
        up = field[x][y-1] + field[x-1][y-1] + field[x+1][y-1]
        down = field[x][y+1] + field[x-1][y+1] + field[x+1][y+1]
        left = field[x-1][y] + field[x-1][y-1] + field[x-1][y+1]
        right = field[x+1][y] + field[x+1][y-1] + field[x+1][y+1]
        #up, down, left, rigt = field_values[up], field_values[down], field_values[left], field_values[right]

        v_x = -int(left) + int(right)
        v_y = -int(up) + int(down)

    except (IndexError, ValueError):
        return 0, 0

    if v_x != 0 or v_y != 0:
        v_x = v_x/np.sqrt(v_x**2+v_y**2)
        v_y = v_y/np.sqrt(v_x**2+v_y**2)
    else:
        return 0, 0

    return v_x, v_y

def generate_blobs(population, size):

    blobs_ = []

    for _ in range(population):

        blobs_.append(create_blob(size))

    return blobs_



def create_blob(size):

    x = np.random.randint(size[0])
    y = np.random.randint(size[1])

    dx = np.random.uniform(-1,1)
    dy = np.random.uniform(-1,1)

    return [x, y, dx/np.sqrt(dx**2 + dy**2), dy/np.sqrt(dx**2+dy**2)]



def generate_field(size):
    field=[]

    for i in range(size[0]):
        field.append([])
        for j in range(size[1]):
            field[i].append("0")

    return field



def print_field(field, size, blobs):

    clear()
    field_ = copy.deepcopy(field)

    for i in range(size[0]):
        for j in range(size[1]):
            for blob in blobs:
                if (i,j) == (blob[0], blob[1]):
                    field_[i][j] = "o"

    for i in range(size[0]):
        for j in range(size[1]):
            print(str(field_values[field_[i][j]]) + " ", end="")
        print("")

field_values = {
  ".": 0,
  "0": ".",
  "1": 1,
  "2": 2,
  "3": 3,
  "4": 4,
  "5": 5,
  "6": 6,
  "7": 7,
  "8": 8,
  "9": 9,
  "o": "o"

}

def save_png(data, name):
    sizes = np.shape(data)
    fig1 = plt.figure()
    fig1.set_size_inches(1 , 1 * sizes[0] / sizes[1], forward = False)
    axis = plt.Axes(fig1, [0., 0., 1., 1.])
    axis.set_axis_off()
    fig1.add_axes(axis)
    axis.imshow(data)
    #name = f'{data=}'.split('=')[0] + ".png"
    plt.savefig(name + ".png", dpi = sizes[0])
    #plt.close()

if __name__ == '__main__':
    main()

"""
TODOs:

- ww zwischen pfaden und wegwahl

Done:
- blobs zielstrebiger machen
- teleport an rändern
- pfade
"""
