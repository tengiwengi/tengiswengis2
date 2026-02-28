from typing import *
from dataclasses import dataclass
import unittest
import sys
sys.setrecursionlimit(10**6)
import string


# a linked list of integers, used to store the unique line
# numbers associated with a particular word in the concordance.

IntList : TypeAlias = Union[None, "IntNode"]
@dataclass(frozen = True)
class IntNode:
    head : int
    rest : IntList
   
@dataclass()
class WordLines:
  key : str
  lines : IntList # a non-frozen [mutable] dataclass representing a key-value pair, containing
 # (1) the key--a word--and
 # (2) the [meant-to-be-mutated] value associated with that word: an IntList representing 
 #     the line numbers where that word occurs.

WordLinesList : TypeAlias = Union[None, "WordLinesNode"]
@dataclass(frozen= True)
class WordLinesNode:
  val : WordLines
  rest : WordLinesList | None # a linked list of WordLines

@dataclass()
class HashTable:
    array : List[WordLinesList]
    count : int

     # a non-frozen [mutable] dataclass containing 
          # (1) an array (Python's `List`) of `WordLinesList`s, and
          # (2) a count of the number of `WordLines`es stored in the hash table.


# Compute the result of the specified hash function on strings
def hash_fn(s: str) -> int:
    h = 0 
    for characters in s:
       h = h * 31 + ord(characters)
    return h 

# Make a fresh hash table with the given size, containing no elements
def make_hash(size: int) -> HashTable:
    array : List[WordLinesList]= [None] * size 
    return HashTable(array, 0)    

# Return the size of the given hash table
def hash_size(ht: HashTable) -> int:
    return len(ht.array)

# Return the number of elements in the given hash table
def hash_count(ht: HashTable) -> int:
    return (ht.count)

# Does the hash table contain a mapping for the given word?
def has_key(ht: HashTable, word: str) -> bool:
  if ht.count == 0:
     return False
  else:
     
     idx = hash_fn(word) % len(ht.array)
     node = ht.array[idx]

     while node is not None:
        if node.val.key == word:
           return True
        node = node.rest
     return False



def converter(initial_list : IntList) -> List[int]:
  new_list : List[int] = [] 
  while initial_list is not None:
     new_list.append(initial_list.head)
     initial_list = initial_list.rest
  return new_list


# What line numbers is the given key mapped to in the given hash table?
# this list should not contain duplicates, but need not be sorted.
def lookup(ht: HashTable, word: str) -> List[int]: 
      idx = hash_fn(word) % len(ht.array)
      node = ht.array[idx]

      while node is not None:
        if node.val.key == word:
           return converter(node.val.lines)
        node = node.rest
      return []
           
  

# Add a mapping from the given word to the given line number in
# the given hash table
def add(ht: HashTable, word: str, line: int) -> None:
  index = hash_fn(word) % len(ht.array)
  node = ht.array[index]

  while node is not None:
        if node.val.key == word:
            # check if line already exists
            current = node.val.lines
            while current is not None:
                if current.head == line:
                    return  # already exists
                current = current.rest
            # prepend new line
            node.val.lines = IntNode(line, node.val.lines)
            return
        node = node.rest

    # new key
  new_word = WordLines(key=word, lines=IntNode(line, None))
  new_node = WordLinesNode(val=new_word, rest=ht.array[index])
  ht.array[index] = new_node
  ht.count += 1   


# What are the words that have mappings in this hash table?
# this list should not contain duplicates, but need not be sorted.
def hash_keys(ht: HashTable) -> List[str]:
  if ht.count == 0:
     return accumulator(ht)
  else:
      return accumulator(ht)

def accumulator (ht : HashTable) -> List[str]:
  accumulated_list : List[str] = []
  if ht.count == 0:
     return accumulated_list
  else:
     for bucket in ht.array:
        node = bucket
        while node is not None:
          accumulated_list.append(node.val.key)
          node = node.rest
     return accumulated_list
      

# given a list of stop words and a list of strings representing lines of
# a text, return a hash table
def make_concordance(stop_words: HashTable, text: List[str]) -> HashTable:
    concordance = make_hash(2 * len(text))
    for line_number, line in enumerate(text, start=1):
        words = split_and_clean(line) 
        
        for word_clean in words:
            if has_key(stop_words, word_clean):
                continue
            add(concordance, word_clean, line_number)
    return concordance

def split_and_clean(word: str) -> List[str]:
    cleaned_words = []
    current = ""

    for c in word:
        if c.isalpha():  # keep letters
            current += c.lower()
        else:  # non-letter: end of current word
            if current != "":
                cleaned_words.append(current)
                current = ""
    if current != "":
        cleaned_words.append(current)

    return cleaned_words

# given an input file , a stop-words file, and an output file, overwrite the output file with
# a sorted concordance of the input file.

def full_concordance(in_file: str, stop_words_file: str, out_file: str) -> None:
    stop_words_ht = make_hash(128) 
    with open(stop_words_file, "r") as f:
        for line in f:
            for word in line.strip().split():
                add(stop_words_ht, word, 0) 

    text_words: List[str] = []
    with open(in_file, "r") as f:
        for line in f:
            text_words.extend(line.strip().split())

    concordance_ht = make_concordance(stop_words_ht, text_words)
    sorted_keys = sorted(hash_keys(concordance_ht))
    with open(out_file, "w") as f:
        for key in sorted_keys:
            lines = lookup(concordance_ht, key)
            line_str = ", ".join(str(l) for l in sorted(lines))
            f.write(f"{key}: {line_str}\n")

ht_man_1 : HashTable = make_hash(1)
add(ht_man_1, "computer", 10)

