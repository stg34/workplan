# encoding: utf-8

import tempfile
import pathlib
from srclib.utils import execute_command
from srclib.view.dot.node import ViewDotNode
from srclib.view.dot.main_node import ViewDotMainNode
from srclib.view.dot.title import ViewDotTitle
from srclib.view.dot.edge import ViewDotEdge


class ViewDotBuilder:
    def __init__(self, task, reverse, scheme, colorizer, dir, verbose):
        self.task = task
        self.comments_graph = task.graph
        self.reverse = reverse
        self.scheme = scheme
        self.colorizer = colorizer
        self.dir = dir
        self.content = ''
        self.verbose = verbose

    def build_edges(self, dot_nodes):
        for id in dot_nodes:
            dep_ids = self.comments_graph.outgoing_ids(id)
            penwidth = 2

            for dep_id in dep_ids:
                edge = ViewDotEdge(self.scheme, self.comments_graph, dot_nodes[id], dot_nodes[dep_id])

                color = edge.color
                font_color = edge.font_color
                label = edge.label
                style = edge.style
                attrs = f'[penwidth="{penwidth}" style="{style}" color="{color}" fontcolor="{font_color}" label="{label}"]'
                self.content += f'"{id}"->"{dep_id}" {attrs}\n'

    def build_nodes(self):
        dot_nodes = {}

        node = ViewDotTitle(self.task, self.scheme)
        self.content += f'label=<{node.label}>\n'

        for comment in self.comments_graph.comments:
            if comment.is_main:
                node = ViewDotMainNode(self.comments_graph, comment, self.scheme)
            else:
                # TODO: PL: Передать в ViewDotNode колоризатор
                # ID: srclib/view/dot/builder.py:47
                # DEP: srclib/app/graph_plan.py:54
                # TIME: 0.1
                # COMPL: 100
                node = ViewDotNode(self.comments_graph, comment, self.scheme, self.colorizer)

            self.content += node.content
            dot_nodes[comment.id] = node
            self.content += '\n'

        return dot_nodes

    @property
    def edge_dir(self):
        if self.reverse:
            return 'back'

        return 'forward'

    @property
    def rankdir(self):
        if self.dir == 'lr':
            return 'LR'

        return 'TB'

    def build(self):
        self.content = 'digraph {\n'
        self.content += f'fontname="{self.scheme.font_name}"\n'
        self.content += f'bgcolor="{self.scheme.canvas_color}"\n'
        self.content += f'fontcolor="{self.scheme.font_primary_color(0)}"\n'
        self.content += f'dpi={self.scheme.dpi}\n'
        self.content += f'rankdir="{self.rankdir}"\n'
        self.content += 'pad="0.5,0.5"\n'
        self.content += 'labelloc="t"\n'
        self.content += f'edge [dir="{self.edge_dir}" fontname="{self.scheme.font_name}"]\n'
        self.content += f'node [shape="plain" nojustify=true fontname="{self.scheme.font_name}"]\n'

        dot_nodes = self.build_nodes()
        self.build_edges(dot_nodes)

        self.content += '}\n'

    def write(self, file_name):
        if self.verbose:
            pathlib.Path(f'{file_name}.dot').write_text(self.content)

        with tempfile.NamedTemporaryFile('w+t') as tf:
            tf.write(self.content)
            tf.flush()

            execute_command(f'dot -T png -o{file_name} {tf.name}', self.verbose)

        return file_name  # TODO: check errors
