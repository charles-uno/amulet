import random

from . import io, state

MAX_STATES = 3e4

class TooManyStates(RuntimeError):
    pass

class GameStateManager(object):

    def __init__(self, name, draw=False):
        deck = io.load(name)
        self.turn = 1
        initial_state = state.GameState(deck=deck, turn=1, on_the_draw=draw)
        initial_state.draw(8 if draw else 7)
        self.states = {initial_state}

    def next_turn(self):
        self.turn += 1
        if any( x.done for x in self.states ):
            return
        states, new_states = self.states, set()
        while states:
            for state in states.pop().next_states():
                if state.done:
                    return state
                elif state.turn < self.turn:
                    states.add(state)
                else:
                    new_states.add(state)
            if len(states) + len(new_states) > MAX_STATES:
                raise TooManyStates
        self.states = new_states
        return None

    def done(self):
        done_states = [ x for x in self.states if x.done ]
        if done_states:
            return done_states.pop()
        else:
            return None

    def peek(self):
        state = sorted( (len(x.lines), x) for x in self.states )[-1][-1]
        state.report()