ht_man_2 : HashTable = make_hash(2)
add(ht_man_2, "science", 1)
add(ht_man_2, "science", 2)
add(ht_man_2, "math", 3)

ht_man_3 : HashTable = make_hash(2)
add(ht_man_3, "physics", 4)
add(ht_man_3, "chemistry", 5)

ht_man_4 : HashTable = make_hash(1)
add(ht_man_4, "biology", 6)
add(ht_man_4, "biology", 7)
add(ht_man_4, "biology", 8)

ht_man_5 : HashTable = make_hash(3)
add(ht_man_5, "history", 9)
add(ht_man_5, "english", 0)

ht_init_1 : HashTable = make_hash(128)
ht_init_2 : HashTable = make_hash(0)
ht_init_3 : HashTable = make_hash(256)
ht_init_4 : HashTable = make_hash(11)
ht_init_5 : HashTable = make_hash(1)

line_1 : List[str] = ["learning", "to", "code", "is", "very", "fun", "indeed"]
line_2 : List[str] = ["debugging", "can", "be", "tough", "but", "rewarding"]
line_3 : List[str] = ["always", "check", "your", "syntax", "and", "logic"]
line_4 : List[str] = ["variables", "loops", "functions", "classes", "objects"]
line_5 : List[str] = ["compile", "run", "test", "deploy", "maintain"]

class TestCase(unittest.TestCase):
    
    def test_hash_fn(self):
        self.assertEqual(hash_fn("hello"), 99162322)
        self.assertEqual(hash_fn("my name is tengis"), 82155404364011468610727913)
        self.assertEqual(hash_fn("i am taking data structures"), 63280573535706715328024084225320484882551)
        self.assertEqual(hash_fn(""), 0) 
        self.assertEqual(hash_fn("!@#$%^"), 1004945849) 

    def test_make_hash(self):
        self.assertEqual(len(ht_init_1.array), 128)
        self.assertEqual(len(ht_init_2.array), 0)
        self.assertEqual(len(ht_init_3.array), 256)
        self.assertEqual(len(ht_init_4.array), 11)
        self.assertEqual(len(ht_init_5.array), 1)

    def test_hash_size(self):
        self.assertEqual(hash_size(ht_init_1), 128)
        self.assertEqual(hash_size(ht_init_2), 0)
        self.assertEqual(hash_size(ht_init_3), 256)
        self.assertEqual(hash_size(ht_init_4), 11)
        self.assertEqual(hash_size(ht_init_5), 1)

    def test_hash_count(self):
        self.assertEqual(hash_count(ht_man_1), 1)
        self.assertEqual(hash_count(ht_man_2), 2)
        self.assertEqual(hash_count(ht_man_3), 2)
        self.assertEqual(hash_count(ht_man_4), 1)
        self.assertEqual(hash_count(ht_man_5), 2)

    def test_has_key(self):
        self.assertTrue(has_key(ht_man_1, "computer"))
        self.assertTrue(has_key(ht_man_2, "science"))
        self.assertFalse(has_key(ht_man_2, "biology"))
        self.assertTrue(has_key(ht_man_4, "biology"))
        self.assertTrue(has_key(ht_man_5, "history"))

    def test_lookup(self):
        self.assertEqual(lookup(ht_man_1, "computer"), [10])
        self.assertEqual(sorted(lookup(ht_man_2, "science")), [1, 2])
        self.assertEqual(lookup(ht_man_3, "physics"), [4])
        self.assertEqual(sorted(lookup(ht_man_4, "biology")), [6, 7, 8])
        self.assertEqual(lookup(ht_man_5, "english"), [0])

    def test_add(self):
        ht = make_hash(10)
        
        add(ht, "apple", 1)
        self.assertTrue(has_key(ht, "apple"))
        self.assertEqual(lookup(ht, "apple"), [1])
        add(ht, "apple", 2)
        self.assertEqual(sorted(lookup(ht, "apple")), [1, 2])
        add(ht, "banana", 3)
        self.assertTrue(has_key(ht, "banana"))
        self.assertEqual(hash_count(ht), 2)
        add(ht, "cherry", 4)
        self.assertEqual(lookup(ht, "cherry"), [4])
        
        add(ht, "banana", 3)
        self.assertEqual(sorted(lookup(ht, "banana")), [3]) 

    def test_hash_keys(self):
        self.assertEqual(hash_keys(ht_man_1), ["computer"])
        self.assertEqual(sorted(hash_keys(ht_man_2)), ["math", "science"])
        self.assertEqual(sorted(hash_keys(ht_man_3)), ["chemistry", "physics"])
        self.assertEqual(hash_keys(ht_man_4), ["biology"])
        self.assertEqual(sorted(hash_keys(ht_man_5)), ["english", "history"])

    def test_make_concordance(self):
        stop_words = ["to", "is", "can", "but", "and"]
        stop_ht = make_hash(20)
        for word in stop_words:
            add(stop_ht, word, 0)

        conc1 = make_concordance(stop_ht, line_1)
        self.assertTrue(has_key(conc1, "learning"))
        self.assertFalse(has_key(conc1, "to"))

        conc2 = make_concordance(stop_ht, line_2)
        self.assertTrue(has_key(conc2, "debugging"))
        self.assertFalse(has_key(conc2, "but"))

        conc3 = make_concordance(stop_ht, line_3)
        self.assertTrue(has_key(conc3, "syntax"))
        
        conc4 = make_concordance(stop_ht, line_4)
        self.assertTrue(has_key(conc4, "loops"))

        conc5 = make_concordance(stop_ht, line_5)
        # "run" is the 2nd item in the list, so it is on line 2
        self.assertEqual(sorted(lookup(conc5, "run")), [2])

if __name__ == '__main__':
    unittest.main()