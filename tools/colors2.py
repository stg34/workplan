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


def color1(hex, n):
    S0 = 1
    S1 = S0 * 0.6
    S2 = S1 * 0.6
    S = [S0, S1, S2]

    V0 = 0.9
    V1 = V0 * 0.6
    V2 = V1 * 0.6
    V = [V0, V1, V2]

    c = matplotlib.colors.hex2color(hex)
    c = matplotlib.colors.rgb_to_hsv(c)
    c[1] = c[1] * S[n]
    c[2] = c[2] * V[n]
    c = matplotlib.colors.hsv_to_rgb(c)

    return matplotlib.colors.rgb2hex(c)


def color_light(hex, n):
    try:
        S0 = 1
        S1 = S0 * 0.5
        S2 = S1 * 0.5
        S = [S0, S1, S2]

        V0 = 1
        V1 = V0 * 1
        V2 = V1 * 1
        V = [V0, V1, V2]

        c = matplotlib.colors.hex2color(hex)
        c = matplotlib.colors.rgb_to_hsv(c)
        c[1] = c[1] * S[n]
        c[2] = c[2] * V[n]
        c = matplotlib.colors.hsv_to_rgb(c)

        return matplotlib.colors.rgb2hex(c)
    except Exception as error:
        print(hex, c)
        raise error


def color_dark(hex, s, v):
    c = matplotlib.colors.hex2color(hex)
    c = matplotlib.colors.rgb_to_hsv(c)

    c[1] = c[1] * s
    c[2] = c[2] * v

    c = matplotlib.colors.hsv_to_rgb(c)

    return matplotlib.colors.rgb2hex(c)


def color_debug(hex, s, v):
    c = matplotlib.colors.hex2color(hex)
    c = matplotlib.colors.rgb_to_hsv(c)
    # c[1] = c[1]*s
    # c[2] = c[2]*v
    print('---')
    print(f'original: {hex}')
    print(f's: {c[1]}')
    print(f'v: {c[2]}')
    clear = matplotlib.colors.rgb2hex(matplotlib.colors.hsv_to_rgb([c[0], 1, 1]))
    print(f'clear: {clear}')
    print('---')
    print(hex, c, matplotlib.colors.rgb2hex(matplotlib.colors.hsv_to_rgb([1, 1, 1])))
    c = matplotlib.colors.hsv_to_rgb(c)

    return matplotlib.colors.rgb2hex(c)


def base_color(hex):
    c = matplotlib.colors.hex2color(hex)
    c = matplotlib.colors.rgb_to_hsv(c)
    return matplotlib.colors.rgb2hex(matplotlib.colors.hsv_to_rgb([c[0], 1, 1]))


DARK_CANVAS = '#2b2b2b'
DARK_PRIMARY_FONT = '#f2f2f2'
DARK_SECONDARY_FONT = '#D7B600'
DARK_ERROR_FONT = '#AD003D'
DARK_COLOR_1 = '#0082AD'
DARK_COLOR_2 = '#00D70A'
DARK_COLOR_3 = '#6D00F6'

LIGHT_CANVAS = '#f5f5f5'
LIGHT_PRIMARY_FONT = '#54647A'
LIGHT_SECONDARY_FONT = '#9D6285'
LIGHT_ERROR_FONT = '#c93a90'
LIGHT_EXISTING_FILE = '#458BF5'
LIGHT_NEW_FILE = '#42bb3b'

COLORS_DARK = {
        'canvas color': {
            'canvas_color': color_dark(DARK_CANVAS, 1, 1),
        },

        'main node line color': {
            'main_node_line_color': color1(DARK_PRIMARY_FONT, 1),
        },

        'node background color': {
            'node_color_0': color_dark(DARK_CANVAS, 1, 0.96),
            'node_color_1': color_dark(DARK_CANVAS, 1, 0.98),
            'node_color_2': color_dark(DARK_CANVAS, 1, 1),
        },

        'primary font color': {
            0: color1(DARK_PRIMARY_FONT, 0),
            1: color1(DARK_PRIMARY_FONT, 1),
            2: color1(DARK_PRIMARY_FONT, 2),
        },

        'secondary font color': {
            0: color1(DARK_SECONDARY_FONT, 0),
            1: color1(DARK_SECONDARY_FONT, 1),
            2: color1(DARK_SECONDARY_FONT, 2),
        },
        'error color': {
            0: color1(DARK_ERROR_FONT, 0),
            1: color1(DARK_ERROR_FONT, 1),
            2: color1(DARK_ERROR_FONT, 2),
        },
        'color_1': {
            0: color1(DARK_COLOR_1, 0),
            1: color1(DARK_COLOR_1, 1),
            2: color1(DARK_COLOR_1, 2),
        },
        'color_2': {
            0: color1(DARK_COLOR_2, 0),
            1: color1(DARK_COLOR_2, 1),
            2: color1(DARK_COLOR_2, 2),
        },
        'color_3': {
            0: color1(DARK_COLOR_3, 0),
            1: color1(DARK_COLOR_3, 1),
            2: color1(DARK_COLOR_3, 2),
        }
    }

