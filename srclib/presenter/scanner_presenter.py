# encoding: utf-8

from srclib.utils import setup_i18n
from pathlib import Path
_ = setup_i18n('..', 'messages')


class ScannerPresenter():
    def __init__(self, scanner, excluded_extensions):
        self.scanner = scanner
        self.excluded_extensions = excluded_extensions

    @property
    def errors(self):
        errors = []

        for error in self.scanner.files_with_errors:
            errors.append(_("SCAN FILE ERROR: {file_name} {error}").format(file_name=error['file_name'], error=error['error']))

        return ['\n'.join(errors)]

    @property
    def positions(self):
        comments = []

        for src_comment in self.scanner.src_comments:
            header = ''

            if len(src_comment["header"]) > 0:
                header = src_comment["header"][0]

            comments.append([src_comment["file_name"], src_comment["line_num"], header])

        comments.sort()
        comments = [f'{c[0]}:{c[1]} {c[2]}' for c in comments]

        return _('COMMENT DEFINITIONS:') + '\n\n' + '\n'.join(comments)

    @property
    def exclude_hint(self):
        excluded_extensions = self.excluded_extensions
        error_files = [e['file_name'] for e in self.scanner.files_with_errors]
        error_extensions = [Path(f).suffix for f in error_files]

        extensions = list(set(excluded_extensions + error_extensions))
        extensions.sort()
        extensions = ','.join([e.replace('.', '') for e in extensions])

        return _('HINT SCAN ERROR {ext}').format(ext=extensions)
