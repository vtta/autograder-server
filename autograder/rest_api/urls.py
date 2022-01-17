from pathlib import Path

from django.http.request import HttpRequest
from django.http.response import FileResponse, HttpResponse
from django.shortcuts import render
from django.urls import path
from django.urls.conf import re_path

from autograder.rest_api import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

def api_docs_view(request: HttpRequest) -> HttpResponse:
    return render(request, 'swagger_ui.html')


def api_docs_view_redoc(request: HttpRequest) -> HttpResponse:
    return render(request, 'redoc.html')


def api_schema_yml_view(request: HttpRequest) -> FileResponse:
    return FileResponse(open(Path(__file__).resolve().parent / 'schema' / 'schema.yml', 'rb'))


urlpatterns = [
    re_path('docs/?$', api_docs_view, name='api-docs'),
    re_path('docs/redoc/?$', api_docs_view_redoc, name='api-docs-redoc'),
    path('docs/schema.yml', api_schema_yml_view, name='api-schema-yml'),

    path('oauth2callback/', views.oauth2_callback, name='oauth2callback'),
    path('users/current/', views.CurrentUserView.as_view(), name='current-user'),
    path('users/current/revoke_api_token/', views.RevokeCurrentUserAPITokenView.as_view(),
         name='revoke-api-token'),
    path('users/current/can_create_courses/', views.CurrentUserCanCreateCoursesView.as_view(),
         name='user-can-create-courses'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('users/<username_or_pk>/late_days/', views.UserLateDaysView.as_view(),
         name='user-late-days'),
    path('users/<int:pk>/courses_is_admin_for/', views.CoursesIsAdminForView.as_view(),
         name='courses-is-admin-for'),
    path('users/<int:pk>/courses_is_staff_for/', views.CoursesIsStaffForView.as_view(),
         name='courses-is-staff-for'),
    path('users/<int:pk>/courses_is_enrolled_in/', views.CoursesIsEnrolledInView.as_view(),
         name='courses-is-enrolled-in'),
    path('users/<int:pk>/courses_is_handgrader_for/', views.CoursesIsHandgraderForView.as_view(),
         name='courses-is-handgrader-for'),
    path('users/<int:pk>/groups_is_member_of/', views.GroupsIsMemberOfView.as_view(),
         name='groups-is-member-of'),
    path('users/<int:pk>/group_invitations_sent/', views.GroupInvitationsSentView.as_view(),
         name='group-invitations-sent'),
    path('users/<int:pk>/group_invitations_received/',
         views.GroupInvitationsReceivedView.as_view(),
         name='group-invitations-received'),

    path('courses/', views.ListCreateCourseView.as_view(), name='list-create-courses'),
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course-detail'),
    path('courses/<int:pk>/my_roles/',
         views.CourseUserRolesView.as_view(),
         name='course-user-roles'),
    path('course/<str:name>/<str:semester>/<int:year>/',
         views.CourseByNameSemesterYearView.as_view(),
         name='course-by-fields'),
    path('courses/<int:pk>/copy/', views.CopyCourseView.as_view(), name='copy-course'),
    path('courses/<int:pk>/admins/', views.CourseAdminViewSet.as_view(), name='course-admins'),
    path('courses/<int:pk>/staff/', views.CourseStaffViewSet.as_view(), name='course-staff'),
    path('courses/<int:pk>/students/', views.CourseStudentsViewSet.as_view(),
         name='course-students'),
    path('courses/<int:pk>/handgraders/', views.CourseHandgradersViewSet.as_view(),
         name='course-handgraders'),

    path('courses/<int:pk>/projects/', views.ListCreateProjectView.as_view(),
         name='list-create-projects'),
    path('projects/<int:pk>/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('projects/<int:pk>/num_queued_submissions/', views.NumQueuedSubmissionsView.as_view(),
         name='num-queued-submissions'),
    path('projects/<int:project_pk>/copy_to_course/<int:target_course_pk>/',
         views.CopyProjectView.as_view(), name='copy-project'),

    path('projects/<int:pk>/all_submission_files/', views.AllSubmittedFilesTaskView.as_view(),
         name='all-submission-files-task'),
    path('projects/<int:pk>/ultimate_submission_files/',
         views.UltimateSubmissionSubmittedFilesTaskView.as_view(),
         name='ultimate-submission-files-task'),
    path('projects/<int:pk>/all_submission_scores/', views.AllScoresTaskView.as_view(),
         name='all-submission-scores-task'),
    path('projects/<int:pk>/ultimate_submission_scores/',
         views.UltimateSubmissionScoresTaskView.as_view(),
         name='ultimate-submission-scores-task'),

    path('projects/<int:pk>/download_tasks/', views.ListDownloadTasksView.as_view(),
         name='download-tasks'),
    path('download_tasks/<int:pk>/', views.DownloadTaskDetailView.as_view(),
         name='download-task-detail'),
    path('download_tasks/<int:pk>/result/', views.DownloadTaskResultView.as_view(),
         name='download-task-result'),

    path('projects/<int:pk>/results_cache/', views.ClearResultsCacheView.as_view(),
         name='project-results-cache'),

    path('projects/<int:project_pk>/import_handgrading_rubric_from/<int:import_from_project_pk>/',
         views.ImportHandgradingRubricView.as_view(), name='import-handgrading-rubric'),

    path('projects/<int:pk>/instructor_files/', views.ListCreateInstructorFileView.as_view(),
         name='instructor-files'),
    path('instructor_files/<int:pk>/', views.InstructorFileDetailView.as_view(),
         name='instructor-file-detail'),
    path('instructor_files/<int:pk>/name/', views.RenameInstructorFileView.as_view(),
         name='instructor-file-rename'),
    path('instructor_files/<int:pk>/content/', views.InstructorFileContentView.as_view(),
         name='instructor-file-content'),

    path('projects/<int:pk>/expected_student_files/',
         views.ListCreateExpectedStudentFileView.as_view(), name='expected-student-files'),
    path('expected_student_files/<int:pk>/',
         views.ExpectedStudentFileDetailView.as_view(), name='expected-student-file-detail'),


    path('projects/<int:pk>/group_invitations/',
         views.ListCreateGroupInvitationView.as_view(),
         name='group-invitations'),
    path('group_invitations/<int:pk>/', views.GroupInvitationDetailView.as_view(),
         name='group-invitation-detail'),
    path('group_invitations/<int:pk>/accept/', views.AcceptGroupInvitationView.as_view(),
         name='accept-group-invitation'),

    path('projects/<int:project_pk>/groups/',
        views.ListCreateGroupsView.as_view(), name='groups'),
    path('projects/<int:project_pk>/groups/solo_group/',
        views.CreateSoloGroupView.as_view(),
        name='solo_group'),
    path('groups/<int:pk>/', views.GroupDetailView.as_view(),
         name='group-detail'),
    path('groups/<int:pk>/ultimate_submission/', views.GroupUltimateSubmissionView.as_view(),
         name='group-ultimate-submission'),
    path('groups/<int:pk>/merge_with/<int:other_group_pk>/',
         views.MergeGroupsView.as_view(),
         name='merge-groups'),

    path('groups/<int:pk>/submissions/', views.ListCreateSubmissionView.as_view(),
         name='submissions'),
    path('submissions/<int:pk>/', views.SubmissionDetailView.as_view(),
         name='submission-detail'),
    path('submissions/<int:pk>/file/', views.GetSubmittedFileView.as_view(),
         name='submission-file'),
    path('submissions/<int:pk>/remove_from_queue/', views.RemoveSubmissionFromQueueView.as_view(),
         name='remove-submission-from-queue'),

    path('sandbox_docker_images/', views.ListCreateGlobalSandboxDockerImageView.as_view(),
         name='global-sandbox-images'),
    path('courses/<int:pk>/sandbox_docker_images/',
         views.ListCreateSandboxDockerImageForCourseView.as_view(),
         name='course-sandbox-images'),
    path('image_build_tasks/', views.ListGlobalBuildTasksView.as_view(),
         name='list-global-image-builds'),
    path('courses/<int:pk>/image_build_tasks/',
         views.ListBuildTasksForCourseView.as_view(),
         name='list-course-image-builds'),
    path('image_build_tasks/<int:pk>/', views.BuildTaskDetailView.as_view(),
         name='image-build-task-detail'),
    path('image_build_tasks/<int:pk>/output/', views.BuildTaskOutputView.as_view(),
         name='image-build-task-output'),
    path('image_build_tasks/<int:pk>/files/', views.DownloadBuildTaskFilesView.as_view(),
         name='image-build-task-files'),
    path('image_build_tasks/<int:pk>/cancel/', views.CancelBuildTaskView.as_view(),
         name='cancel-image-build-task'),
    path('sandbox_docker_images/<int:pk>/', views.SandboxDockerImageDetailView.as_view(),
         name='sandbox-docker-image-detail'),
    path('sandbox_docker_images/<int:pk>/rebuild/', views.RebuildSandboxDockerImageView.as_view(),
         name='rebuild-sandbox-docker-image'),

    path('projects/<int:project_pk>/ag_test_suites/',
        views.AGTestSuiteListCreateView.as_view(), name='ag_test_suites'),
    path('projects/<int:project_pk>/ag_test_suites/order/',
        views.AGTestSuiteOrderView.as_view(), name='ag_test_suite_order'),
    path('ag_test_suites/<int:pk>/', views.AGTestSuiteDetailView.as_view(),
         name='ag-test-suite-detail'),

    path('ag_test_suites/<int:ag_test_suite_pk>/ag_test_cases/',
        views.AGTestCaseListCreateView.as_view(), name='ag_test_cases'),
    path('ag_test_suites/<int:ag_test_suite_pk>/ag_test_cases/order/',
        views.AGTestCaseOrderView.as_view(), name='ag_test_case_order'),
    path('ag_test_cases/<int:pk>/', views.AGTestCaseDetailView.as_view(),
         name='ag-test-case-detail'),

    path('ag_test_cases/<int:ag_test_case_pk>/ag_test_commands/',
        views.AGTestCommandListCreateView.as_view(), name='ag_test_commands'),
    path('ag_test_cases/<int:ag_test_case_pk>/ag_test_commands/order/',
        views.AGTestCommandOrderView.as_view(), name='ag_test_command_order'),
    path('ag_test_commands/<int:pk>/', views.AGTestCommandDetailView.as_view(),
         name='ag-test-command-detail'),

    path('projects/<int:project_pk>/mutation_test_suites/',
        views.MutationTestSuiteListCreateView.as_view(), name='mutation_test_suites'),
    path('projects/<int:project_pk>/mutation_test_suites/order/',
        views.MutationTestSuiteOrderView.as_view(), name='mutation_test_suite_order'),
    path('mutation_test_suites/<int:pk>/', views.MutationTestSuiteDetailView.as_view(),
         name='student-test-suite-detail'),

    path('projects/<int:project_pk>/rerun_submissions_tasks/',
         views.RerunSubmissionsTaskListCreateView.as_view(),
         name='rerun_submissions_tasks'),
    path('rerun_submissions_tasks/<int:pk>/',
         views.RerunSubmissionsTaskDetailView.as_view(),
         name='rerun-submissions-task-detail'),
    path('rerun_submissions_tasks/<int:pk>/cancel/',
         views.CancelRerunSubmissionsTaskView.as_view(),
         name='cancel-rerun-submissions-task'),

    path('groups/<int:pk>/submissions_with_results/',
         views.ListSubmissionsWithResults.as_view(),
         name='list-submissions-with-results'),

    path('submissions/<int:pk>/results/',
         views.SubmissionResultsView.as_view(),
         name='submission-results'),

    path('projects/<int:project_pk>/all_ultimate_submission_results/',
         views.AllUltimateSubmissionResults.as_view(),
         name='all-ultimate-submission-results'),

    path('submissions/<int:pk>/ag_test_suite_results/<int:result_pk>/stdout/',
         views.AGTestSuiteResultStdoutView.as_view(),
         name='ag-test-suite-result-stdout'),
    path('submissions/<int:pk>/ag_test_suite_results/<int:result_pk>/stderr/',
         views.AGTestSuiteResultStderrView.as_view(),
         name='ag-test-suite-result-stderr'),
    path('submissions/<int:pk>/ag_test_suite_results/<int:result_pk>/output_size/',
         views.AGTestSuiteResultOutputSizeView.as_view(),
         name='ag-test-suite-result-output-size'),

    path('submissions/<int:pk>/ag_test_cmd_results/<int:result_pk>/stdout/',
         views.AGTestCommandResultStdoutView.as_view(),
         name='ag-test-cmd-result-stdout'),
    path('submissions/<int:pk>/ag_test_cmd_results/<int:result_pk>/stderr/',
         views.AGTestCommandResultStderrView.as_view(),
         name='ag-test-cmd-result-stderr'),
    path('submissions/<int:pk>/ag_test_cmd_results/<int:result_pk>/stdout_diff/',
         views.AGTestCommandResultStdoutDiffView.as_view(),
         name='ag-test-cmd-result-stdout-diff'),
    path('submissions/<int:pk>/ag_test_cmd_results/<int:result_pk>/stderr_diff/',
         views.AGTestCommandResultStderrDiffView.as_view(),
         name='ag-test-cmd-result-stderr-diff'),
    path('submissions/<int:pk>/ag_test_cmd_results/<int:result_pk>/output_size/',
         views.AGTestCommandResultOutputSizeView.as_view(),
         name='ag-test-cmd-result-output-size'),

    path('submissions/<int:pk>/mutation_test_suite_results/<int:result_pk>/setup_stdout/',
         views.MutationTestSuiteResultSetupStdoutView.as_view(),
         name='mutation-suite-setup-stdout'),
    path('submissions/<int:pk>/mutation_test_suite_results/<int:result_pk>/setup_stderr/',
         views.MutationTestSuiteResultSetupStderrView.as_view(),
         name='mutation-suite-setup-stderr'),

    path('submissions/<int:pk>/mutation_test_suite_results/<int:result_pk>/get_student_test_names_stdout/',  # noqa
         views.MutationTestSuiteResultGetStudentTestsStdoutView.as_view(),
         name='mutation-suite-get-student-test-names-stdout'),
    path('submissions/<int:pk>/mutation_test_suite_results/<int:result_pk>/get_student_test_names_stderr/',  # noqa
         views.MutationTestSuiteResultGetStudentTestsStderrView.as_view(),
         name='mutation-suite-get-student-test-names-stderr'),

    path('submissions/<int:pk>/mutation_test_suite_results/<int:result_pk>/validity_check_stdout/',
         views.MutationTestSuiteResultValidityCheckStdoutView.as_view(),
         name='mutation-suite-validity-check-stdout'),
    path('submissions/<int:pk>/mutation_test_suite_results/<int:result_pk>/validity_check_stderr/',
         views.MutationTestSuiteResultValidityCheckStderrView.as_view(),
         name='mutation-suite-validity-check-stderr'),

    path('submissions/<int:pk>/mutation_test_suite_results/<int:result_pk>/grade_buggy_impls_stdout/',  # noqa
         views.MutationTestSuiteResultGradeBuggyImplsStdoutView.as_view(),
         name='mutation-suite-grade-buggy-impls-stdout'),
    path('submissions/<int:pk>/mutation_test_suite_results/<int:result_pk>/grade_buggy_impls_stderr/',  # noqa
         views.MutationTestSuiteResultGradeBuggyImplsStderrView.as_view(),
         name='mutation-suite-grade-buggy-impls-stderr'),

    path('submissions/<int:pk>/mutation_test_suite_results/<int:result_pk>/output_size/',
         views.MutationTestSuiteOutputSizeView.as_view(),
         name='mutation-suite-result-output-size'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
