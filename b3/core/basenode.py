import b3
import pydot as pd
import uuid

__all__ = ['BaseNode']

class BaseNode(object):
    category = None
    title = None
    description = None

    def __init__(self):
        self.id = str(uuid.uuid1())
        self.title = self.title or self.__class__.__name__
        self.description = self.description or ''
        self.parameters = {}
        self.properties = {}
        self._graph_node = None

    def __str__(self):
        return '%s' % self.__class__.__name__

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def graph_node(self):
        if self._graph_node is None:
            self._graph_node = pd.Node(
                    self.id,
                    label=str(self),
                    shape='ellipse',
                    style='filled',
                    fillcolor='gray',
                    fontsize=11,
                    fontcolor='black')
        return self._graph_node

    def graph_edge(self, other):
        return pd.Edge(
                self.graph_node.get_name(),
                other.graph_node.get_name())

    def _execute(self, tick):
        self._enter(tick)

        if (not tick.blackboard.get('is_open', tick.tree.id, self.id)):
            self._open(tick)

        status = self._tick(tick)

        if (status != b3.RUNNING):
            self._close(tick)

        self._exit(tick)

        return status

    def _enter(self, tick):
        tick._enter_node(self)
        self.enter(tick)

    def _open(self, tick):
        tick._open_node(self)
        tick.blackboard.set('is_open', True, tick.tree.id, self.id)
        self.open(tick)

        self.graph_node.set_fillcolor('green')

    def _tick(self, tick):
        tick._tick_node(self)
        return self.tick(tick)

    def _close(self, tick):
        tick._close_node(self)
        tick.blackboard.set('is_open', False, tick.tree.id, self.id)
        self.close(tick)

        self.graph_node.set_fillcolor('gray')

    def _exit(self, tick):
        tick._exit_node(self)
        self.exit(tick)

    def enter(self, tick): pass
    def open(self, tick): pass
    def tick(self, tick): pass
    def close(self, tick): pass
    def exit(self, tick): pass
