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
        automaton_str = """
        Automaton:
            Symbols: 01

            q0
            qf final

            --> q0
            q0 -0-> qf
        """

        expected_str = """
        Automaton:
            Symbols: 01

            q0
            qf final
            empty

            --> q0
            q0 -0-> qf
            q0 -1-> empty
            qf -0-> empty
            qf -1-> empty
            empty -0-> empty
            empty -1-> empty
        """
        self._check_transform(automaton_str, expected_str)
        
    def test_case2(self):
        """
        Un caso representativo:
        AFD que reconoce cadenas
        con un número par de
        símbolos, y la cadena
        vacía. Se ha ampliado
        artificiosamente con
        estados adicionales. 
        """

        automaton_str = """
        Automaton:
            Symbols: 01

            q0 final
            q1
            q2 final
            q3
            q4 final
            q5

            --> q0
            q0 -0-> q1
            q0 -1-> q1
            q1 -0-> q2
            q1 -1-> q2
            q2 -0-> q3
            q2 -1-> q3
            q3 -0-> q4
            q3 -1-> q4
            q4 -0-> q5
            q4 -1-> q5
            q5 -0-> q0
            q5 -1-> q0
        """

        expected_str = """
        Automaton:
            Symbols: 01

            q0 final
            q1

            --> q0
            q0 -0-> q1
            q0 -1-> q1
            q1 -0-> q0
            q1 -1-> q0
        """
        self._check_transform(automaton_str, expected_str)

    def test_case3(self):
        """
        Un caso representativo:
        Se puede comprobar
        intuitivamente que los
        estados q1 y q3, y q2 y q4,
        son equivalentes entre sí.
        """

        automaton_str = """
        Automaton:
            Symbols: ab

            q0
            q1 final
            q2
            q3 final
            q4

            --> q0
            q0 -a-> q1
            q0 -b-> q3
            q1 -a-> q2
            q1 -b-> q1
            q2 -a-> q1
            q2 -b-> q2
            q3 -a-> q4
            q3 -b-> q3
            q4 -a-> q3
            q4 -b-> q4
        """

        expected_str = """
        Automaton:
            Symbols: ab

            q0
            q1 final
            q2

            --> q0
            q0 -a-> q1
            q0 -b-> q1
            q1 -a-> q2
            q1 -b-> q1
            q2 -a-> q1
            q2 -b-> q2
        """
        self._check_transform(automaton_str, expected_str)

    def test_case4(self):
        """
        Un caso representativo:
        Se puede comprobar
        intuitivamente que los
        estados A y B son
        equivalentes.
        """

        automaton_str = """
        Automaton:
            Symbols: abc

            A final
            B final
            C final
            D final
            E

            --> A
            A -a-> B
            A -b-> C
            A -c-> B
            B -a-> B
            B -b-> C
            B -c-> B
            C -a-> B
            C -b-> D
            C -c-> B
            D -a-> E
            D -b-> E
            D -c-> E
            E -a-> E
            E -b-> E
            E -c-> E
        """

        expected_str = """
        Automaton:
            Symbols: abc

            AB final
            C final
            D final
            E

            --> AB
            AB -a-> AB
            AB -b-> C
            AB -c-> AB
            C  -a-> AB
            C  -b-> D
            C  -c-> AB
            D  -a-> E
            D  -b-> E
            D  -c-> E
            E  -a-> E
            E  -b-> E
            E  -c-> E
        """
        self._check_transform(automaton_str, expected_str)

if __name__ == '__main__':
    unittest.main()