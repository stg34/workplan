# encoding: utf-8

import pathlib
import math
import subprocess
import tempfile
import matplotlib.colors


def hex_to_rgb(hex):
    return [int(hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)]


def rgb_to_hex(rgb):
    return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'


def execute_command(command):
    res = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="UTF8")

    if res.returncode != 0:
        print(command, res.stdout, res.stderr)
        return


def hsv2rgb(h, s, v):
    c = matplotlib.colors.hsv_to_rgb([h % 1, s, v])
    return matplotlib.colors.rgb2hex(c)


d = 0.094
s = 0.0

s0 = 0.9
s1 = 0.5
s2 = 0.2

v0 = 0.8
v1 = 0.85
v2 = 0.95

COLORS_LIGHT = {
        'canvas_color': hsv2rgb(0, 0, 0.96),

        'node_background_color': {
            0: hsv2rgb(0, 0, 0.94),
            1: hsv2rgb(0, 0, 0.96),
            2: hsv2rgb(0, 0, 0.96),
        },
        'font_color_1': {
            0: hsv2rgb(1, 0, 0.3),
            1: hsv2rgb(1, 0, 0.5),
            2: hsv2rgb(1, 0, 0.8),
        },
        'font_color_2': {
            0: hsv2rgb(s + d, s0, 0.7),
            1: hsv2rgb(s + d, s1, 0.8),
            2: hsv2rgb(s + d, s2, 0.9),
        },
        'error_color': {
            0: hsv2rgb(s, s0, v0),
            1: hsv2rgb(s, s1, v1),
            2: hsv2rgb(s, s2, v2),
        },
        'color_1': {
            0: hsv2rgb(s + 0.5 + d, s0, v0),
            1: hsv2rgb(s + 0.5 + d, s1, v1),
            2: hsv2rgb(s + 0.5 + d, s2, v2),
        },
        'color_2': {
            0: hsv2rgb(s + 0.5, s0, v0),
            1: hsv2rgb(s + 0.5, s1, v1),
            2: hsv2rgb(s + 0.5, s2, v2),
        },
        'color_3': {
            0: hsv2rgb(s + 0.5 - d, s0, v0),
            1: hsv2rgb(s + 0.5 - d, s1, v1),
            2: hsv2rgb(s + 0.5 - d, s2, v2),
        }
    }

d = 0.094
s = 0.0

s0 = 0.8
s1 = 0.5
s2 = 0.4

v0 = 0.8
v1 = 0.5
v2 = 0.3

COLORS_DARK = {
        'canvas_color': hsv2rgb(0, 0, 0.16),

        'node_background_color': {
            0: hsv2rgb(0, 0, 0.15),
            1: hsv2rgb(0, 0, 0.16),
            2: hsv2rgb(0, 0, 0.16),
        },
        'font_color_1': {
            0: hsv2rgb(1, 0, v0),
            1: hsv2rgb(1, 0, v1),
            2: hsv2rgb(1, 0, v2),
        },
        'font_color_2': {
            0: hsv2rgb(s + d, s0, v0),
            1: hsv2rgb(s + d, s1, v1),
            2: hsv2rgb(s + d, s2, v2),
        },
        'error_color': {
            0: hsv2rgb(s, s0, v0),
            1: hsv2rgb(s, s1, v1),
            2: hsv2rgb(s, s2, v2),
        },
        'color_1': {
            0: hsv2rgb(s + 0.5 + d, s0, v0),
            1: hsv2rgb(s + 0.5 + d, s1, v1),
            2: hsv2rgb(s + 0.5 + d, s2, v2),
        },
        'color_2': {
            0: hsv2rgb(s + 0.5, s0, v0),
            1: hsv2rgb(s + 0.5, s1, v1),
            2: hsv2rgb(s + 0.5, s2, v2),
        },
        'color_3': {
            0: hsv2rgb(s + 0.5 - d, s0, v0),
            1: hsv2rgb(s + 0.5 - d, s1, v1),
            2: hsv2rgb(s + 0.5 - d, s2, v2),
        }
    }


def dot_table(id, line_color, primary, secondary, error, bgcolor, cellborder=1):
    table = f'''
        "{id}" [label=<
            <table border="0" cellspacing="5" cellpadding="5" cellborder="{cellborder}" color="{line_color}" bgcolor="{bgcolor}">
                <tr>
                    <td balign="left" align="left" colspan="2"><font point-size="14" color="{primary}">{id} Создать модель Profile<br/><br/><font point-size="14" color="{primary}">bloggitt/core/models.py:10</font></font></td>
                </tr>
                <tr>
                    <td balign="left" align="left"><font point-size="14" color="{secondary}">Время: ?</font></td><td balign="left" align="left"><font point-size="14" color="{secondary}">Прогресс: 0 %</font></td>
                </tr>
                <tr>
                    <td balign="left" align="left" colspan="2"><font point-size="14" color="{error}">Неверный формат времени</font></td>
                </tr>
            </table>>
        ]
    \n'''

    return table


