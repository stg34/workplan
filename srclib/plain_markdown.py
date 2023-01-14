class PlainMarkdown:
    def __init__(self, comments, title, unit, work_hours, verbose):
        self.comments = comments
        self.title = title
        self.verbose = verbose
        self.title = title
        self.unit = unit
        self.work_hours = work_hours

    def total_expected_time(self):
        time = 0
        for comment in self.comments:
            time += comment.time
        return time

    def total_time_complete(self):
        time = 0
        for comment in self.comments:
            time += (comment.time * comment.completeness)/100
        return time

    def total_complete(self):
        return round((self.total_time_complete() / self.total_expected_time()) * 100)

    def fib(self, n):
        a, b = 0, 1
        while a < n: a, b = b, a + b

        return a

    def debug_info(self, comment):
        indent = 2
        indent_str = ' ' * indent
        content = ''
        content += f'{indent_str}<sub><sup>'
        content += f'{indent_str}  Определено: {comment.file_name}:{comment.src_line_num}'
        content += f'{indent_str}  Порядок: {comment.order}<br>'
        content += f'{indent_str}</sup></sub>\n'
        return content

    def build(self):
        content = '\n'
        content += f'# План задачи {self.title}\n\n'

        if not self.comments:
            content += 'Пусто\n'
            return content

        if self.unit == 'hour':
            days_str = ''
            if self.work_hours:
                days = int(self.total_expected_time() / self.work_hours)
                hours = int(self.total_expected_time() % self.work_hours)
                days_str = f' ({days} д. {hours} ч.)'

            content += f'**Время: {self.total_expected_time()} ч.{days_str}**\n'
            content += f'**Готовность: {self.total_complete()} %**\n'
        else:
            content += f'**SP: {self.fib(self.total_expected_time())}**<br>\n'
            content += f'**Готовность: {self.total_complete()} %**\n'

        for comment in self.comments:
            if comment.completeness == 100:
                content += f'* ~~{comment.description}~~\n'
            elif comment.completeness > 0:
                content += f'* __{comment.description}__\n'
            else:
                content += f'* {comment.description}\n'
            content += f'  <sup>{comment.file_name}</sup>\n'

            if self.unit == 'hour':
                content += f'  <sup>Время: {comment.time} ч. Готовность: {comment.completeness}%</sup>\n'
            else:
                content += f'  <sup>SP: {comment.time}. Готовность: {comment.completeness}%</sup>\n'

            if self.verbose:
                content += self.debug_info(comment)

        return content
