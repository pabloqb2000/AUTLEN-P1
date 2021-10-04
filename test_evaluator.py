"""Test evaluation of automatas."""
import unittest
from abc import ABC, abstractmethod
from typing import Optional, Type

from automata.automaton import FiniteAutomaton
from automata.automaton_evaluator import FiniteAutomatonEvaluator
from automata.utils import AutomataFormat


class TestEvaluatorBase(ABC, unittest.TestCase):
    """Base class for string acceptance tests."""

    automaton: FiniteAutomaton
    evaluator: FiniteAutomatonEvaluator

    @abstractmethod
    def _create_automata(self) -> FiniteAutomaton:
        pass

    def setUp(self) -> None:
        """Set up the tests."""
        self.automaton = self._create_automata()
        self.evaluator = FiniteAutomatonEvaluator(self.automaton)

    def _check_accept_body(
        self,
        string: str,
        should_accept: bool = True,
    ) -> None:
        accepted = self.evaluator.accepts(string)
        self.assertEqual(accepted, should_accept)

    def _check_accept(
        self,
        string: str,
        should_accept: bool = True,
        exception: Optional[Type[Exception]] = None,
    ) -> None:

        with self.subTest(string=string):
            if exception is None:
                self._check_accept_body(string, should_accept)
            else:
                with self.assertRaises(exception):
                    self._check_accept_body(string, should_accept)


class TestEvaluatorFixed(TestEvaluatorBase):
    """Test for a fixed string."""

    def _create_automata(self) -> FiniteAutomaton:

        description = """
        Automaton:
            Symbols: Helo

            Empty
            H
            He
            Hel
            Hell
            Hello final

            --> Empty
            Empty -H-> H
            H -e-> He
            He -l-> Hel
            Hel -l-> Hell
            Hell -o-> Hello
        """

        return AutomataFormat.read(description)

    def test_fixed(self) -> None:
        """Test for a fixed string."""
        self._check_accept("Hello", should_accept=True)
        self._check_accept("Helloo", should_accept=False)
        self._check_accept("Hell", should_accept=False)
        self._check_accept("llH", should_accept=False)
        self._check_accept("", should_accept=False)
        self._check_accept("Hella", exception=ValueError)
        self._check_accept("Helloa", exception=ValueError)


class TestEvaluatorLambdas(TestEvaluatorBase):
    """Test for a fixed string."""

    def _create_automata(self) -> FiniteAutomaton:

        description = """
        Automaton:
            Symbols:

            1
            2
            3
            4 final

            --> 1
            1 --> 2
            2 --> 3
            3 --> 4
        """

        return AutomataFormat.read(description)

    def test_lambda(self) -> None:
        """Test for a fixed string."""
        self._check_accept("", should_accept=True)
        self._check_accept("a", exception=ValueError)


class TestEvaluatorNumber(TestEvaluatorBase):
    """Test for a fixed string."""

    def _create_automata(self) -> FiniteAutomaton:

        description = """
        Automaton:
            Symbols: 01-.

            initial
            sign
            int final
            dot
            decimal final

            --> initial
            initial ---> sign
            initial --> sign
            sign -0-> int
            sign -1-> int
            int -0-> int
            int -1-> int
            int -.-> dot
            dot -0-> decimal
            dot -1-> decimal
            decimal -0-> decimal
            decimal -1-> decimal
        """

        return AutomataFormat.read(description)

    def test_number(self) -> None:
        """Test for a fixed string."""
        self._check_accept("0", should_accept=True)
        self._check_accept("0.0", should_accept=True)
        self._check_accept("0.1", should_accept=True)
        self._check_accept("1.0", should_accept=True)
        self._check_accept("-0", should_accept=True)
        self._check_accept("-0.0", should_accept=True)
        self._check_accept("-0.1", should_accept=True)
        self._check_accept("-1.0", should_accept=True)
        self._check_accept("-101.010", should_accept=True)
        self._check_accept("0.", should_accept=False)
        self._check_accept(".0", should_accept=False)
        self._check_accept("0.0.0", should_accept=False)
        self._check_accept("0-0.0", should_accept=False)


