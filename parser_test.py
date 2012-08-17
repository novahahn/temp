#!/usr/bin/env python3.2

from unittest import TestCase, main, skip
from parser import *


class TreeTest(TestCase):
    def test_multiple_children(self):
        children = [1, 2]
        tree = Tree(None, children)
        self.assertEqual(tree.children, children)

#class TestCNF(TestCase):
#    def test_binarize(self):
#        grammar = {
#            Rule("a", ["b", "c", "d"], 1)
#        }
#        expected = 
#        self.assertEquals(



class TestRule(TestCase):
    def test_split_simple(self):
        rule = Rule("a", ["b", "c"])
        self.assertEqual({rule}, set(rule.split()))

    def test_split(self):
        rule = Rule("a", ["b", "c", "d"])
        self.assertEqual(
            {
            Rule("a", ["b", SplitTag(["c", "d"])]),
            Rule(SplitTag(["c", "d"]), ["c", "d"])
            },
            set(rule.split())
        )

    def test_eq(self):
        rule1 = Rule("a", ["b", "c"])
        rule2 = Rule("b", ["b", "c"])
        self.assertNotEqual(rule1, rule2)
        rule3 = Rule("a", ["b", "c"])
        self.assertEqual(rule1, rule3)

    def test_str(self):
        rule = Rule("a", ["apfel"])
        self.assertEqual(rule.right_side[0], "apfel")

grammar = {
    Rule("S", ["NP", "VP"]),
    Rule("VP", ["VP", "PP"]),
    Rule("VP", ["V", "NP"]),
    Rule("VP", ["eats"]),
    Rule("PP", ["P", "NP"]),
    Rule("NP", ["Det", "N"]),
    Rule("NP", ["she"]),
    Rule("V", ["eats"]),
    Rule("P", ["with"]),
    Rule("N", ["fish"]),
    Rule("N", ["fork"]),
    Rule("Det", ["a"])
}

unary_grammar = {
    Rule("S", ["NP", "VP"]),
    Rule("VP", ["V"]),
    Rule("NP", ["John"]),
    Rule("V", ["eats"])
}

unary_grammar2 = {
    Rule("S", ["S2"]),
    Rule("NP", ["she"]),
    Rule("S2", ["NP", "VP"]),
    Rule("VP", ["eats"])
}


class TestParse(TestCase):
    correct_sentence = [("she", "NP"), ("eats", "V"), ("a", "Det"), ("fish", "N")]
    correct_unary_sentence = [("John", "NP"), ("eats", "V")]
    correct_unary_sentence2 = [("she", "NP"), ("eats", "VP")]
    def test_init(self):
        result = cyk_init(Grammar(grammar).pospruned, self.correct_sentence)
        expected = defaultdict(lambda: False,
            {
                (1, 1, PospruningTag("NP")): True,
                (2, 1, PospruningTag("V")): True,
                (3, 1, PospruningTag("Det")): True,
                (4, 1, PospruningTag("N")): True
            }
            )
        self.assertEqual(set(result.items()), set(expected.items()))

    def test_true(self):
        self.assertIsNotNone(parse(grammar, self.correct_sentence))

    def test_false(self):
        self.assertIsNone(parse(grammar, [("she", "NP"), ("fish", "N"), ("eats", "V")]))

    def test_unary_true(self):
        self.assertIsNotNone(parse(unary_grammar, self.correct_unary_sentence))

    def test_unary_false(self):
        self.assertIsNone(parse(unary_grammar, [("eats", "V"), ("John", "NP")]))

    def test_unary_true2(self):
        self.assertIsNotNone(parse(unary_grammar2, self.correct_unary_sentence2))



class TestGrammar(TestCase):
    def setUp(self):
        self.g = Grammar(grammar)
        self.gp = self.g.pospruned

    
    def test_pospruned(self):
        self.assertEqual(set(self.g.pospruned.rules),
        {
            Rule("S", (PospruningTag("NP"), PospruningTag("VP"))),
            Rule(PospruningTag("VP"), (PospruningTag("VP"), "PP")),
            Rule(PospruningTag("VP"), (PospruningTag("V"), PospruningTag("NP"))),
            Rule(PospruningTag("VP"), ("VP",)),
            Rule("PP", (PospruningTag("P"), PospruningTag("NP"))),
            Rule(PospruningTag("NP"), (PospruningTag("Det"), PospruningTag("N"))),
            Rule(PospruningTag("NP"), ("NP",)),
            Rule(PospruningTag("V"), ("V",)),
            Rule(PospruningTag("P"), ("P",)),
            Rule(PospruningTag("N"), ("N",)),
            Rule(PospruningTag("N"), ("N",)),
            Rule(PospruningTag("Det"), ("Det",))
        })

class TestGrammarUnary(TestCase):
    def setUp(self):
        self.g = Grammar(unary_grammar)
        self.gp = self.g.pospruned

    def test_pospruned(self):
        self.assertEqual(set(self.g.pospruned.rules),
        {
            Rule("S", (PospruningTag("NP"), "VP")),
            Rule("VP", (PospruningTag("V"),)),
            Rule(PospruningTag("NP"), ("NP",)),
            Rule(PospruningTag("V"), ("V",))
        })



if __name__ == '__main__':
    main()
