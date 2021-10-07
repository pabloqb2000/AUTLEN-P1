"""Evaluation of automata."""
from typing import Set

from automata.automaton import FiniteAutomaton, State
from automata.interfaces import AbstractFiniteAutomatonEvaluator


class FiniteAutomatonEvaluator(
    AbstractFiniteAutomatonEvaluator[FiniteAutomaton, State],
):
    """Evaluator of an automaton."""

    def process_symbol(self, symbol: str) -> None:
        new_states = set()

        if symbol not in self.automaton.symbols and symbol:
            raise ValueError(f"Symbol {symbol} is not a valid symbol {self.automaton.symbols}")

        for state in self.current_states:
            for transition in self.automaton.transitions:
                if state == transition.initial_state and symbol == transition.symbol and symbol:
                    new_states.add(transition.final_state)

        self._complete_lambdas(new_states)
        self.current_states = new_states

    def _complete_lambdas(self, set_to_complete: Set[State]) -> None:
        completed_states = set_to_complete

        while True:
            new_states = set()

            for state in completed_states:
                for transition in self.automaton.transitions:
                    if state == transition.initial_state and not transition.symbol:
                        new_states.add(transition.final_state)

            if new_states.issubset(set_to_complete):
                break
            set_to_complete.update(new_states)
            completed_states = new_states

    def is_accepting(self) -> bool:
        return any(state.is_final for state in self.current_states)

