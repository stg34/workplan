# encoding: utf-8

from srclib.presenter.estimate_presenter import EstimatePresenter
from srclib.presenter.progress_presenter import ProgressPresenter
from srclib.model.comment import Comment
from srclib.utils import setup_i18n

_ = setup_i18n('..', 'messages')


class GraphCommentPresenter():
    ERROR_MAP = {
        Comment.ERROR_ID_IS_NOT_DEFINED: _('ID IS NOT DEFINED'),
        Comment.ERROR_ID_IS_ALREADY_DEFINED: _('ID IS ALREADY DEFINED'),
        Comment.ERROR_DEVELOPER_IS_ALREADY_DEFINED: _('DEVELOPER IS ALREADY DEFINED'),
        Comment.ERROR_BLOCKER_IS_ALREADY_DEFINED: _('BLOCKER ATTRIBUTE IS ALREADY DEFINED'),
        Comment.ERROR_HEADER_IS_NOT_DEFINED: _('HEADER IS NOT DEFINED'),
        Comment.ERROR_HEADER_IS_ALREADY_DEFINED: _('HEADER IS ALREADY DEFINED'),
        Comment.ERROR_REFERENCE_TO_MAIN: _("COMMENT REFERENCES THE MAIN COMMENT (COMMENT WITH ID '{id}')").format(id=Comment.ID_MAIN),
        Comment.ERROR_EMPTY_DEPENDENCY: _('EMPTY DEPENDENCY'),
        Comment.ERROR_ORDER_IS_NOT_DEFINED: _('ORDER IS NOT DEFINED'),
        Comment.ERROR_ORPHAN: _('ORPHAN'),
    }

    def __init__(self, comment):
        self.comment = comment
        self.work_hours = comment.work_hours
        self.estimate = EstimatePresenter(comment.estimate, self.work_hours)
        self.progress = ProgressPresenter(comment.progress, self.work_hours)

    @property
    def file_label(self):
        return _('FILE')

    @property
    def def_position(self):
        return self.comment.def_position

    @property
    def file_value(self):
        return self.def_position

    @property
    def file(self):
        return self.file_label + ': ' + self.file_value

    @property
    def header(self):
        return self.comment.header

    @property
    def developer_name(self):
        if self.comment.developer_name:
            return _('DEVELOPER') + ': ' + self.comment.developer_name

        return None

    @property
    def blocked(self):
        if self.comment.blocked:
            return _('BLOCKED')

        return None

    @property
    def blocker(self):
        if self.comment.blocker:
            return _('BLOCKER') + ': ' + self.comment.blocker_comment

        return None

    @property
    def errors(self):
        errors = [self.ERROR_MAP[error] for error in self.comment.errors]

        return errors

    @property
    def all_errors(self):
        errors = [self.ERROR_MAP[error] for error in self.comment.errors]

        return errors + self.estimate.errors + self.progress.errors + self.graph_errors

    @property
    def graph_errors(self):
        errors = []

        if self.comment.id in self.comment.graph.not_uniq_ids:
            errors.append(_("NOT UNIQ ID '{id}'").format(id=self.comment.id))

        if self.comment.id in self.comment.graph.orphans_by_id:
            errors.append(_("ORPHAN").format(id=self.comment.id))

        if self.comment.id in self.comment.graph.unknown_dependencies_by_id:
            for dep in self.comment.graph.unknown_dependencies_by_id[self.comment.id]:
                errors.append(_("UNKNOWN DEPENDENCY '{dep}'").format(dep=dep))

        return errors

    def inspect(self):
        return f'{self.def_position}\n\n' + '\n'.join(["%4s %s" % (line['num'], line['line'].rstrip()) for line in self.comment.src_lines])