def edge_color(src, dst):
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


def edge(src_id, dst_id, src_color, dst_color, label, label_color):
    return f'{src_id}->{dst_id} [penwidth="2" style="solid" color="{edge_color(src_color, dst_color)}" fontcolor="{label_color}" label="{label}"];'


def dot(colors):
    canvas_color = colors['canvas_color']

    content = 'digraph workplan {\n'
    content += 'fontname="Helvetica,Arial,sans-serif"\n'
    content += f'bgcolor = "{canvas_color}"\n'
    content += 'dpi=60\n'
    content += 'edge [fontname="Helvetica,Arial,sans-serif"]\n'
    content += 'node [shape="plain" nojustify=true fontname="Helvetica,Arial,sans-serif"]\n'
    content += 'pad="0.5,0.5"\n'
    content += 'fontsize="32"\n'
    content += 'rankdir = "LR"\n'
    content += f'MAIN [shape="circle" label="" width="0.25" style="filled" color="{colors["color_1"][0]}"]\n'

    for c in range(1, 4):
        color = f'color_{c}'
        content += dot_table(f'{c}P', colors[color][0], colors['font_color_1'][0], colors['font_color_2'][0], colors['error_color'][0], colors['node_background_color'][0], 2)
        content += dot_table(f'{c}0', colors[color][0], colors['font_color_1'][0], colors['font_color_2'][0], colors['error_color'][0], colors['node_background_color'][0])
        content += dot_table(f'{c}1', colors[color][1], colors['font_color_1'][1], colors['font_color_2'][1], colors['error_color'][1], colors['node_background_color'][1])
        content += dot_table(f'{c}2', colors[color][2], colors['font_color_1'][2], colors['font_color_2'][2], colors['error_color'][2], colors['node_background_color'][2])
        content += dot_table(f'{c}3', colors['error_color'][0], colors['font_color_1'][0], colors['font_color_2'][0], colors['error_color'][0], colors['node_background_color'][0])

        content += edge('MAIN', f'"{c}P"', colors['color_1'][0], colors[color][0], 'label', colors['font_color_1'][0]) + '\n'
        content += edge(f'"{c}P"', f'{c}0', colors[color][0], colors[color][1], 'label', colors['font_color_1'][0]) + '\n'
        content += edge(f'{c}0', f'{c}1', colors[color][0], colors[color][1], 'label', colors['font_color_1'][0]) + '\n'
        content += edge(f'{c}1', f'{c}2', colors[color][1], colors[color][2], 'label', colors['font_color_1'][1]) + '\n'
        content += edge(f'{c}2', f'{c}3', colors[color][2], colors['error_color'][0], 'label', colors['font_color_1'][2]) + '\n'

    content += '}\n'

    file_name = 'colors-test.png'

    pathlib.Path('colors-test.dot').write_text(content)

    with tempfile.NamedTemporaryFile('w+t') as tf:
        tf.write(content)
        tf.flush()
        execute_command(f'dot -Tpng -o{file_name} {tf.name}')

    return content


def py():
    content = '# encoding: utf-8\n\n'

    names = ['COLORS_DARK', 'COLORS_LIGHT']
    for nn, colors in enumerate([COLORS_DARK, COLORS_LIGHT]):
        content += f"{names[nn]} = {{\n"
        content += f"    'canvas_color': '{colors['canvas_color']}',\n\n"

        color_names = ['node_background_color', 'font_color_1', 'font_color_2', 'error_color', 'color_1', 'color_2', 'color_3']

        n = 0
        for cidx, color_name in enumerate(color_names):
            for i in range(3):
                n += 1
                color = colors[f'{color_name}'][i]
                content += f"    '{color_name}_{i}': '{color}',\n"

            if cidx < len(color_names) - 1:
                content += '\n'

        content += '}\n'

        if nn < len(names) - 1:
            content += '\n'

    print(content)

    with open('./srclib/view/dot/colors.py', 'w') as f:
        f.write(content)

def conf():
    content = ''

    names = ['[COLOR_SCHEME_DARK]', '[COLOR_SCHEME_LIGHT]']
    for nn, colors in enumerate([COLORS_DARK, COLORS_LIGHT]):
        content += f"# {names[nn]}\n"
        content += f"# canvas_color = {colors['canvas_color']}\n\n"

        color_names = ['node_background_color', 'font_color_1', 'font_color_2', 'error_color', 'color_1', 'color_2', 'color_3']

        n = 0
        for cidx, color_name in enumerate(color_names):
            for i in range(3):
                n += 1
                color = colors[f'{color_name}'][i]
                content += f"# {color_name}_{i} = {color}\n"

            if cidx < len(color_names) - 1:
                content += '\n'

        # content += '\n'

        if nn < len(names) - 1:
            content += '\n'

    print(content)

    with open('./colors-test.conf', 'w') as f:
        f.write(content)


dot(COLORS_LIGHT)
py()
conf()
