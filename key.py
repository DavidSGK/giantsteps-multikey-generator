from __future__ import annotations
from enum import Enum

class Tonic(Enum):
  # NOTE: We notate everything in flat keys for now (data set only has flat key annotations)
  C   = 0
  Db  = 1
  D   = 2
  Eb  = 3
  E   = 4
  F   = 5
  Gb  = 6
  G   = 7
  Ab  = 8
  A   = 9
  Bb  = 10
  B   = 11

class Mode(Enum):
  major = 0
  minor = 1

class Key():
  @staticmethod
  def parse(key_str: str):
    tonic_str, mode_str = key_str.split(' ')

    return Key(Tonic[tonic_str], Mode[mode_str])

  def __init__(self, tonic: Tonic, mode: Mode):
    self.tonic = tonic
    self.mode = mode

  def shift(self, delta: int) -> Key:
    return Key(Tonic((self.tonic.value + delta) % 12), self.mode)

  def __repr__(self) -> str:
    return f'{self.tonic.name} {self.mode.name}'
