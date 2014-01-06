#!/bin/env python
# usage: depth , inDictionary [, outJSON]

def generateChain(depth, inFile):
  import collections, re
  numChar, endChar = '#', '.'
  regexWord = re.compile('^[a-z]+$')
  depthRange = range(depth - 1)
  padStr = ' ' * (depth - 1)
  chars = collections.deque(maxlen = depth) # limit to depth chars

  def NestedDict(): return collections.defaultdict(NestedDict)
  rootNode = NestedDict() # create a tree of dictionaries
  rootNode['depth'] = depth # set the depth of the chain
  curNode, curChar = None, None

  with open(inFile, 'r') as f:
    for word in f.read().split():
      if regexWord.match(word):
        chars.extend(padStr) # reset chars for the new word
        for curChar in "%s%s" % (word, endChar):
          chars.append(curChar) # add the next character

          curNode = rootNode # start at the root of the tree
          for n in depthRange: # traverse down the tree
            curNode = curNode[chars[n]]

          # increment the total for the leaves on the branch
          curNode[numChar] = curNode.get(numChar, 0) + 1
          # increment the total for the current leaf
          curNode[curChar] = curNode.get(curChar, 0) + 1
  return rootNode

def writeToFile(chain, outFile):
  with open(outFile, 'w') as f:
    import json # write the json data to outFile
    # the json data will be sorted and compressed to save space
    f.write(json.dumps(chain, sort_keys=True, separators=(',',':')))

def main():
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument('depth', metavar='depth', type=int, help='The length of any given chain')
  parser.add_argument('inFile', type=str, help='Input dictionary file')
  parser.add_argument('outFile', type=str, nargs='?', default='_markov.json', help='Output JSON file (default = _markov.json)')
  (args, unknown) = parser.parse_known_args()

  chain = generateChain(args.depth, args.inFile)
  writeToFile(chain, args.outFile)

if __name__ == "__main__":
  main()
