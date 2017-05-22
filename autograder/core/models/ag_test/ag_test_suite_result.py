from typing import List

from django.db import models

from ..ag_model_base import AutograderModel, ToDictMixin
from .ag_test_suite import AGTestSuite, AGTestSuiteFeedbackConfig
from .feedback_category import FeedbackCategory
from ..submission import Submission


class AGTestSuiteResult(AutograderModel):
    ag_test_suite = models.ForeignKey(
        AGTestSuite, help_text='The AGTestSuite that this result belongs to.')

    submission = models.ForeignKey(Submission, help_text='The Submission that this result is for.')

    # FIXME
    setup_output = models.TextField(blank=True)
    teardown_output = models.TextField(blank=True)

    def get_fdbk(self, fdbk_category: FeedbackCategory) -> 'AGTestSuiteResult.FeedbackCalculator':
        return AGTestSuiteResult.FeedbackCalculator(self, fdbk_category)

    class FeedbackCalculator(ToDictMixin):
        def __init__(self, ag_test_suite_result: 'AGTestSuiteResult',
                     fdbk_category: FeedbackCategory):
            self._ag_test_suite_result = ag_test_suite_result
            self._fdbk_category = fdbk_category
            self._ag_test_suite = self._ag_test_suite_result.ag_test_suite

            if fdbk_category == FeedbackCategory.normal:
                self._fdbk = self._ag_test_suite.normal_fdbk_config
            elif fdbk_category == FeedbackCategory.ultimate_submission:
                self._fdbk = self._ag_test_suite.ultimate_submission_fdbk_config
            elif fdbk_category == FeedbackCategory.past_limit_submission:
                self._fdbk = self._ag_test_suite.past_limit_submission_fdbk_config
            elif fdbk_category == FeedbackCategory.staff_viewer:
                self._fdbk = self._ag_test_suite.staff_viewer_fdbk_config
            elif fdbk_category == FeedbackCategory.max:
                self._fdbk = AGTestSuiteFeedbackConfig(show_individual_tests=True,
                                                       show_setup_and_teardown_commands=True)

        @property
        def fdbk_conf(self):
            return self._fdbk

        @property
        def pk(self):
            return self._ag_test_suite_result.pk

        @property
        def ag_test_suite_name(self):
            return self._ag_test_suite.name

        @property
        def ag_test_suite_pk(self):
            return self._ag_test_suite.pk

        @property
        def fdbk_settings(self) -> dict:
            return self._fdbk.to_dict()

        @property
        def total_points(self):
            return sum((ag_test_case_result.get_fdbk(self._fdbk_category).total_points
                        for ag_test_case_result in
                        self._ag_test_suite_result.ag_test_case_results.all()))

        @property
        def total_points_possible(self):
            return sum((ag_test_case_result.get_fdbk(self._fdbk_category).total_points_possible
                        for ag_test_case_result in
                        self._ag_test_suite_result.ag_test_case_results.all()))

        @property
        def ag_test_case_results(self) -> List['AGTestCaseResult']:
            if not self._fdbk.show_individual_tests:
                return []

            test_order = self._ag_test_suite.get_agtestcase_order()
            results = list(self._ag_test_suite_result.ag_test_case_results.all())
            return [next(filter(lambda result: result.ag_test_case.pk == test_pk, results))
                    for test_pk in test_order]

        SERIALIZABLE_FIELDS = (
            'pk',
            'ag_test_suite_name',
            'ag_test_suite_pk',
            'fdbk_settings',
            'total_points',
            'total_points_possible',
        )
