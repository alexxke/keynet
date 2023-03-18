import os
import glob
import numpy as np
import h5py
from PIL import Image

keydb = h5py.File('keydb.h5', 'w')

# key images are structured as ./alex_key_img/{bitting}{o or r}.jpg

bittings_str = {os.path.basename(x)[:-5] for x in glob.glob('./alex_key_img/*.jpg')}
bittings_str = sorted(list(bittings_str))

for face in ['obverse', 'reverse']:
    face_images = []
    for bitting_str in bittings_str:
        img = Image.open(f'./alex_key_img/{bitting_str}{face[0]}.jpg')
        w, h = img.size
        subimg = img.crop((w//2 - 1024, h//2 - 1024, w//2 + 1024, h//2 + 1024))
        subimg = subimg.resize((512, 512))
        face_images.append(np.asarray(subimg, dtype=np.uint8))
    face_images = np.stack(face_images)
    keydb[face] = face_images

keydb['bittings'] = np.array(
    [[int(bit) for bit in bitting] for bitting in bittings_str],
    dtype=np.uint8
)

keydb.close()