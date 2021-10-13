"""Automaton implementation."""
from typing import Collection, Set

from automata.interfaces import (
    AbstractFiniteAutomaton,
    AbstractState,
    AbstractTransition,
)


class State(AbstractState):
    """State of an automaton."""

    # You can add new attributes and methods that you think that make your
    # task easier, but you cannot change the constructor interface.


class Transition(AbstractTransition[State]):
    """Transition of an automaton."""

    # You can add new attributes and methods that you think that make your
    # task easier, but you cannot change the constructor interface.


class FiniteAutomaton(
    AbstractFiniteAutomaton[State, Transition],
):
    """Automaton."""

    def __init__(
        self,
        *,
        initial_state: State,
        states: Collection[State],
        symbols: Collection[str],
        transitions: Collection[Transition],
    ) -> None:
        super().__init__(
            initial_state=initial_state,
            states=states,
            symbols=symbols,
            transitions=transitions,
        )

        # Add here additional initialization code.
        # Do not change the constructor interface.

    @property
    def final_state(self):
        return self.states[-1]

    def get_closure(self, states: Set[State]) -> Set[State]:
        states_to_complete = states
        closure = states.copy()

        while True:
            new_states = set()

            for state in states_to_complete:
                for transition in self.transitions:
                    if state == transition.initial_state and not transition.symbol:
                        new_states.add(transition.final_state)

            if new_states.issubset(closure):
                break
            closure.update(new_states)
            states_to_complete = new_states
        
        return closure

    def to_deterministic(
        self,
    ) -> "FiniteAutomaton":
        raise NotImplementedError("This method must be implemented.")

    def to_minimized(
        self,
    ) -> "FiniteAutomaton":
        raise NotImplementedError("This method must be implemented.")
