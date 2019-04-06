from django.conf import settings
from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter

from openedx.core.djangoapps.youngsphere.sites.social_back import CourseWallView
from .api import SiteConfigurationViewSet, SiteViewSet, FileUploadView, SiteCreateView, \
    UsernameAvailabilityView, DomainAvailabilityView, \
    SchoolView, ClassView, SectionView, CourseView, UserMiniProfileView, UserSectionMappingView, SchoolProfile, \
    TeacherProfile, TeacherNewProfile, NewClassView, NewSectionView, StudentProfile, StudentNewProfile, \
    StudentEnrollView, NewStudentEnrollView, TeacherEnrollView, NewTeacherEnrollView, BulkNewStudentEnrollView, \
    SectionBulkNewStudentEnrollView, BulkNewStudentsView, ProgressLeaderBoard, ProductsView, UpdateTeacher, SEPView, \
    SocialWallView, ExtraContentView
from . import social_back
# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'site-configurations', SiteConfigurationViewSet)
router.register(r'sites', SiteViewSet)
router.register(r'school', SchoolView )
router.register(r'userminiprofile', UserMiniProfileView )
router.register(r'usersection', UserSectionMappingView )

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^upload_file/', FileUploadView.as_view()),
    url(r'^username/{}/'.format(settings.USERNAME_PATTERN), UsernameAvailabilityView.as_view()),
    url(r'^domain/(?P<subdomain>[\w.@+-]+)/', DomainAvailabilityView.as_view()),
    url(r'^register/', SiteCreateView.as_view()),
    url(r'^schoolprofile/{}/'.format(settings.USERNAME_PATTERN), SchoolProfile.as_view()),
    url(r'^teacher/(?P<pk>[0-9]+)/', TeacherProfile.as_view()),
    url(r'^updateteacher/(?P<pk>[0-9]+)/', UpdateTeacher.as_view()),
    url(r'^teacher/', TeacherNewProfile.as_view()),
    url(r'^class/(?P<pk>[0-9]+)/', ClassView.as_view()),
    url(r'^class/', NewClassView.as_view()),
    url(r'^section/(?P<pk>[0-9]+)/', SectionView.as_view()),
    url(r'^section/', NewSectionView.as_view()),
    url(r'^student/(?P<pk>[0-9]+)/', StudentProfile.as_view()),
    url(r'^student/', StudentNewProfile.as_view()),
    url(r'^course/(?P<pk>[0-9]+)/', CourseView.as_view()),
    url(r'^enroll_student/(?P<course_key>[\w\-\+\:]+)/', StudentEnrollView.as_view()),
    url(r'^enroll_student/', NewStudentEnrollView.as_view()),
    url(r'^enroll_teacher/(?P<course_key>[\w\-\+\:]+)/', TeacherEnrollView.as_view()),
    url(r'^enroll_teacher/', NewTeacherEnrollView.as_view()),
    url(r'^bulk_enroll_student/', BulkNewStudentEnrollView.as_view()),
    url(r'^bulk_enroll_student/', BulkNewStudentsView.as_view()),
    url(r'^bulk_enroll_section/', SectionBulkNewStudentEnrollView.as_view()),
    url(r'^progressleaderboard/', ProgressLeaderBoard.as_view()),
    url(r'^products/', ProductsView.as_view()),
    url(r'^engagement/', SEPView.as_view()),
    url(r'^social_wall/', SocialWallView.as_view()),
    url(r'^extra_content/', ExtraContentView.as_view()),
    #socialwall urls
    url(r'friendslist', social_back.friends, name='friends'),
    url(r'groupstats', social_back.GroupStats.as_view()),
    url(r'me', social_back.me, name='me'),
    url(r'search/user', social_back.search, name='search'),
    url(r'^getfeed/(?P<feedgroup>[\w\-]+)/(?P<userid>[\w\-]+)', social_back.getfeed, name='getfeed'),
    url(r'^follow', social_back.FollowApi.as_view()),
    url(r'^moderator/(?P<feedgroup>[\w\-]+)', social_back.isModerator.as_view()),
    url(r'^approve/', social_back.ApproveFeed.as_view()),
    url(r'', social_back.index, name='index'),
    url(r'^', include(router.urls)),
    url(r"^course_wall", login_required(CourseWallView.as_view()), name="course_wall_dashboard")
]
