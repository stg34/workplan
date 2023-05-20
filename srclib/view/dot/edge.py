# encoding: utf-8

import math
from srclib.presenter.edge_presenter import EdgePresenter
from srclib.utils import rgb_to_hex
from srclib.utils import hex_to_rgb


class ViewDotEdge:
    def __init__(self, scheme, comments_graph, src, dst) -> None:
        self.scheme = scheme
        self.comments_graph = comments_graph
        self.src = src
        self.dst = dst
        self.edge = EdgePresenter(self.comments_graph, src.comment, dst.comment)

    @property
    def font_color(self):
        if self.comments_graph.is_edge_in_loop(self.src.comment, self.dst.comment):
            return self.scheme.line_error_color(0)

        return self.scheme.font_primary_color(0)

    @property
    def style(self):
        if self.comments_graph.is_edge_in_loop(self.src.comment, self.dst.comment):
            return 'solid'

        if self.comments_graph.is_edge_in_tree(self.src.comment, self.dst.comment):
            return 'solid'

        return 'dotted'

    @property
    def color(self):
        if self.comments_graph.is_edge_in_loop(self.src.comment, self.dst.comment):
            return self.scheme.line_error_color(0)

        src = self.src.border_color
        dst = self.dst.border_color

        if src == dst:
            return src

        src_rgb = hex_to_rgb(src)
        dst_rgb = hex_to_rgb(dst)
        res = [None, None, None]
        d = []
        for i in range(3):
            d.append(dst_rgb[i] - src_rgb[i])

        N = 10

        color_list = [f'{src};{1/N}']

        for n in range(1, N):
            for i in range(3):
                res[i] = math.ceil(src_rgb[i] + d[i] / (N - 1) * n)

            color_list.append(f'{rgb_to_hex(res)};{1/N}')

        return ':'.join(color_list)

    @property
    def label(self):
        return self.edge.label