COLORS_LIGHT = {
        'canvas color': {
            'canvas_color': color_dark(LIGHT_CANVAS, 1, 1),
        },

        'main node line color': {
            'main_node_line_color': color1(LIGHT_PRIMARY_FONT, 1),
        },

        'node background color': {
            'node_color_0': color_dark(LIGHT_CANVAS, 1, 0.96),
            'node_color_1': color_dark(LIGHT_CANVAS, 1, 0.98),
            'node_color_2': color_dark(LIGHT_CANVAS, 1, 1),
        },

        'primary font color': {
            'font_primary_color_0': color_light(LIGHT_PRIMARY_FONT, 0),
            'font_primary_color_1': color_light(LIGHT_PRIMARY_FONT, 1),
            'font_primary_color_2': color_light(LIGHT_PRIMARY_FONT, 2),
        },

        'secondary font color': {
            'font_secondary_color_0': color_light(LIGHT_SECONDARY_FONT, 0),
            'font_secondary_color_1': color_light(LIGHT_SECONDARY_FONT, 1),
            'font_secondary_color_2': color_light(LIGHT_SECONDARY_FONT, 2),
        },

        'error font color': {
            'font_error_color_0': color_light(LIGHT_ERROR_FONT, 0),
            'font_error_color_1': color_light(LIGHT_ERROR_FONT, 1),
            'font_error_color_2': color_light(LIGHT_ERROR_FONT, 2),
        },

        'border and edge 1 (existing file)': {
            'line_1_color_0': color_light(LIGHT_EXISTING_FILE, 0),
            'line_1_color_1': color_light(LIGHT_EXISTING_FILE, 1),
            'line_1_color_2': color_light(LIGHT_EXISTING_FILE, 2),
        },

        'border and edge 2 (new file)': {
            'line_2_color_0': color_light(LIGHT_NEW_FILE, 0),
            'line_2_color_1': color_light(LIGHT_NEW_FILE, 1),
            'line_2_color_2': color_light(LIGHT_NEW_FILE, 2),
        },

        'border and edge 3 color': {
            'line_error_color_0': color_light(LIGHT_ERROR_FONT, 0),
            'line_error_color_1': color_light(LIGHT_ERROR_FONT, 1),
            'line_error_color_2': color_light(LIGHT_ERROR_FONT, 2),
        }
    }


def dot_table(id, line_color, primary, secondary, error, cellborder = 1):
    table = f'''
        "{id}" [label=<
            <table border="0" cellspacing="5" cellpadding="5" cellborder="{cellborder}" color="{line_color}" bgcolor="#2a2a2a">
                <tr>
                    <td balign="left" align="left" colspan="2"><font point-size="14" color="{primary}">Создать модель Profile<br/><br/><font point-size="14" color="{primary}">bloggitt/core/models.py:10</font></font></td>
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
    canvas_color = colors['canvas color']['canvas_color']
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
        print(c)
        color = f'color_{c}'
        content += dot_table(f'{c}P', colors[color][0], colors['primary font color'][0], colors['secondary font color'][0], colors['error color'][0], 3)
        content += dot_table(f'{c}0', colors[color][0], colors['primary font color'][0], colors['secondary font color'][0], colors['error color'][0])
        content += dot_table(f'{c}1', colors[color][1], colors['primary font color'][1], colors['secondary font color'][1], colors['error color'][1])
        content += dot_table(f'{c}2', colors[color][2], colors['primary font color'][2], colors['secondary font color'][2], colors['error color'][2])
        content += dot_table(f'{c}3', colors['error color'][0], colors['primary font color'][0], colors['secondary font color'][0], colors['error color'][0])

        content += edge('MAIN', f'"{c}P"', colors['color_1'][0], colors[color][0], 'label', colors['primary font color'][0]) + '\n'
        content += edge(f'"{c}P"', f'{c}0', colors[color][0], colors[color][1], 'label', colors['primary font color'][0]) + '\n'
        content += edge(f'{c}0', f'{c}1', colors[color][0], colors[color][1], 'label', colors['primary font color'][0]) + '\n'
        content += edge(f'{c}1', f'{c}2', colors[color][1], colors[color][2], 'label', colors['primary font color'][1]) + '\n'
        content += edge(f'{c}2', f'{c}3', colors[color][2], colors['error color'][0], 'label', colors['primary font color'][2]) + '\n'

    content += '}\n'

    file_name = 'colors-test.png'

    pathlib.Path('colors-test.dot').write_text(content)

    with tempfile.NamedTemporaryFile('w+t') as tf:
        tf.write(content)
        tf.flush()
        execute_command(f'dot -Tpng -o{file_name} {tf.name}')

    return content


def py(colors):
    content = 'COLORS = {\n'

    groups = colors.keys()

    for idx, group in enumerate(groups):
        content += f'    # {group}\n'
        for cidx, color_name in enumerate(colors[group].keys()):
            color = colors[group][color_name]
            content += f"    '{color_name}': '{color}'"
            if idx < len(groups) - 1 or cidx < len(colors[group].keys()) - 1:
                content += ','
            content += '\n'

        if idx < len(groups) - 1:
            content += '\n'

    content += '}\n'
    # print(content)

    with open('./srclib/dot_colors.py', 'w') as f:
        f.write(content)


dot(COLORS_DARK)
# py(COLORS_DARK)
