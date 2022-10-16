import subprocess

class DotBuilder:
    def __init__(self, comments_graph, title):
        self.comments_graph = comments_graph
        self.title = title

    def build(self, file_name = 'test.dot'):
        comments = self.comments_graph.comments
        bgcolor = '#2b2b2b'
        fontcolor = '#ca6d2f'
        linecolor = '#0278b2'

        content = 'digraph workplan {\n'
        content += 'fontname="Helvetica,Arial,sans-serif"\n'
        content += f'bgcolor = "{bgcolor}"\n'
        content += f'fontcolor = "{fontcolor}"\n'
        content += 'labelloc = "t"\n'
        content += 'rankdir = "LR"\n'
        content += 'labeljust = "l"\n'
        content += 'dpi = 60\n'
        content += f'label="{self.title}\n\n"\n'
        content += f'edge [color="{linecolor}"]\n'
        content += f'node [shape="plain" fontname="Helvetica,Arial,sans-serif" gradientangle="315" color="{linecolor}" fontcolor="{fontcolor}"]\n'

        for comment in comments:
            content += f'"{comment.id}" [label={self.node_label(comment)}]\n'
            content += '\n'

        for comment in comments:
            for dep in comment.dependencies:
                content += f'"{comment.id}"->"{dep}"\n'
                # content += f'"{dep}"->"{comment.id}"\n'

        content += '}\n'
        
        with open(file_name, 'w') as f:
            f.write(content)

        subprocess.run(f'dot -Tpng -O {file_name}', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="UTF8")

        return content
    
    def fit_string(self, string, width = 50):
        result = []
        content = ''
        parts = string.split()

        for part in parts:
            if len(content + part) >= width:
                result.append(content + '<br align="left"/>')
                content = ''
            else:    
                content += ' '

            content += part

        if content: 
            result.append(content)

        return ''.join(result)

    def node_label(self, comment):
        fontcolor = '#A9B7C6'
        bgcolor = '#2f2f2f:#252525'
        gradientangle = 135
        content = f'<<table ALIGN="LEFT" gradientangle="{gradientangle}" BGCOLOR="{bgcolor}" border="0" cellborder="1" cellspacing="0" cellpadding="5">'
        content += f'<tr><td align="left" BALIGN="LEFT"><FONT COLOR="{fontcolor}"><b>{self.fit_string(comment.header)}</b></FONT></td></tr>'
        # content += f'<tr><td BALIGN="LEFT" align="left">{self.fit_string(comment.header)}</td></tr>'
        content += f'<tr><td TITLE="value" align="left">Время: {comment.time_expected} ч.</td></tr>'
        content += f'<tr><td TITLE="value" align="left">Готовность: {comment.completeness}</td></tr>'
        content += f'<tr><td TITLE="value" align="left">Порядок: {comment.order}</td></tr>'
        content += f'<tr><td TITLE="value" align="left">ID: {comment.id}</td></tr>'
        content += f'<tr><td TITLE="value" align="left">Исходник:<br align="left"/>{comment.file_name}</td></tr>'
        content += '</table>>'
        return content
    