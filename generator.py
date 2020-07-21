import json
import os
import random
from typing import Callable

import sox

from key import Key

MIN_INTERVAL = 5.
MAX_LENGTH = 120.
MIN_SHIFT = -5
MAX_SHIFT = 5

class MissingAnnotationError(Exception):
  pass

def original_key(in_file: str, annotations_path: str) -> Key:
  try:
    f_name = os.path.basename(in_file)
    annotation_f_name = '.'.join(f_name.split('.')[:-1] + ['key'])
    annotation_path = os.path.join(annotations_path, annotation_f_name)

    with open(annotation_path, 'r') as a:
      return Key.parse(a.readline().strip())
  except FileNotFoundError as e:
    raise MissingAnnotationError(e)

def generate(in_file: str, ann_in_path: str, out_path: str, ann_out_path: str, n_gen: int = 5):
  try:
    key = original_key(in_file, ann_in_path)
  except MissingAnnotationError as e:
    yield(f'Missing annotation for {in_file}. Skipping.')
    return

  for i in range(n_gen):
    tfm = sox.Transformer()

    n_keys = random.choice([1, 2, 2, 2, 3, 3, 3])
    shifts = random.choices([s for s in range(MIN_SHIFT, MAX_SHIFT + 1)], k=n_keys)
    keypoints = sorted([random.uniform(MIN_INTERVAL, MAX_LENGTH - MIN_INTERVAL) for _ in range(n_keys - 1)])

    if len(keypoints) == 2:
      while keypoints[1] - keypoints[0] < MIN_INTERVAL:
        keypoints = sorted([random.uniform(MIN_INTERVAL, MAX_LENGTH - MIN_INTERVAL) for _ in range(2)])

    starts = [1e-5] + keypoints

    if n_keys > 1:
      # Limitation: can't shift by 0 using bend
      tfm.bend(n_keys, starts, [kp + 0.01 for kp in starts], [s * 100 if s != 0 else 1 for s in shifts])
    else:
      tfm.pitch(shifts[0])

    f_name = os.path.basename(in_file)
    f_segs = f_name.split('.')
    f_segs[0] += f'-{i}'
    out_name = '.'.join(f_segs)

    yield(f'{f_name} gen {i} with {n_keys} keys at {[round(x, 2) for x in starts]} by {shifts} from {key} start')

    tfm.build(in_file, os.path.join(out_path, out_name))

    ann_out_name = '.'.join(f_segs[:-1] + ['json'])
    serialized_keys = []
    last_key = key
    for j in range(n_keys):
      shifted = last_key.shift(shifts[j])
      serialized_keys.append({ 'start': round(starts[j], 2), 'key': str(shifted) })
      last_key = shifted

    with open(os.path.join(ann_out_path, ann_out_name), 'w') as a:
      json.dump(serialized_keys, a)

    yield(f'{f_name} gen {i} done')
