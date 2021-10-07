"""Test evaluation of regex parser."""
import unittest

from automata.automaton_evaluator import FiniteAutomatonEvaluator
from automata.re_parser import REParser


class TestREParser(unittest.TestCase):
    """Tests for regex parser."""

    def _create_evaluator(self, regex: str) -> FiniteAutomatonEvaluator:
        automaton = REParser().create_automaton(regex)
        return FiniteAutomatonEvaluator(automaton)

    def _check_accept(
        self,
        evaluator: FiniteAutomatonEvaluator,
        string: str,
        should_accept: bool = True,
    ) -> None:
        with self.subTest(string=string):
            accepted = evaluator.accepts(string)
            self.assertEqual(accepted, should_accept)

    def test_fixed(self) -> None:
        """Test fixed regex."""
        evaluator = self._create_evaluator("H.e.l.l.o")

        self._check_accept(evaluator, "Hello", should_accept=True)
        self._check_accept(evaluator, "Helloo", should_accept=False)
        self._check_accept(evaluator, "Hell", should_accept=False)
        self._check_accept(evaluator, "llH", should_accept=False)
        self._check_accept(evaluator, "", should_accept=False)

    def test_star(self) -> None:
        """Test Kleene star."""
        evaluator = self._create_evaluator("a*.b*")

        self._check_accept(evaluator, "", should_accept=True)
        self._check_accept(evaluator, "a", should_accept=True)
        self._check_accept(evaluator, "b", should_accept=True)
        self._check_accept(evaluator, "aa", should_accept=True)
        self._check_accept(evaluator, "bb", should_accept=True)
        self._check_accept(evaluator, "ab", should_accept=True)
        self._check_accept(evaluator, "ba", should_accept=False)
        self._check_accept(evaluator, "aab", should_accept=True)
        self._check_accept(evaluator, "abb", should_accept=True)
        self._check_accept(evaluator, "aba", should_accept=False)
        self._check_accept(evaluator, "bab", should_accept=False)

    def test_or(self) -> None:
        """Test Kleene star."""
        evaluator = self._create_evaluator("(a+b)*")

        self._check_accept(evaluator, "", should_accept=True)
        self._check_accept(evaluator, "a", should_accept=True)
        self._check_accept(evaluator, "b", should_accept=True)
        self._check_accept(evaluator, "aa", should_accept=True)
        self._check_accept(evaluator, "bb", should_accept=True)
        self._check_accept(evaluator, "ab", should_accept=True)
        self._check_accept(evaluator, "ba", should_accept=True)
        self._check_accept(evaluator, "aab", should_accept=True)
        self._check_accept(evaluator, "abb", should_accept=True)
        self._check_accept(evaluator, "aba", should_accept=True)
        self._check_accept(evaluator, "bab", should_accept=True)

    def test_number(self) -> None:
        """Test number expression."""
        num = "(0+1+2+3+4+5+6+7+8+9)"
        evaluator = self._create_evaluator(
            f"({num}.{num}*.,.{num}*)+{num}*",
        )

        self._check_accept(evaluator, ",", should_accept=False)
        self._check_accept(evaluator, "1,7", should_accept=True)
        self._check_accept(evaluator, "25,73", should_accept=True)
        self._check_accept(evaluator, "5027", should_accept=True)
        self._check_accept(evaluator, ",13", should_accept=False)
        self._check_accept(evaluator, "13,", should_accept=True)
        self._check_accept(evaluator, "3,7,12", should_accept=False)

    def test_lambda(self) -> None:
        """Test lambda use."""
        evaluator = self._create_evaluator(
            "λ+(a.b.λ)+(a.a.b.(b.a+λ))",
        )

        self._check_accept(evaluator, "", should_accept=True)
        self._check_accept(evaluator, "ab", should_accept=True)
        self._check_accept(evaluator, "aab", should_accept=True)
        self._check_accept(evaluator, "aabba", should_accept=True)
        self._check_accept(evaluator, "aabb", should_accept=False)
        self._check_accept(evaluator, "abba", should_accept=False)
        self._check_accept(evaluator, "aaba", should_accept=False)
        self._check_accept(evaluator, "abb", should_accept=False)
        self._check_accept(evaluator, "a", should_accept=False)
        self._check_accept(evaluator, "b", should_accept=False)

    def test_non_repeated(self) -> None:
        """Test non repeated bs."""
        evaluator = self._create_evaluator(
            "((b.a)+a)*.(b+λ)",
        )

        self._check_accept(evaluator, "", should_accept=True)
        self._check_accept(evaluator, "a", should_accept=True)
        self._check_accept(evaluator, "b", should_accept=True)
        self._check_accept(evaluator, "aa", should_accept=True)
        self._check_accept(evaluator, "ba", should_accept=True)
        self._check_accept(evaluator, "ab", should_accept=True)
        self._check_accept(evaluator, "ba", should_accept=True)
        self._check_accept(evaluator, "aaa", should_accept=True)
        self._check_accept(evaluator, "baa", should_accept=True)
        self._check_accept(evaluator, "aba", should_accept=True)
        self._check_accept(evaluator, "aab", should_accept=True)
        self._check_accept(evaluator, "bab", should_accept=True)
        self._check_accept(evaluator, "abab", should_accept=True)
        self._check_accept(evaluator, "baba", should_accept=True)
        self._check_accept(evaluator, "baab", should_accept=True)
        self._check_accept(evaluator, "bb", should_accept=False)
        self._check_accept(evaluator, "bbb", should_accept=False)
        self._check_accept(evaluator, "bba", should_accept=False)
        self._check_accept(evaluator, "abb", should_accept=False)
        self._check_accept(evaluator, "bbab", should_accept=False)
        self._check_accept(evaluator, "babb", should_accept=False)
        self._check_accept(evaluator, "abba", should_accept=False)


if __name__ == "__main__":
    unittest.main()
