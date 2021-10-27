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

        return FiniteAutomaton(
            initial_state=initial_state,
            states=new_states,
            symbols=self.symbols,
            transitions=new_transitions
        )

    def eliminate_unreachable_states(self) -> "FiniteAutomaton":
        reachable_states = []
        reachable_stack = [self.initial_state]
        while reachable_stack:
            state = reachable_stack.pop()
            reachable_states.append(state)
            for transition in self.transitions:
                if transition.initial_state == state:
                    if not transition.final_state in reachable_states and not transition.final_state in reachable_stack:
                        reachable_stack.append(transition.final_state)

        return FiniteAutomaton(
            initial_state=self.initial_state,
            states=set(reachable_states),
            symbols=self.symbols,
            transitions=[t for t in self.transitions if t.final_state in reachable_states and t.initial_state in reachable_states]
        )

    def to_minimized(
        self,
    ) -> "FiniteAutomaton":
        automaton = self.eliminate_unreachable_states()
        
        states = list(automaton.states)
        states_idx = {state:i for i, state in enumerate(states)}
        list_1 = [
            1 if state.is_final else 0
            for state in states
        ]
        
        for _ in range(len(automaton.states) - 2):
            i, index = 0, 0
            new_idx = max(list_1) + 1
            list_2 = [None for _ in automaton.states]

            while i < len(list_2):
                s1 = states[i]
                state_old_class, state_new_class = list_1[i], list_2[i]
                
                if state_new_class is None:
                    if state_old_class >= index:
                        list_2[i] = state_old_class
                        index += 1
                    else:
                        list_2[i] = new_idx
                        new_idx += 1
                    
                    for j in range(i+1, len(list_1)):
                        s2 = states[j]
                        s1_trans = {t.symbol: t.final_state for t in automaton.transitions if t.initial_state == s1}
                        s2_trans = {t.symbol: t.final_state for t in automaton.transitions if t.initial_state == s2}
                        equiv = True
                        for symbol in s1_trans:
                            f1_idx = states_idx[s1_trans[symbol]]
                            f2_idx = states_idx[s2_trans[symbol]]
                            if list_1[f1_idx] != list_2[f2_idx]:
                                equiv = False
                        
                        if equiv:
                            list_2[j] = list_2[i]
                i += 1
            
            if list_1 == list_2:
                break
            list_1 = list_2

        new_states = []
        classes = set()
        
        for i in range(len(list_1)):
            if list_1[i] in classes:
                pass
            else:
                classes.add(list_1[i])
                new_states.append(states[i])
            

        return FiniteAutomaton(
            initial_state=self.initial_state,
            states=new_states,
            symbols=self.symbols,
            transitions=[t for t in self.transitions if t.final_state in new_states and t.initial_state in new_states]
        )
    