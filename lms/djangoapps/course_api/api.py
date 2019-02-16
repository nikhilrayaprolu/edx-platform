"""
Course API
"""

from django.contrib.auth.models import AnonymousUser, User
from rest_framework.exceptions import PermissionDenied
from django.conf import settings
from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers
from lms.djangoapps.courseware.access import has_access
from lms.djangoapps.courseware.courses import (
    get_course_overview_with_access,
    get_courses,
    get_permission_for_course_about
)

from .permissions import can_view_courses_for_username


def get_effective_user(requesting_user, target_username):
    """
    Get the user we want to view information on behalf of.
    """
    if target_username == requesting_user.username:
        return requesting_user
    elif target_username == '':
        return AnonymousUser()
    elif can_view_courses_for_username(requesting_user, target_username):
        return User.objects.get(username=target_username)
    else:
        raise PermissionDenied()


def course_detail(request, username, course_key):
    """
    Return a single course identified by `course_key`.

    The course must be visible to the user identified by `username` and the
    logged-in user should have permission to view courses available to that
    user.

    Arguments:
        request (HTTPRequest):
            Used to identify the logged-in user and to instantiate the course
            module to retrieve the course about description
        username (string):
            The name of the user `requesting_user would like to be identified as.
        course_key (CourseKey): Identifies the course of interest

    Return value:
        `CourseOverview` object representing the requested course
    """
    user = get_effective_user(request.user, username)
    return get_course_overview_with_access(
        user,
        get_permission_for_course_about(),
        course_key,
    )


def list_courses(request, username, org=None, filter_=None):
    """
    Return a list of available courses.

    The courses returned are all be visible to the user identified by
    `username` and the logged in user should have permission to view courses
    available to that user.

    Arguments:
        request (HTTPRequest):
            Used to identify the logged-in user and to instantiate the course
            module to retrieve the course about description
        username (string):
            The name of the user the logged-in user would like to be
            identified as

    Keyword Arguments:
        org (string):
            If specified, visible `CourseOverview` objects are filtered
            such that only those belonging to the organization with the provided
            org code (e.g., "HarvardX") are returned. Case-insensitive.
        filter_ (dict):
            If specified, visible `CourseOverview` objects are filtered
            by the given key-value pairs.

    Return value:
        List of `CourseOverview` objects representing the collection of courses.
    """
    user = get_effective_user(request.user, username)
    from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
    courses = CourseOverview.get_all_courses(filter_=filter_)
    permission_name = configuration_helpers.get_value(
        'COURSE_CATALOG_VISIBILITY_PERMISSION',
        settings.COURSE_CATALOG_VISIBILITY_PERMISSION
    )
    courses = [c for c in courses if has_access(user, permission_name, c)]
    print(courses)
    #courses = get_courses(user, org=org, filter_=filter_)
    #print(courses)
    return courses
