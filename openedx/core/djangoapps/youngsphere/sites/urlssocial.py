from django.conf import settings
from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from openedx.core.djangoapps.youngsphere.sites.social_back import CourseWallView
from . import social_back

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'friendslist', social_back.friends, name='friends'),
    url(r'followerslist', social_back.followers, name='followers'),
    url(r'follow_count', social_back.FollowCount.as_view()),
    url(r'groupstatslist', social_back.GroupStats),
    url(r'delete_reaction', social_back.remove_comment, name='remove_comment'),
    url(r'me', social_back.me, name='me'),
    url(r'search/user', social_back.search, name='search'),
    url(r'^getfeed/(?P<feedgroup>[\w\-]+)/(?P<userid>[\w\-]+)', social_back.getfeed, name='getfeed'),
    url(r'^follow', social_back.FollowApi.as_view()),
    url(r'^moderator/(?P<feedgroup>[\w\-]+)', social_back.isModerator.as_view()),
    url(r'^approve/', social_back.ApproveFeed.as_view()),
    url(r"^course_wall", login_required(CourseWallView.as_view()), name="course_wall_dashboard"),
    url(r'', social_back.index, name='index'),

]
