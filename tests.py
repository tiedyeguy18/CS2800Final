import unittest
from main import *

import sys

class Tester(unittest.TestCase):

    def test_get_possible_answers(self):
        self.assertEqual(set(get_possible_answers("allwords_nodups.txt", "examples.txt")), set(["dogs", "gods", "bods", "dobs", "mods"]))
        self.assertEqual(get_possible_answers("exampleWords.txt", "examples.txt"), ["dogs"])
        self.assertEqual(get_possible_answers("allwords_nodups.txt", "examples2.txt"), ["magic"])
        self.assertEqual(set(get_possible_answers("allwords_nodups.txt", "examples3.txt")), set(["was", "saw"]))
        self.assertEqual(set(get_possible_answers("allwords_nodups.txt", "examples4.txt")), set(["rats", "arts", "star", "cart", "tars"]))
        self.assertEqual(set(get_possible_answers("allwords_nodups.txt", "examples5.txt")), set(["kin", "yin", "ink"]))
        self.assertEqual(set(get_possible_answers("allwords_nodups.txt", "spesner.txt")), set(["spam", "maps", "amps", "tamp", "trek", "take", "teak", "sake"]))

        self.assertRaises(ValueError, get_possible_answers, "exampleWords.txt", "examples6.txt")
        self.assertRaises(ValueError, get_possible_answers, "exampleWordsBad.txt", "examples.txt")
        self.assertRaises(FileNotFoundError, get_possible_answers, "exampleordsBad.txt", "examples.txt")
        self.assertRaises(FileNotFoundError, get_possible_answers, "exampleWordsBad.txt", "exmples.txt")

    def test_list_equal_z3(self):
        self.assertEqual(list_equal_z3([], []), True)
        self.assertEqual(list_equal_z3([1], []), False)
        self.assertEqual(list_equal_z3([], [2]), False)
        self.assertEqual(list_equal_z3([1], [1]), And(True,True))
        self.assertEqual(list_equal_z3([1,2,3], [1,2,3]), And(True,And(True,And(True,True))))
        self.assertEqual(list_equal_z3([1], [2]), And(False, True))
        self.assertEqual(list_equal_z3([1], [1,2]), And(True, False))
        self.assertEqual(list_equal_z3([Int("x")], [1]), And(Int("x") == 1, True))
        self.assertEqual(list_equal_z3([Int("x")], [1,2]), And(Int("x") == 1, False))
        self.assertEqual(list_equal_z3([Int("x"),Int("y")], [1]), And(Int("x") == 1, False))
        self.assertEqual(list_equal_z3([Int("x"),Int("y")], [1,2]), And(Int("x") == 1,And(Int("y") == 2, True)))
        self.assertEqual(list_equal_z3([Int("x"),Int("y")], [1,2,3]), And(Int("x") == 1,And(Int("y") == 2, False)))

        s = Solver()

        x = [ Int(f"x_{i}") for i in range(5) ]
        s.add(list_equal_z3(x, [1,2,3,4,5]))

        self.assertEqual(s.check(), sat)
        s.add(x[0] == 1)
        self.assertEqual(s.check(), sat)
        s.add(x[1] == 3)
        self.assertEqual(s.check(), unsat)

    def test_num_in_list_z3(self):
        self.assertEqual(num_in_list_z3(1, []), False)
        self.assertEqual(simplify(num_in_list_z3(1, [1])), True)
        self.assertEqual(simplify(num_in_list_z3(1, [1, 2])), True)
        self.assertEqual(simplify(num_in_list_z3(2, [1, 2])), True)
        self.assertEqual(simplify(num_in_list_z3(1, [2, 3, 4])), False)
        self.assertEqual(num_in_list_z3(Int("x"), []), False)

        s = Solver()

        x = Int("x")
        s.add(num_in_list_z3(x, [1,2,3,4,5]))

        self.assertEqual(s.check(), sat)
        s.add(x == 3)
        self.assertEqual(s.check(), sat)

        s = Solver()

        x = Int("x")
        s.add(num_in_list_z3(x, [1,2,3,4,5]))

        self.assertEqual(s.check(), sat)
        s.add(x == 0)
        self.assertEqual(s.check(), unsat)

    def test_list_in_lol_z3(self):
        self.assertEqual(list_in_lol_z3([], [[]]), Or(True, False))
        self.assertEqual(list_in_lol_z3([1], [[]]), Or(False, False))
        self.assertEqual(list_in_lol_z3([], [[1]]), Or(False, False))
        self.assertEqual(list_in_lol_z3([1], [[1]]), Or(And(True, True), False))
        self.assertEqual(list_in_lol_z3([2], [[1]]), Or(And(False, True), False))
        self.assertEqual(list_in_lol_z3([1,2], [[1]]), Or(And(True, False), False))
        self.assertEqual(list_in_lol_z3([1], [[1,2]]), Or(And(True, False), False))
        self.assertEqual(list_in_lol_z3([1,2], [[1,2]]), Or(And(True, And(True, True)), False))
        self.assertEqual(list_in_lol_z3([1,2], [[1],[1,2]]), Or(And(True, False), Or(And(True, And(True, True)), False)))
        self.assertEqual(list_in_lol_z3([Int("x")], [[1]]), Or(And(Int("x") == 1, True), False))
        self.assertEqual(list_in_lol_z3([Int("x")], [[1],[2]]), Or(And(Int("x") == 1, True), Or(And(Int("x") == 2, True), False)))

        s = Solver()

        x = [ Int(f"x_{i}") for i in range(5) ]
        s.add(list_in_lol_z3(x, [[1],[1,2,3,4,5],[1,2,3],[5,2,4,3,1]]))
        self.assertEqual(s.check(), sat)
        s.add(x[1] == 2)
        self.assertEqual(s.check(), sat)
        s.add(x[0] == 1)
        self.assertEqual(s.check(), sat)
        s.add(x[3] == 4)
        self.assertEqual(s.check(), sat)
        s.add(x[4] == 3)
        self.assertEqual(s.check(), unsat)

    def test_match_number_z3(self):
        self.assertEqual(match_number_z3([], [], 0), True)
        self.assertEqual(match_number_z3([], [], 1), False)
        self.assertEqual(match_number_z3([], [1], 0), True)
        self.assertEqual(simplify(match_number_z3([1], [1], 1)), True)
        self.assertEqual(simplify(match_number_z3([1], [1], 0)), False)
        self.assertEqual(simplify(match_number_z3([2, 1], [1], 1)), True)
        self.assertEqual(simplify(match_number_z3([1, 2], [2, 1], 2)), True)
        self.assertEqual(simplify(match_number_z3([1, 2], [2, 1], 1)), False)
        self.assertEqual(simplify(match_number_z3([1, 2, 3], [3, 1, 2], 3)), True)
        
        self.assertEqual(simplify(match_number_z3([1], [Int('a')], 1)), Int('a') == 1)
        self.assertEqual(simplify(match_number_z3([1, 2], [Int('a'), Int('b')], 2)), simplify(And(Or(Int('a') == 1, Int('b') == 1), Or(Int('b') == 2, Int('a') == 2))))
        self.assertEqual(simplify(match_number_z3([1, 2], [Int('a'), Int('b')], 1)), simplify(Or(Int('b') == 1, Int('a') == 1) == Not(Or(Int('b') == 2, Int('a') == 2))))
        self.assertEqual(simplify(match_number_z3([1], [Int('a'), Int('b')], 1)), simplify(Or(Int('b') == 1, Int('a') == 1)))
        
        s = Solver()
        x = [ Int(f"x_{i}") for i in range(5) ]
        s.add(match_number_z3(x, [1, 2, 3, 4, 5], 3))
        self.assertEqual(s.check(), sat)
        
        s.add(x[0] == 4)
        self.assertEqual(s.check(), sat)
        s.add(x[1] == 1)
        self.assertEqual(s.check(), sat)
        s.add(x[2] == 5)
        self.assertEqual(s.check(), sat)
        s.add(x[3] == 2)
        self.assertEqual(s.check(), unsat)

    def test_get_allwords_and_guesses(self):
        self.assertEqual(get_allwords_and_guesses("exampleWords.txt", "examples.txt"),
                        ([[2, 14, 20, 15], [3, 14, 6, 18], [3, 14, 13, 18],
                                 [3, 14, 18, 19], [7, 0, 21, 4], [17, 14, 3, 18],
                                 [18, 11, 8, 15], [18, 14, 22, 18], [18, 20, 3, 18]],
                         {'have': 0, 'slip': 1, 'coup': 1, 'dost': 3, 'rods': 3, 'dons': 3}, 4))
        self.assertRaises(ValueError, get_allwords_and_guesses, "exampleWordsBad.txt", "examples.txt")
        self.assertRaises(FileNotFoundError, get_allwords_and_guesses, "exampleordsBad.txt", "examples.txt")
        self.assertRaises(FileNotFoundError, get_allwords_and_guesses, "exampleWordsBad.txt", "exmples.txt")
    
    def test_binary_search(self):
        self.assertEqual(binary_search(1, []), -1)
        self.assertEqual(binary_search('', []), -1)
        self.assertEqual(binary_search(1, [1]), 0)
        self.assertEqual(binary_search(1, [0]), -1)
        self.assertEqual(binary_search(2, [1, 2, 3]), 1)
        self.assertEqual(binary_search("hello", ["goodbye", "hello", "former", "raise"]), 1)
        self.assertEqual(binary_search("hello", ["goodbye", "hell", "former", "raise"]), -1)

    def test_str_to_list_nums(self):
        self.assertEqual(str_to_list_nums(""), [])
        self.assertEqual(str_to_list_nums("a"), [0])
        self.assertEqual(str_to_list_nums("b"), [1])
        self.assertEqual(str_to_list_nums("m"), [12])
        self.assertEqual(str_to_list_nums("y"), [24])
        self.assertEqual(str_to_list_nums("z"), [25])
        self.assertEqual(str_to_list_nums("abmyz"), [0, 1, 12, 24, 25])
        self.assertEqual(str_to_list_nums("dogs"), [3, 14, 6, 18])
        self.assertRaises(ValueError, str_to_list_nums, "A")
        self.assertRaises(ValueError, str_to_list_nums, "{")
        self.assertRaises(ValueError, str_to_list_nums, "Z")
        self.assertRaises(ValueError, str_to_list_nums, "abracaDABra")

    def test_list_nums_to_str(self):
        self.assertEqual(list_nums_to_str([]), "")
        self.assertEqual(list_nums_to_str([0]), "a")
        self.assertEqual(list_nums_to_str([1]), "b")
        self.assertEqual(list_nums_to_str([12]), "m")
        self.assertEqual(list_nums_to_str([24]), "y")
        self.assertEqual(list_nums_to_str([25]), "z")
        self.assertEqual(list_nums_to_str([0, 1, 12, 24, 25]), "abmyz")
        self.assertEqual(list_nums_to_str([3, 14, 6, 18]), "dogs")
        self.assertRaises(ValueError, list_nums_to_str, [-1])
        self.assertRaises(ValueError, list_nums_to_str, [26])
        self.assertRaises(ValueError, list_nums_to_str, [1, 2, 4, 8, 16, 32, 64])

    def test_num_to_char(self):
        self.assertEqual(num_to_char(0), 'a')
        self.assertEqual(num_to_char(1), 'b')
        self.assertEqual(num_to_char(12), 'm')
        self.assertEqual(num_to_char(24), 'y')
        self.assertEqual(num_to_char(25), 'z')
        self.assertRaises(ValueError, num_to_char, -1)
        self.assertRaises(ValueError, num_to_char, 26)
        self.assertRaises(ValueError, num_to_char, 97)

    def test_char_to_num(self):
        self.assertEqual(char_to_num('a'), 0)
        self.assertEqual(char_to_num('b'), 1)
        self.assertEqual(char_to_num('m'), 12)
        self.assertEqual(char_to_num('y'), 24)
        self.assertEqual(char_to_num('z'), 25)
        self.assertRaises(ValueError, char_to_num, 'A')
        self.assertRaises(ValueError, char_to_num, '{')
        self.assertRaises(ValueError, char_to_num, 'Z')
        self.assertRaises(TypeError, char_to_num, '')
        self.assertRaises(TypeError, char_to_num, 'hi')

