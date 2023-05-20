# encoding: utf-8

from srclib.model.comment import Comment
from srclib.utils import setup_i18n

_ = setup_i18n('..', 'messages')


class GraphPresenter():
    def __init__(self, graph):
        self.graph = graph

    # @property
    # def comment_errors(self):
    #     errors = []
    #     graph = self.graph

    #     if not graph.semantic_comments:
    #         errors.append(self.error_no_comments)

    #     if not graph.has_main_comment:
    #         errors.append(self.error_no_main_comment)

    #     if self.has_comments_with_errors:
    #         errors.append(self.error_comments_with_errors)

    #     return errors

    @property
    def errors(self):
        errors = []
        graph = self.graph

        if not graph.semantic_comments:
            errors.append(self.error_no_comments)

        if not graph.has_main_comment:
            errors.append(self.error_no_main_comment)

        if self.has_comments_with_errors:
            errors.append(self.error_comments_with_errors)

        if graph.has_loops:
            errors.append(self.error_loops)

        return errors

    @property
    def error_no_comments(self):
        return _('NO COMMENTS')

    @property
    def error_comments_with_errors(self):
        return _('COMMENTS WITH ERRORS')

    @property
    def error_no_main_comment(self):
        return _('MAIN COMMENT IS NOT DEFINED (COMMENT WITH ID "{id}")').format(id=Comment.ID_MAIN)

    @property
    def error_loops(self):
        return _('LOOPS')

    @property
    def error_loop(self):
        return _('LOOP')

    @property
    def has_comments_with_errors(self):
        graph = self.graph
        return self.has_comment_errors or graph.has_not_uniq_ids or graph.has_unknown_dependencies or graph.has_orphans

    # @property
    # def not_uniq_id_error(self):
    #     return 'ERROR'

    @property
    def has_comment_errors(self):
        return len([c for c in self.graph.semantic_comments if c.has_errors or c.estimate.has_errors or c.progress.has_errors]) != 0

    @property
    def main_comment_not_found_label(self):
        return _("MAIN COMMENT IS NOT DEFINED (COMMENT WITH ID '{id}')").format(id=Comment.ID_MAIN)
