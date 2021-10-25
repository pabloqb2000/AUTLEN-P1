"""Test evaluation of finite automaton to deterministic."""
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
        automaton = REParser().create_automaton(regex).to_deterministic()
        if not is_deterministic(automaton):
            raise ValueError("Automaton is not deterministic") 
        return FiniteAutomatonEvaluator(automaton)


class TestTransform(ABC, unittest.TestCase):
    """Base class for string acceptance tests."""

    def _check_transform(
        self,
        automaton: FiniteAutomaton,
        expected: FiniteAutomaton,
    ) -> None:
        """Test that the transformed automaton is as the expected one."""
        transformed = automaton.to_deterministic()
        equiv_map = deterministic_automata_isomorphism(
            transformed,
            expected,
        )

        self.assertTrue(equiv_map is not None)

    def test_case1(self) -> None:
        """Test Case 1."""
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

        automaton = AutomataFormat.read(automaton_str)
        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)

    def test_case2(self) -> None:
        """Un caso representativo:  
        AF que reconoce un número 
        decimal con signo opcional."""
        automaton_str = """
        Automaton:
            Symbols: 0123456789+-.

            q0
            q1
            q2
            q3
            q4
            q5 final

            -->q0
            q0 -+-> q1
            q0 ---> q1
            q0 --> q1
            q1 -0-> q1
            q1 -1-> q1
            q1 -2-> q1
            q1 -3-> q1
            q1 -4-> q1
            q1 -5-> q1
            q1 -6-> q1
            q1 -7-> q1
            q1 -8-> q1
            q1 -9-> q1          
            q1 -0-> q4
            q1 -1-> q4
            q1 -2-> q4
            q1 -3-> q4
            q1 -4-> q4
            q1 -5-> q4
            q1 -6-> q4
            q1 -7-> q4
            q1 -8-> q4
            q1 -9-> q4
            q1 -.-> q2
            q2 -0-> q3
            q2 -1-> q3
            q2 -2-> q3
            q2 -3-> q3
            q2 -4-> q3
            q2 -5-> q3
            q2 -6-> q3
            q2 -7-> q3
            q2 -8-> q3
            q2 -9-> q3
            q4 -.-> q3
            q3 -0-> q3
            q3 -1-> q3
            q3 -2-> q3
            q3 -3-> q3
            q3 -4-> q3
            q3 -5-> q3
            q3 -6-> q3
            q3 -7-> q3
            q3 -8-> q3
            q3 -9-> q3
            q3 --> q5
        """

        expected_str = """
        Automaton:
            Symbols: 0123456789+-.

            q0
            q1
            q2
            q3
            q4 final
            q5 final
            empty

            --> q0
            q0 -+-> q1
            q0 ---> q1
            q0 -0-> q2
            q0 -1-> q2
            q0 -2-> q2
            q0 -3-> q2
            q0 -4-> q2
            q0 -5-> q2
            q0 -6-> q2
            q0 -7-> q2
            q0 -8-> q2
            q0 -9-> q2
            q0 -.-> q3
            q1 -+-> empty
            q1 ---> empty
            q1 -0-> q2
            q1 -1-> q2
            q1 -2-> q2
            q1 -3-> q2
            q1 -4-> q2
            q1 -5-> q2
            q1 -6-> q2
            q1 -7-> q2
            q1 -8-> q2
            q1 -9-> q2
            q1 -.-> q3
            q2 -+-> empty
            q2 ---> empty
            q2 -0-> q2
            q2 -1-> q2
            q2 -2-> q2
            q2 -3-> q2
            q2 -4-> q2
            q2 -5-> q2
            q2 -6-> q2
            q2 -7-> q2
            q2 -8-> q2
            q2 -9-> q2
            q2 -.-> q4
            q3 -+-> empty
            q3 ---> empty
            q3 -0-> q5
            q3 -1-> q5
            q3 -2-> q5
            q3 -3-> q5
            q3 -4-> q5
            q3 -5-> q5
            q3 -6-> q5
            q3 -7-> q5
            q3 -8-> q5
            q3 -9-> q5
            q3 -.-> empty
            q4 -+-> empty
            q4 ---> empty
            q4 -0-> q5
            q4 -1-> q5
            q4 -2-> q5
            q4 -3-> q5
            q4 -4-> q5
            q4 -5-> q5
            q4 -6-> q5
            q4 -7-> q5
            q4 -8-> q5
            q4 -9-> q5
            q4 -.-> empty
            q5 -+-> empty
            q5 ---> empty
            q5 -0-> q5
            q5 -1-> q5
            q5 -2-> q5
            q5 -3-> q5
            q5 -4-> q5
            q5 -5-> q5
            q5 -6-> q5
            q5 -7-> q5
            q5 -8-> q5
            q5 -9-> q5
            q5 -.-> empty
            empty -+-> empty
            empty ---> empty
            empty -0-> empty
            empty -1-> empty
            empty -2-> empty
            empty -3-> empty
            empty -4-> empty
            empty -5-> empty
            empty -6-> empty
            empty -7-> empty
            empty -8-> empty
            empty -9-> empty
            empty -.-> empty

        """

        automaton = AutomataFormat.read(automaton_str)
        expected = AutomataFormat.read(expected_str)

        self._check_transform(automaton, expected)
        
    def test_case3(self) -> None:
        """Un caso representativo:  
        AF que reconoce las cadenas 
        “1”, “01”, y “101”, 
        artificiosamente ampliado con 
        transiciones lambda.
        """ 

        automaton_str = """
        Automaton:
            Symbols: 01

            q0
            q1
            q2
            q3
            q4
            q5
            q6 final
            q7

            -->q0
            q0 --> q1
            q0 --> q2
            q1 -1-> q5
            q1 -1-> q3
            q2 -0-> q4
            q4 -1-> q6
            q5 --> q7
            q5 -0-> q4
            q5 -0-> q3
            q7 --> q6
        """

        expected_str = """
        Automaton:
            Symbols: 01

            q0
            q1
            q2 final
            q3
            q4 final
            empty

            -->q0
            q0 -0-> q1
            q0 -1-> q4
            q1 -0-> empty
            q1 -1-> q2
            q2 -0-> empty
            q2 -1-> empty
            q3 -0-> empty
            q3 -1-> q2
            q4 -0-> q3
            q4 -1-> empty
            empty -0-> empty
            empty -1-> empty
        """
        
        automaton = AutomataFormat.read(automaton_str)
        expected = AutomataFormat.read(expected_str)
        self._check_transform(automaton, expected)

    def test_case4(self) -> None:
        """Test Case 4.
            Un caso representativo:
            AF que reconoce las cadenas
            acabadas en “11”. El AFD
            resultante mantiene el
            número de estados.
        """
        automaton_str = """
        Automaton:
            Symbols: 01

            q0
            q1
            qf final

            --> q0
            q0 -0-> q0
            q0 -1-> q0
            q0 -1-> q1
            q1 -1-> qf
        """

        expected_str = """
        Automaton:
            Symbols: 01

            q0
            q0q1
            q0q1qf final

            --> q0
            q0 -0-> q0
            q0 -1-> q0q1
            q0q1 -0-> q0
            q0q1 -1-> q0q1qf
            q0q1qf -0-> q0
            q0q1qf -1-> q0q1qf
        """

        automaton = AutomataFormat.read(automaton_str)
        expected = AutomataFormat.read(expected_str)
        self._check_transform(automaton, expected)

    def test_case5(self) -> None:
        automaton_str = """
        Automaton:
            Symbols: abc

            q0
            q1
            q2
            q3
            q4
            q5
            q6
            q7
            qf final

            --> q0
            q0 --> q1
            q0 --> qf
            q1 --> q2
            q1 --> q5
            q2 -a-> q3
            q3 -b-> q4
            q4 --> q7
            q5 -c-> q6
            q6 --> q7
            q7 --> q1
            q7 --> qf
        """

        expected_str = """
        Automaton:
            Symbols: abc

            q0 final
            q1 final
            q2 final
            q3
            empty

            --> q0
            q0 -a-> q3
            q0 -b-> empty
            q0 -c-> q1
            q1 -a-> q3
            q1 -b-> empty
            q1 -c-> q1
            q2 -a-> q3
            q2 -b-> empty
            q2 -c-> q1
            q3 -a-> empty
            q3 -b-> q2
            q3 -c-> empty
            empty -a-> empty
            empty -b-> empty
            empty -c-> empty
        """

        automaton = AutomataFormat.read(automaton_str)
        expected = AutomataFormat.read(expected_str)
        self._check_transform(automaton, expected)
        
if __name__ == '__main__':
    unittest.main()
