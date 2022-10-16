class MarkdownBuilder:
    def __init__(self, comments_graph, title, debug = False):
        self.comments_graph = comments_graph
        self.title = title
        self.debug = debug
        self.title = 'TFX-5641 Related articles'

    def total_expected_time(self):
        time = 0
        for comment in self.comments_graph.comments:
            time += comment.time_expected
        return time
    
    def total_time_complete(self):
        time = 0
        for comment in self.comments_graph.comments:
            time += comment.time_complete()
        return time
    
    def total_complete(self):
        return round((self.total_time_complete() / self.total_expected_time()) * 100)

    def debug_info(self, comment):
        indent = 2
        indent_str = ' ' * indent
        content = f'{indent_str}<br>\n'
        content += f'{indent_str}<sup>\n'
        content += f'{indent_str}  Определено: {comment.file_name}:{comment.src_line_num}<br>\n'
        content += f'{indent_str}  Порядок: {comment.order}<br>\n'
        for dep in comment.dependencies:
            content += f'{indent_str}  Зависимость: {dep}<br>\n'

        content += f'{indent_str}</sup>\n'
        return content

    def build(self):
        content = '\n'
        content += f'# {self.title}\n\n'

        ids = self.comments_graph.topological_sort()

        for id in ids:
            comment = self.comments_graph.comment(id)
            content += f'* {comment.header}\n'
            content += f'  - Время: {comment.time_expected}\n'
            content += f'  - Готовность: {comment.completeness}% \n'
            # content += f'  - Время: {comment.time_expected}\n'
            content += self.debug_info(comment)

        content += '\n'
        content += f'**Время: {self.total_expected_time()} ч.**\n\n'
        # content += f'**Готовность: {52}%**\n'
       
        with open('test.md', 'w') as f:
            f.write(content)

        # print(content)
        return content
    
    def tree_comment(self, comment, level):
        max_level = 1

        if level >= max_level: 
            indent = max_level
        else:
            indent = level

        indent_str = ' ' * indent * 2
        content = ''
        content += f'{indent_str}* {comment.header}\n'
        content += f'{indent_str}  - Время: {comment.time_expected}\n'
        content += f'{indent_str}  - Готовность: {comment.completeness}% \n'

        if self.debug: 
            content += self.debug_info(comment)

        self.cb_content += content
        # return content

    def build_tree(self):
        content = '\n'
        content += f'# {self.title}\n\n'

        self.cb_content = ''
        ids = self.comments_graph.independent_comment_ids(reverse = False)
        ids.sort(key = lambda id: self.comments_graph.comment(id).order)
        
        for id in ids:
            self.comments_graph.dfs(id, self.tree_comment)

        content += self.cb_content
        content += '\n'
        content += f'**Время: {self.total_expected_time()} ч.**<br>\n'
        content += f'**Готовность: {self.total_complete()} %**\n'
       
        with open('test-tree.md', 'w') as f:
            f.write(content)

        return content
    
    def build_plain(self):
        content = '\n'
        content += f'# {self.title}\n\n'

        comments = self.comments_graph.comments.sort(key = lambda comment: comment.order)

        for comment in self.comments_graph.comments:
            content += f'* {comment.header}\n'
            content += f'  - Время: {comment.time_expected}\n'
            content += f'  - Готовность: {comment.completeness}% \n'
            # content += f'  - {comment.time_expected} ч. / {comment.completeness}%\n'
            if self.debug: 
                content += self.debug_info(comment)

        content += '\n'
        content += f'**Время: {self.total_expected_time()} ч.**<br>\n'
        content += f'**Готовность: {self.total_complete()} %**\n'
       
        with open('test-plain.md', 'w') as f:
            f.write(content)

        # print(content)
        return content
    