##    def test_match_number(self):
##        self.assertEqual(match_number(str_to_list_nums("cats"), str_to_list_nums("dogs")), 1)
##        self.assertEqual(match_number(str_to_list_nums("spool"), str_to_list_nums("cools")), 4)
##        self.assertEqual(match_number(str_to_list_nums("rose"), str_to_list_nums("rats")), 2)
##        self.assertEqual(match_number(str_to_list_nums("dog"), str_to_list_nums("cat")), 0)
##        self.assertEqual(match_number(str_to_list_nums("have"), str_to_list_nums("dogs")), 0)
##        self.assertEqual(match_number(str_to_list_nums("slip"), str_to_list_nums("dogs")), 1)
##        self.assertEqual(match_number(str_to_list_nums("coup"), str_to_list_nums("dogs")), 1)
##        self.assertEqual(match_number(str_to_list_nums("sows"), str_to_list_nums("dogs")), 2)
##        self.assertEqual(match_number(str_to_list_nums("suds"), str_to_list_nums("dogs")), 2)
##        self.assertEqual(match_number(str_to_list_nums("dost"), str_to_list_nums("dogs")), 3)
##        self.assertEqual(match_number(str_to_list_nums("rods"), str_to_list_nums("dogs")), 3)
##        self.assertEqual(match_number(str_to_list_nums("dons"), str_to_list_nums("dogs")), 3)
##        self.assertEqual(match_number(str_to_list_nums("dogs"), str_to_list_nums("dogs")), 4)
##        self.assertEqual(match_number(str_to_list_nums("error"), str_to_list_nums("roars")), 3)
##        self.assertEqual(match_number(str_to_list_nums("d"), str_to_list_nums("h")), 0)
##        self.assertEqual(match_number(str_to_list_nums("d"), str_to_list_nums("d")), 1)
##        self.assertEqual(match_number(str_to_list_nums(""), str_to_list_nums("")), 0)
##        self.assertEqual(match_number(str_to_list_nums(""), str_to_list_nums("a")), 0)
##        self.assertEqual(match_number(str_to_list_nums("dog"), str_to_list_nums("dogs")), 3)
##
##        s = str_to_list_nums("hello")
##        self.assertEqual(match_number(s[:],s), 5)
##        self.assertEqual(s, str_to_list_nums("hello"))
##
##    def test_remove_z3(self):
##        self.assertEqual(remove_z3(1, [], []), True)
##        self.assertEqual(remove_z3(1, [1], []), True)
##        self.assertEqual(remove_z3(1, [1], [1]), False)
##        self.assertEqual(remove_z3(1, [], [1]), False)
##        self.assertEqual(remove_z3(1, [1,2], [1]), If(True, And(False, True), And(True, True)))
##        self.assertEqual(remove_z3(1, [1,2], [2]), If(True, And(True, True), And(False, True)))
##        self.assertEqual(remove_z3(2, [1,2], [2]), If(False, And(True, True), And(False, True)))
##        self.assertEqual(remove_z3(2, [2,2], [2]), If(True, And(True, True), And(True, True)))
##        self.assertEqual(remove_z3(1, [], [Int("x")]), False)
##        self.assertEqual(remove_z3(1, [1], [Int("x")]), False)
##        self.assertEqual(remove_z3(1, [1, 2], [Int("x")]), If(True, And(Int("x") == 2, True), And(Int("x") == 1, True)))
##
##        s = Solver()
##
##        s.add(remove_z3(2, [1,2,3], [Int("y"), Int("z")]))
##
##        s.check()
##        m = s.model()
##
##        self.assertEqual(m.decls()[0].name(), "z")
##        self.assertEqual(m.decls()[1].name(), "y")
##        self.assertEqual(m[m.decls()[0]], 3)
##        self.assertEqual(m[m.decls()[1]], 1)
##
##        s = Solver()
##
##        s.add(remove_z3(2, [2,2,2], [Int("y"), Int("z")]))
##
##        s.check()
##        m = s.model()
##
##        self.assertEqual(m.decls()[0].name(), "z")
##        self.assertEqual(m.decls()[1].name(), "y")
##        self.assertEqual(m[m.decls()[0]], 2)
##        self.assertEqual(m[m.decls()[1]], 2)
##
##        s = Solver()
##
##        s.add(remove_z3(2, [2,1,2], [Int("y"), Int("z")]))
##
##        s.check()
##        
##        m = get_next_model(s)
##
##        self.assertEqual(m.decls()[0].name(), "y")
##        self.assertEqual(m.decls()[1].name(), "z")
##        self.assertEqual(m[m.decls()[0]], 2)
##        self.assertEqual(m[m.decls()[1]], 1)
##
##        m = get_next_model(s)
##
##        self.assertEqual(m.decls()[0].name(), "y")
##        self.assertEqual(m.decls()[1].name(), "z")
##        self.assertEqual(m[m.decls()[0]], 1)
##        self.assertEqual(m[m.decls()[1]], 2)


##        s = Solver()
##
##        s.add(match_number_z3([1,2,3], [Int("a"), Int("b"), Int("c")], 2))
##
##
##        print(s.assertions())
##        while s.check() == sat:
##            print (s.model())
##            s.add(Or(Int(a != s.model()[a], b != s.model()[b]))

        

if __name__ == '__main__':
    sys.setrecursionlimit(10**5)

    unittest.main()
