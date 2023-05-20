# encoding: utf-8

from srclib.utils import setup_i18n

_ = setup_i18n('..', 'messages')


class EdgePresenter():
    def __init__(self, graph, src_comment, dst_comment):
        self.graph = graph
        self.src_comment = src_comment
        self.dst_comment = dst_comment

    @property
    def loop_label(self):
        return _('LOOP')

    @property
    def label(self):
        if self.graph.is_edge_in_loop(self.src_comment, self.dst_comment):
            return self.loop_label

        dependencies = self.graph.outgoing(self.src_comment.id)
        idx = dependencies.index(self.dst_comment)

        tree_deps_count = len(list(filter(lambda d: self.graph.is_edge_in_tree(self.src_comment, d), dependencies)))

        if tree_deps_count > 1:
            label = idx + 1
        else:
            label = ''

        return label
