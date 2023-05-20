import subprocess
import tempfile
import matplotlib.colors

# tuple(int('#afeeaa'.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))


def execute_command(command):
    res = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="UTF8")

    if res.returncode != 0:
        print(command, res.stdout, res.stderr)
        return


def color1(hex, n):
    S0 = 0.9
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


# print(base_color('#2f2f2f'))
# color_debug('#2f2f2f', 1, 1)

DARK_CANVAS = '#2b2b2b'
DARK_PRIMARY_FONT = '#f2f2f2'
DARK_SECONDARY_FONT = '#f28f4e'
DARK_ERROR_FONT = '#f14c4c'
DARK_EXISTING_FILE = '#00abff'
DARK_NEW_FILE = '#47ac55'

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
            'font_primary_color_0': color1(DARK_PRIMARY_FONT, 0),
            'font_primary_color_1': color1(DARK_PRIMARY_FONT, 1),
            'font_primary_color_2': color1(DARK_PRIMARY_FONT, 2),
        },

        'secondary font color': {
            'font_secondary_color_0': color1(DARK_SECONDARY_FONT, 0),
            'font_secondary_color_1': color1(DARK_SECONDARY_FONT, 1),
            'font_secondary_color_2': color1(DARK_SECONDARY_FONT, 2),
        },

        'error font color': {
            'font_error_color_0': color1(DARK_ERROR_FONT, 0),
            'font_error_color_1': color1(DARK_ERROR_FONT, 1),
            'font_error_color_2': color1(DARK_ERROR_FONT, 2),
        },

        'border and edge 1 (existing file)': {
            'line_1_color_0': color1(DARK_EXISTING_FILE, 0),
            'line_1_color_1': color1(DARK_EXISTING_FILE, 1),
            'line_1_color_2': color1(DARK_EXISTING_FILE, 2),
        },

        'border and edge 2 (new file)': {
            'line_2_color_0': color1(DARK_NEW_FILE, 0),
            'line_2_color_1': color1(DARK_NEW_FILE, 1),
            'line_2_color_2': color1(DARK_NEW_FILE, 2),
        },

        'border and edge 3 color': {
            'line_error_color_0': color1(DARK_ERROR_FONT, 0),
            'line_error_color_1': color1(DARK_ERROR_FONT, 1),
            'line_error_color_2': color1(DARK_ERROR_FONT, 2),
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


def dot(colors):
    canvas_color = colors['canvas color']['canvas_color']
    content = 'digraph workplan {\n'
    content += 'fontname="Helvetica,Arial,sans-serif"\n'
    content += f'bgcolor = "{canvas_color}"\n'
    content += 'dpi=60\n'
    content += 'node [style=filled shape="box" fontname="Helvetica,Arial,sans-serif"]\n'
    content += 'pad="0.5,0.5"\n'
    content += 'fontsize="32"\n'
    content += 'rankdir = "LR"\n'

    groups = list(colors.keys())
    groups.reverse()
    for group in groups:
        for color_name in colors[group].keys():
            color = colors[group][color_name]
            content += f'"{color_name}" [fontsize="18" fillcolor="{color}" width=3]\n'

    for group in groups:
        colors_num = len(colors[group])
        colors_names = list(colors[group].keys())

        if colors_num > 1:
            for n in range(1, colors_num):

                content += f'{colors_names[n-1]}->{colors_names[n]}\n'

    content += '}\n'

    file_name = 'colors-test.png'

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


dot(COLORS_LIGHT)
py(COLORS_DARK)
