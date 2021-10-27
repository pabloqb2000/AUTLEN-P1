"""Test evaluation of finite automaton to minimized."""
import unittest
from abc import ABC

from automata.automaton_evaluator import FiniteAutomatonEvaluator
from automata.automaton import FiniteAutomaton
from automata.utils import AutomataFormat, deterministic_automata_isomorphism, write_dot, is_deterministic
from automata.re_parser import REParser
from test_re_parser import TestREParser


class ReTest(TestREParser):
    """Test that the transormed automatas have the same behaviour as the non transformed ones."""

    def _create_evaluator(self, regex: str) -> FiniteAutomatonEvaluator:
        automaton = REParser().create_automaton(regex).to_deterministic().to_minimized()
        if not is_deterministic(automaton):
            raise ValueError("Automaton is not deterministic") 
        return FiniteAutomatonEvaluator(automaton)

'''
class TestTransform(ABC, unittest.TestCase):
    """Base class for string acceptance tests."""

    def _check_transform(
        self,
        automaton_str: str,
        expected_str: str,
    ) -> None:
        """Test that the transformed automaton is as the expected one."""
        automaton = AutomataFormat.read(automaton_str)
        expected = AutomataFormat.read(expected_str)
        transformed = automaton.to_deterministic().to_minimized()

        equiv_map = deterministic_automata_isomorphism(
            transformed,
            expected,
        )

        self.assertTrue(equiv_map is not None)

    def test_case1(self):
        pass'''
        
if __name__ == '__main__':
    unittest.main()