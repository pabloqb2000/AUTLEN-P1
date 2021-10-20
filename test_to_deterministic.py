"""Test evaluation of finite automaton to deterministic."""
import unittest

from automata.automaton_evaluator import FiniteAutomatonEvaluator
from automata.re_parser import REParser

from test_re_parser import TestREParser

class TestToDeterministic(TestREParser):
    """Test evaluation of finite automaton to deterministic."""

    def _create_evaluator(self, regex: str) -> FiniteAutomatonEvaluator:
        automaton = REParser().create_automaton(regex).to_deterministic()
        return FiniteAutomatonEvaluator(automaton)

if __name__ == "__main__":
    unittest.main()
