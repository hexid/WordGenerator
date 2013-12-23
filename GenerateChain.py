#!/bin/env python
from argparse import ArgumentParser
from collections import defaultdict, deque
import json, re

# usage: depth , inDictionary, outJSON
parser = ArgumentParser()
parser.add_argument('depth', metavar='depth', type=int,
  help='The length of any given chain')
parser.add_argument('inFile', type=str,
  help='Input dictionary file')
parser.add_argument('outFile', type=str, nargs='?',
  default='_markov.json', help='Output JSON file (default = _markov.json)')
(args, unknown) = parser.parse_known_args()

class NestedDict(defaultdict):
  def __getitem__(self, item):
    try:
      return dict.__getitem__(self, item)
    except KeyError:
      value = self[item] = type(self)()
      return value

numChar = '#' # holds the total number of words for that sequence
endChar = '.' # holds the number of words that end with that sequence

rootNode = NestedDict()
rootNode['depth'] = args.depth # set the depth of the chain
with open(args.inFile) as f:
  for word in f.read().split():
    if re.match('^[a-z]+$', word.strip()):
      chars = deque(maxlen = args.depth) # limit to args.depth chars
      for w in range(args.depth):
        chars.append(' ') # start with args.depth spaces

      # append endChar to the word before processing it
      for character in (word + endChar):
        chars.append(character) # add the next character

        node = rootNode # start at the root of the tree
        for i in range(args.depth-1):
          node = node[chars[i]] # traverse down the tree

        # increment the total for the leaves on the branch
        node[numChar] = node.get(numChar, 0) + 1
        # increment the total for the current leaf
        node[character] = node.get(character, 0) + 1

with open(args.outFile, 'w') as f:
  # print the json data to outFile
  # the json data will be sorted and compressed to save space
  f.write(json.dumps(rootNode, sort_keys=True, separators=(',',':')))
