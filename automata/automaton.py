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

            for transition in self.transitions:
                if transition.initial_state in states_to_complete and not transition.symbol:
                    new_states.add(transition.final_state)

            if new_states.issubset(closure):
                break
            states_to_complete = new_states - closure
            closure.update(new_states)
        
        return closure

    def state_from_state_set(self, states_set: Set[State]) -> State:
        if not states_set:
            return State("empty")
        return State(
            name="".join([state.name for state in states_set]),
            is_final=any(state.is_final for state in states_set)
        )

    def to_deterministic(
        self,
    ) -> "FiniteAutomaton":
        new_transitions = set()
        new_states = set()
        initial_state_closure = self.get_closure({self.initial_state})
        initial_state = self.state_from_state_set(initial_state_closure)
        # sink_state = State("empty")
        # new_states.add(sink_state)
        states_to_evaluate = [(
            initial_state_closure,
            initial_state
        )]

        while states_to_evaluate:
            state_set, state = states_to_evaluate.pop()
            new_states.add(state)

            for symbol in set(self.symbols):
                reachable_states = {
                    transition.final_state
                    for transition in self.transitions
                    if transition.symbol == symbol and \
                        transition.initial_state in state_set
                }

                reachable_states = self.get_closure(reachable_states)
                new_state = self.state_from_state_set(reachable_states)
                new_state_tupple = (
                    reachable_states,
                    new_state
                )
                if not new_state in new_states:
                    states_to_evaluate.append(new_state_tupple)

                new_transitions.add(Transition(
                    state, symbol, new_state
                ))
        
        # for symbol in self.symbols:
        #     new_transitions.add(Transition(
        #         sink_state, symbol, sink_state
        #     ))

        return FiniteAutomaton(
            initial_state=initial_state,
            states=new_states,
            symbols=self.symbols,
            transitions=new_transitions
        )

    def to_minimized(
        self,
    ) -> "FiniteAutomaton":
        raise NotImplementedError("This method must be implemented.")
