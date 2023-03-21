from PIL import Image
import os
import sys
import numpy as np
from random import SystemRandom
from numpy.random import default_rng
rng = default_rng()
random = SystemRandom()
# from Crypto.Random import random
# TODO: Add optional overlay image to B share

if len(sys.argv) != 5:
    print("This takes two arguments; the images to be shared.")
    exit()

infile1 = str(sys.argv[1])
infile2 = str(sys.argv[2])
infile3 = str(sys.argv[3])
infile4 = str(sys.argv[4])

if not os.path.isfile(infile1) or not os.path.isfile(infile2)\
        or not os.path.isfile(infile3) or not os.path.isfile(infile4):
    print("Some of the files do not exist")
    exit()

img1 = Image.open(infile1)
img2 = Image.open(infile2)
img3 = Image.open(infile3)
img4 = Image.open(infile4)

f, e = os.path.splitext(infile1)
out_filename_A = "test"+"_A.png"
out_filename_B = "test"+"_B.png"

img1 = img1.convert('1')
img2 = img2.convert('1')
img3 = img3.convert('1')
img4 = img4.convert('1')

# TODO: enforce all equals, plus square

if not img1.size == img2.size:
    print("The two images have to be the same size")
    exit()

print(f"Image size: {img1.size}")

size = img1.size[0]


def sign(x):
    if x == 0:
        return 0
    elif x > 0:
        return 1
    else:
        return -1


def R1(x):
    return 9 * (sign((x+1) % 3)) - 3*((x+1) % 3) + (x)//3


def R2(x):
    return R1(R1(x))


def R3(x):
    return R1(R1(R1(x)))


A = [[np.matrix('0 0 0; 0 0 0; 0 0 0') for y in range(size)]
     for x in range(size)]
B = [[np.matrix('255 255 255; 255 255 255; 255 255 255') for y in range(size)]
     for x in range(size)]


def topos(x):
    return (x//3, x % 3)


for x in range(size):
    for y in range(size):
        if x >= y and x+y+1 < size:
            perm = rng.permutation(9)

            A[x][y][topos(perm[0])] = 255
            A[size-1-y][x][topos(R1(perm[1]))] = 255
            A[size-1-x][size-1-y][topos(R2(perm[2]))] = 255
            A[y][size-1-x][topos(R3(perm[3]))] = 255

            imsum = 4-sum([img1.getpixel((x, y)),
                           img2.getpixel((x, y)),
                           img3.getpixel((x, y)),
                           img4.getpixel((x, y))])//255

            B[x][y][topos(perm[0])] = img1.getpixel((x, y))
            B[x][y][topos(perm[1])] = img2.getpixel((x, y))
            B[x][y][topos(perm[2])] = img3.getpixel((x, y))
            B[x][y][topos(perm[3])] = img4.getpixel((x, y))

            fill = random.sample(sorted(perm[4:9]),
                                 k=(5 - random.randint(0, 1) - imsum))

            for p in fill:
                B[x][y][topos(p)] = 0

            B[size-1-y][x][topos(R1(perm[1]))] = img1.getpixel((size-1-y, x))
            B[size-1-y][x][topos(R1(perm[2]))] = img2.getpixel((size-1-y, x))
            B[size-1-y][x][topos(R1(perm[3]))] = img3.getpixel((size-1-y, x))
            B[size-1-y][x][topos(R1(perm[0]))] = img4.getpixel((size-1-y, x))

            imsum = 4-sum([img1.getpixel((size-1-y, x)),
                           img2.getpixel((size-1-y, x)),
                           img3.getpixel((size-1-y, x)),
                           img4.getpixel((size-1-y, x))])//255

            fill = random.sample(sorted(perm[4:9]),
                                 k=(5 - random.randint(0, 1) - imsum))

            for p in fill:
                B[size-1-y][x][topos(R1(p))] = 0

            B[size-1-x][size-1-y][topos(R2(perm[2]))] \
                = img1.getpixel((size-1-x, size-1-y))
            B[size-1-x][size-1-y][topos(R2(perm[3]))] \
                = img2.getpixel((size-1-x, size-1-y))
            B[size-1-x][size-1-y][topos(R2(perm[0]))] \
                = img3.getpixel((size-1-x, size-1-y))
            B[size-1-x][size-1-y][topos(R2(perm[1]))] \
                = img4.getpixel((size-1-x, size-1-y))

            imsum = 4-sum([img1.getpixel((size-1-x, size-1-y)),
                           img2.getpixel((size-1-x, size-1-y)),
                           img3.getpixel((size-1-x, size-1-y)),
                           img4.getpixel((size-1-x, size-1-y))])//255

            fill = random.sample(sorted(perm[4:9]),
                                 k=(5 - random.randint(0, 1) - imsum))

            for p in fill:
                B[size-1-x][size-1-y][topos(R2(p))] = 0

            B[y][size-1-x][topos(R3(perm[3]))] = img1.getpixel((y, size-1-x))
            B[y][size-1-x][topos(R3(perm[0]))] = img2.getpixel((y, size-1-x))
            B[y][size-1-x][topos(R3(perm[1]))] = img3.getpixel((y, size-1-x))
            B[y][size-1-x][topos(R3(perm[2]))] = img4.getpixel((y, size-1-x))

            imsum = 4-sum([img1.getpixel((y, size-1-x)),
                           img2.getpixel((y, size-1-x)),
                           img3.getpixel((y, size-1-x)),
                           img4.getpixel((y, size-1-x))])//255

            fill = random.sample(sorted(perm[4:9]),
                                 k=(5 - random.randint(0, 1) - imsum))

            for p in fill:
                B[y][size-1-x][topos(R3(p))] = 0

Adraw = np.block(A)
Adraw.reshape(size*3, size*3)
Bdraw = np.block(B)
Bdraw.reshape(size*3, size*3)
out_image_A = Image.new('1', (size*3, size*3))
out_image_B = Image.new('1', (size*3, size*3))
pixels_A = out_image_A.load()
pixels_B = out_image_B.load()
for x in range(size*3):
    for y in range(size*3):
        pixels_A[x, y] = int(Adraw[x][y])
        pixels_B[x, y] = int(Bdraw[x][y])

out_image_A.save(out_filename_A, 'PNG')
out_image_B.save(out_filename_B, 'PNG')
