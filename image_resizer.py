import os
import glob
import argparse
import itertools
import multiprocessing

import cv2
from tqdm import tqdm


def get_image_filename_recursive(input_dir):
    if not os.path.isdir(input_dir):
        raise Exception(input_dir, 'not a dir!')

    img_filepaths = []
    extensions = ['**/*.jpg', '**/*.png', '**/*.tif']
    for ext in extensions:
        img_filepaths.extend(glob.iglob(os.path.join(input_dir, ext), recursive=True))

    return img_filepaths


def resize_image(args):
    img_filepath, out_img_filepath, w, h = args
    img = cv2.imread(img_filepath)
    img = cv2.resize(img, (w,h))
    cv2.imwrite(out_img_filepath, img)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", dest="input_dir", required=True)
    parser.add_argument("-o", dest="output_dir", required=True)
    parser.add_argument("-width", dest="width", required=True)
    parser.add_argument("-height", dest="height", required=True)
    args = parser.parse_args()

    input_dir = args.input_dir
    output_dir = args.output_dir
    w = int(args.width)
    h = int(args.height)

    n_cpu = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(n_cpu)

    img_filepaths = get_image_filename_recursive(input_dir)
    out_img_filepaths = []
    for img_filepath in img_filepaths:
        out_img_filepath = os.path.join(output_dir, os.path.basename(img_filepath))
        out_img_filepaths.append(out_img_filepath)

    os.makedirs(args.output_dir, exist_ok=True)

    it = pool.imap_unordered(resize_image, zip(img_filepaths, out_img_filepaths,
                                               itertools.repeat(w), itertools.repeat(h)))
    for _ in tqdm(it, total=len(img_filepaths)):
        pass
