from argparse import ArgumentParser
import os
from pathlib import Path
from tqdm import tqdm
from time import sleep

import generator

if __name__ == '__main__':
  parser = ArgumentParser()
  parser.add_argument('input_path', metavar='i', type=str, help='input path to find .mp3 files in')
  parser.add_argument('output_path', metavar='o', type=str, help='output path to store generated files in')

  args = parser.parse_args()

  Path(args.output_path).mkdir(parents=True, exist_ok=True)

  for root, dirs, files in os.walk(args.input_path):
    for name in tqdm(files):
      for out in generator.generate(os.path.join(root, name), args.output_path, 1):
        tqdm.write(out)
