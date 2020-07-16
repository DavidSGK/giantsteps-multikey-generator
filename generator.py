import os
import random
from typing import Callable

import sox

MIN_INTERVAL = 5.
MAX_LENGTH = 120.
MIN_SHIFT = -11
MAX_SHIFT = 11

def generate(input_file: str, output_path: str, n_gen: int = 5):
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

    f_name = os.path.basename(input_file)
    f_segs = f_name.split('.')
    f_segs[0] += f'-{i}'
    out_name = '.'.join(f_segs)

    yield(f'{f_name} gen {i} with {n_keys} keys at {[round(x, 2) for x in starts]} by {shifts} start')

    tfm.build(input_file, os.path.join(output_path, out_name))

    yield(f'{f_name} gen {i} done')
