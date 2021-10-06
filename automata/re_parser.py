"""Conversion from regex to automata."""
from automata.automaton import FiniteAutomaton, State, Transition
from automata.re_parser_interfaces import AbstractREParser


class REParser(AbstractREParser):
    """Class for processing regular expressions in Kleene's syntax."""

    def _create_automaton_empty(
        self,
    ) -> FiniteAutomaton:
        initial_state = State(f"q{self.state_counter}")
        final_state = State(f"q{self.state_counter+1}", is_final=True)
        self.state_counter += 2

        return FiniteAutomaton(
            initial_state=initial_state,
            states=[initial_state, final_state],
            symbols=[],
            transitions=[]
        )

    def _create_automaton_lambda(
        self,
    ) -> FiniteAutomaton:
        initial_state = State(f"q{self.state_counter}", is_final=True)
        self.state_counter += 1

        return FiniteAutomaton(
            initial_state=initial_state,
            states=[initial_state],
            symbols=[],
            transitions=[]
        )

    def _create_automaton_symbol(
        self,
        symbol: str,
    ) -> FiniteAutomaton:
        initial_state = State(f"q{self.state_counter}")
        final_state = State(f"q{self.state_counter+1}", is_final=True)
        self.state_counter += 2

        transition = Transition(initial_state, symbol, final_state)

        return FiniteAutomaton(
            initial_state=initial_state,
            states=[initial_state, final_state],
            symbols=[symbol],
            transitions=[transition]
        )

    def _create_automaton_star(
        self,
        automaton: FiniteAutomaton,
    ) -> FiniteAutomaton:
        initial_state = State(f"q{self.state_counter}")
        final_state = State(f"q{self.state_counter+1}", is_final=True)
        self.state_counter += 2

        automaton.final_state.is_final = False

        transitions = [Transition(initial_state, None, automaton.initial_state),
                        Transition(automaton.final_state, None, final_state),
                        Transition(automaton.final_state, None, automaton.initial_state),
                        Transition(initial_state, None, final_state)]
                        
        return FiniteAutomaton(
            initial_state=initial_state, 
            states=[initial_state] + list(automaton.states) + [final_state],
            symbols=automaton.symbols, 
            transitions=transitions + list(automaton.transitions)
        )

    def _create_automaton_union(
        self,
        automaton1: FiniteAutomaton,
        automaton2: FiniteAutomaton,
    ) -> FiniteAutomaton:
        initial_state = State(f"q{self.state_counter}")
        final_state = State(f"q{self.state_counter+1}", is_final=True)
        self.state_counter += 2

        automaton1.final_state.is_final = False
        automaton2.final_state.is_final = False

        new_transitions = [
            Transition(initial_state, None, automaton1.initial_state),
            Transition(initial_state, None, automaton2.initial_state),

            Transition(automaton1.final_state, None, final_state),
            Transition(automaton2.final_state, None, final_state),
        ]

        return FiniteAutomaton(
            initial_state=automaton1.initial_state,
            states=[initial_state] + list(automaton1.states) + list(automaton2.states) + [final_state],
            symbols=set(automaton1.symbols) | set(automaton2.symbols),
            transitions=list(automaton1.transitions) + new_transitions + list(automaton2.transitions)
        )


    def _create_automaton_concat(
        self,
        automaton1: FiniteAutomaton,
        automaton2: FiniteAutomaton,
    ) -> FiniteAutomaton:
        automaton1.final_state.is_final = False
        transition: Transition = Transition(automaton1.final_state, None, automaton2.initial_state)

        return FiniteAutomaton(
            initial_state=automaton1.initial_state,
            states=list(automaton1.states) + list(automaton2.states),
            symbols=set(automaton1.symbols) | set(automaton2.symbols),
            transitions=list(automaton1.transitions) + [transition] + list(automaton2.transitions)
        )
