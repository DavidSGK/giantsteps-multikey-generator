from argparse import ArgumentParser
import os
from pathlib import Path
from tqdm import tqdm
from time import sleep

import generator

if __name__ == '__main__':
  parser = ArgumentParser()
  parser.add_argument('in_path', metavar='i', type=str, help='input path to find .mp3 files in')
  parser.add_argument('ann_in_path', metavar='ai', type=str, help='path to find associated annotations in')
  parser.add_argument('in_count', metavar='ic', type=int, help='how many input files to process before stopping, 0 for no limit')
  parser.add_argument('out_path', metavar='o', type=str, help='output path to store generated files in')
  parser.add_argument('ann_out_path', metavar='ao', type=str, help='path to output generated assotiations to')
  parser.add_argument('per_count', metavar='pc', type=int, help='how many variations to generate per input track')

  args = parser.parse_args()

  Path(args.out_path).mkdir(parents=True, exist_ok=True)
  Path(args.ann_out_path).mkdir(parents=True, exist_ok=True)

  for root, dirs, files in os.walk(args.in_path):
    to_process = files[:args.in_count] if args.in_count > 0 else files
    for name in tqdm(to_process):
      for out in generator.generate(os.path.join(root, name), args.ann_in_path, args.out_path, args.ann_out_path, args.per_count):
        tqdm.write(out)