class TestEvaluatorCustom1(TestEvaluatorBase):
    """Test lambda cycles."""

    def _create_automata(self) -> FiniteAutomaton:

        description = """
        Automaton:
            Symbols: abc

            q0
            q1
            q2 final

            --> q0
            q0 --> q0
            q0 --> q1
            q1 --> q0
            q2 --> q1
            q1 -a-> q2
            q1 -b-> q2
        """

        return AutomataFormat.read(description)

    def test_custom1(self) -> None:
        """Test lambda cycles."""
        self._check_accept("", should_accept=False)
        self._check_accept("a", should_accept=True)
        self._check_accept("b", should_accept=True)
        self._check_accept("ab", should_accept=True)
        self._check_accept("aaabaabbaabbab", should_accept=True)
        self._check_accept("aaabaabcbabbab", should_accept=False)


class TestEvaluatorCustom2(TestEvaluatorBase):
    """Test lambda cycles."""

    def _create_automata(self) -> FiniteAutomaton:

        description = """
        Automaton:
            Symbols: abc

            q0 
            q1 final
            q2 

            --> q0
            q0 --> q0
            q0 --> q1
            q1 --> q0
            q2 --> q1
            q1 -a-> q2
            q1 -b-> q2
        """

        return AutomataFormat.read(description)

    def test_custom2(self) -> None:
        """Test lambda cycles."""
        self._check_accept("", should_accept=True)
        self._check_accept("a", should_accept=True)
        self._check_accept("b", should_accept=True)
        self._check_accept("ab", should_accept=True)
        self._check_accept("aaabaabbaabbab", should_accept=True)
        self._check_accept("aaabaabcbabbab", should_accept=False)


class TestEvaluatorCustom3(TestEvaluatorBase):
    """Test not repeated bs automata."""

    def _create_automata(self) -> FiniteAutomaton:

        description = """
        Automaton:
            Symbols: ab

            q0 final
            q1 
            q2 final

            --> q0
            q0 -b-> q1
            q0 -b-> q2
            q0 -a-> q0
            q1 -a-> q0
        """

        return AutomataFormat.read(description)

    def test_custom3(self) -> None:
        """Test not repeated bs automata."""
        self._check_accept("", should_accept=True)
        self._check_accept("a", should_accept=True)
        self._check_accept("b", should_accept=True)
        self._check_accept("ab", should_accept=True)
        self._check_accept("ba", should_accept=True)
        self._check_accept("bab", should_accept=True)
        self._check_accept("aba", should_accept=True)
        self._check_accept("ababaaab", should_accept=True)
        self._check_accept("bababaaab", should_accept=True)
        self._check_accept("baababaa", should_accept=True)
        self._check_accept("abaababaa", should_accept=True)
        self._check_accept("bb", should_accept=False)
        self._check_accept("bbabaaba", should_accept=False)
        self._check_accept("babbaaba", should_accept=False)
        self._check_accept("babaababb", should_accept=False)
        self._check_accept("babbaababb", should_accept=False)
        self._check_accept("bbabaababb", should_accept=False)


class TestEvaluatorCustom4(TestEvaluatorBase):
    """Test for (ab + bc)*a."""

    def _create_automata(self) -> FiniteAutomaton:

        description = """
        Automaton:
            Symbols: abc

            q0 
            q1 
            q2 
            q3 
            q4 
            q5 final

            --> q0
            q0 -a-> q1
            q1 -b-> q2
            q2 -a-> q5
            q0 -b-> q3
            q3 -c-> q4
            q4 -a-> q5
            q0 --> q2
            q2 --> q0
            q0 --> q4
            q4 --> q0
        """

        return AutomataFormat.read(description)

    def test_custom4(self) -> None:
        """Test for (ab + bc)*a."""
        self._check_accept("", should_accept=False)
        self._check_accept("a", should_accept=True)
        self._check_accept("aba", should_accept=True)
        self._check_accept("bca", should_accept=True)
        self._check_accept("abbca", should_accept=True)
        self._check_accept("bcaba", should_accept=True)
        self._check_accept("bcababbca", should_accept=True)
        self._check_accept("abbc", should_accept=False)
        self._check_accept("abca", should_accept=False)
        self._check_accept("abba", should_accept=False)
        self._check_accept("ab", should_accept=False)
        self._check_accept("bbca", should_accept=False)


if __name__ == '__main__':
    unittest.main()
