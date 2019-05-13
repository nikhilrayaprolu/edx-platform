import logging
import random
import string

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.files.storage import DefaultStorage, get_storage_class
from django.db import transaction
from django.http import Http404
from django.utils.decorators import method_decorator
from edx_rest_framework_extensions.authentication import JwtAuthentication
from opaque_keys.edx.keys import CourseKey
from rest_framework import generics, views, viewsets
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from organizations.models import UserOrganizationMapping
from edxmako.shortcuts import render_to_response, render_to_string

from openedx.core.djangoapps.site_configuration.models import SiteConfiguration
from rest_framework.views import APIView
from openedx.core.djangoapps.site_configuration import helpers as configuration_helpers
from openedx.core.djangoapps.user_api.accounts.api import check_account_exists
from openedx.core.djangoapps.youngsphere.social_engagement.models import StudentSocialEngagementProgressClassScore
from openedx.core.lib.api.permissions import ApiKeyHeaderPermission
from openedx.core.lib.api.authentication import (
    OAuth2AuthenticationAllowInactiveUser,
)

from .models import School, Class, Section, Course, UserMiniProfile, UserSectionMapping
from .permissions import AMCAdminPermission
from .serializers import SiteConfigurationSerializer, SiteConfigurationListSerializer, SiteSerializer, \
    RegistrationSerializer, SchoolSerializer, ClassSerializer, SectionSerializer, \
    CourseSerializer, UserMiniProfileSerializer, UserSectionMappingSerializer, OrganizationSerializer
from .utils import delete_site
from student.forms import PasswordResetFormNoActive
from student.views import create_account_with_params
from django.core.exceptions import NON_FIELD_ERRORS, ValidationError
from student.roles import CourseInstructorRole, CourseStaffRole
from student.models import CourseEnrollment, UserProfile
from enrollment.serializers import CourseEnrollmentSerializer
from django.db import IntegrityError

class SiteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    authentication_classes = (OAuth2AuthenticationAllowInactiveUser,)
    permission_classes = (IsAuthenticated, AMCAdminPermission)

    def get_queryset(self):
        queryset = Site.objects.exclude(id=settings.SITE_ID)
        user = self.request.user
        if not user.is_superuser:
            queryset = queryset.filter(organizations=user.organizations.all())
        return queryset


class SiteConfigurationViewSet(viewsets.ModelViewSet):
    queryset = SiteConfiguration.objects.all()
    serializer_class = SiteConfigurationSerializer
    list_serializer_class = SiteConfigurationListSerializer
    create_serializer_class = SiteSerializer
    authentication_classes = (OAuth2AuthenticationAllowInactiveUser,)
    permission_classes = (IsAuthenticated, AMCAdminPermission)

    def get_serializer_class(self):
        if self.action == 'list':
            return self.list_serializer_class
        if self.action == 'create':
            return self.create_serializer_class
        return super(SiteaConfigurationViewSet, self).get_serializer_class()

    def perform_destroy(self, instance):
        delete_site(instance)


class FileUploadView(views.APIView):
    parser_classes = (MultiPartParser,)
    def post(self, request, format=None):
        file_obj = request.data['file']
        file_path = self.handle_uploaded_file(file_obj, request.GET.get('filename'))
        return Response({'file_path': file_path}, status=201)

    def handle_uploaded_file(self, content, filename):
        kwargs = {}
        # passing these settings to the FileSystemStorage causes an exception
        if not settings.DEBUG:
            kwargs = {
                'location': "customer_files",
                'file_overwrite': False
            }
        storage = get_storage_class()(**kwargs)
        name = storage.save(filename, content)
        return storage.url(name)


class SiteCreateView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    authentication_classes = (
        TokenAuthentication,
    )

class UsernameAvailabilityView(APIView):
    def get(self, request, username, format=None):
        try:
            User.objects.get(username=username)
            return Response(None, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)


class DomainAvailabilityView(APIView):
    def get(self, request, subdomain, format=None):
        try:
            Site.objects.get(name=subdomain)
            return Response(None, status=status.HTTP_200_OK)
        except Site.DoesNotExist:
            return Response(None, status=status.HTTP_404_NOT_FOUND)



class SchoolView(viewsets.ModelViewSet):
    authentication_classes = (JwtAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = School.objects.all()
    serializer_class = SchoolSerializer


class UserMiniProfileView(viewsets.ModelViewSet):
    queryset = UserMiniProfile.objects.all()
    serializer_class = UserMiniProfileSerializer
    authentication_classes = (OAuth2AuthenticationAllowInactiveUser, JwtAuthentication,)
    permission_classes = (IsAuthenticated,)

class UserSectionMappingView(viewsets.ModelViewSet):
    queryset = UserSectionMapping.objects.all()
    serializer_class = UserSectionMappingSerializer
    authentication_classes = (OAuth2AuthenticationAllowInactiveUser,JwtAuthentication,)
    permission_classes = (IsAuthenticated,)

class SchoolProfile(APIView):
    #authentication_classes = (OAuth2AuthenticationAllowInactiveUser,)
    #permission_classes = (IsAuthenticated,)

    def get_user_organization(self, username):
        try:
            user = User.objects.get(username=username)
            print(user)
        except User.DoesNotExist:
            raise Http404
        try:
            return UserOrganizationMapping.objects.filter(user=user).first()

        except UserOrganizationMapping.DoesNotExist:
            raise Http404

    def get_user_school(self, organization):
        try:
            return School.objects.get(organization=organization)
        except School.DoesNotExist:
            return None

    def get(self, request, username):
        user_organization = self.get_user_organization(username)
        organization_serializer = OrganizationSerializer(user_organization.organization)
        user_school = self.get_user_school(user_organization.organization)
        if user_school is not None:
            school_serializer = SchoolSerializer(user_school)
            return Response({'organization': organization_serializer.data, 'school': school_serializer.data})
        return Response({'organization': organization_serializer.data, 'school': None})

log = logging.getLogger(__name__)

def create_password():
    """
    Copied from appsembler_api `CreateUserAccountWithoutPasswordView`
    """
    return ''.join(
        random.choice(
            string.ascii_uppercase + string.ascii_lowercase + string.digits)
        for _ in range(32))


def send_password_reset_email(request):
    """Copied/modified from appsembler_api.utils in enterprise Ginkgo
    Copied the template files from enterprise Ginkgo LMS templates
    """
    form = PasswordResetFormNoActive(request.data)
    if form.is_valid():
        form.save(
            use_https=request.is_secure(),
            from_email=configuration_helpers.get_value(
                'email_from_address', settings.DEFAULT_FROM_EMAIL),
            request=request,
            domain_override=request.get_host(),
            subject_template_name='youngsphere/emails/set_password_subject.txt',
            email_template_name='youngsphere/emails/set_password_email.html')
        return True
    else:
        return False



@method_decorator(transaction.non_atomic_requests, name='dispatch')
class TeacherProfile(APIView):
    #authentication_classes = (OAuth2AuthenticationAllowInactiveUser,JwtAuthentication)
    #permission_classes = (IsAuthenticated,)

    def get_school_teachers(self, school):
        try:
            user_mini_profile = UserMiniProfile.objects.filter(school=school, is_staff=True)
            print(user_mini_profile)
            return user_mini_profile
        except UserMiniProfile.DoesNotExist:
            raise Http404

    def get_user_school(self, organization):
        try:
            return School.objects.get(organization=organization)
        except School.DoesNotExist:
            return None

    def get(self, request, pk):
        print(pk)
        user_mini_profile = self.get_school_teachers(pk)
        user_mini_serializer = UserMiniProfileSerializer(user_mini_profile, many=True)
        return Response(user_mini_serializer.data)


    def get_object(self, pk):
        try:
            return UserMiniProfile.objects.get(pk=pk)
        except UserMiniProfile.DoesNotExist:
            raise Http404
    def put(self, request, pk):
        teacher = self.get_teacher(pk)
        serializer = UserMiniProfileSerializer(teacher, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(transaction.non_atomic_requests, name='dispatch')
class TeacherNewProfile(APIView):
    authentication_classes = (OAuth2AuthenticationAllowInactiveUser,JwtAuthentication)
    permission_classes = (IsAuthenticated,)


    def post(self, request):
        """Creates a new user account for the site that calls this view
        To use, perform a token authenticated POST to the URL::
            /tahoe/api/v1/registrations/
        Required arguments (JSON data):
            "username"
            "email"
            "name"
        Optional arguments:
            "password"
            "send_activation_email"
        Returns:
            HttpResponse: 200 on success, {"user_id ": 9}
            HttpResponse: 400 if the request is not valid.
            HttpResponse: 409 if an account with the given username or email
                address already exists
        The code here is adapted from the LMS ``appsembler_api`` bulk registration
        code. See the ``appsembler/ginkgo/master`` branch
        """
        data = request.data
        password_provided = 'password' in data

        # set the honor_code and honor_code like checked,
        # so we can use the already defined methods for creating an user
        data['honor_code'] = "True"
        data['terms_of_service'] = "True"

        if password_provided:
            if 'send_activation_email' in data and data['send_activation_email'] == "False":
                data['send_activation_email'] = False
            else:
                data['send_activation_email'] = True
        else:
            data['password'] = create_password()
            data['send_activation_email'] = False

        email = request.data.get('email')
        username = request.data.get('username')

        # Handle duplicate email/username
        conflicts = check_account_exists(email=email, username=username)
        if conflicts:
            errors = {"user_message": "User already exists"}
            return Response(errors, status=409)

        try:
            user = create_account_with_params(
                request=request,
                params=data,
                send_activation_email_flag=data['send_activation_email'])
            # set the user as active if password is provided
            # meaning we don't have to send a password reset email
            user.is_active = password_provided
            user.save()
            user_id = user.id
            if not password_provided:
                success = send_password_reset_email(request)
                if not success:
                    log.error('Tahoe Reg API: Error sending password reset '
                              'email to user {}'.format(user.username))
        except ValidationError as err:
            log.error('ValidationError. err={}'.format(err))
            # Should only get non-field errors from this function
            assert NON_FIELD_ERRORS not in err.message_dict
            # Only return first error for each field

            # TODO: Let's give a clue as to which are the error causing fields
            errors = {
                "user_message": "Invalid parameters on user creation"
            }
            return Response(errors, status=400)
        data['is_staff'] = "True"
        data['user'] = user.id
        data['birthday'] = data['birthday'][:10]
        user_mini_profile = UserMiniProfileSerializer(data = data)
        if user_mini_profile.is_valid():
            user_mini_profile.save()
        else:
            print(user_mini_profile.errors)

        return Response(user_mini_profile.data, status=200)

class UpdateTeacher(APIView):
    def get_object(self, pk):
        try:
            return UserMiniProfile.objects.get(pk=pk)
        except UserMiniProfile.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        teacher = self.get_object(pk)
        serializer = UserMiniProfileSerializer(teacher, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClassView(APIView):
    def get_class_organization(self, organization):
        try:
            classes = Class.objects.filter(organization=organization)
            print(classes)
            return classes
        except Class.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        classes = self.get_class_organization(pk)
        classes_serializer = ClassSerializer(classes, many=True)
        return Response(classes_serializer.data)


class NewClassView(APIView):
    def post(self, request):
        class_serializer = ClassSerializer(data=request.data)
        if class_serializer.is_valid():
            class_serializer.save()
            return Response(class_serializer.data)
        else:
            return Response(class_serializer.errors)


class SectionView(APIView):
    def get_section_organization(self, organization):
        try:
            sections = Section.objects.filter(section_class__organization=organization)
            print(sections)
            return sections
        except Section.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        sections = self.get_section_organization(pk)
        sections_serializer = SectionSerializer(sections, many=True)
        return Response(sections_serializer.data)

class SectionByClassView(APIView):
    def get_section_class(self, section_class):
        try:
            sections = Section.objects.filter(section_class=section_class)
            print(sections)
            return sections
        except Section.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        sections = self.get_section_class(pk)
        sections_serializer = SectionSerializer(sections, many=True)
        return Response(sections_serializer.data)


class CourseView(APIView):
    def get_course_organization(self, organization):
        try:
            courses = Course.objects.filter(organization=organization)
            print(courses)
            return courses
        except Course.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        courses = self.get_course_organization(pk)
        courses_serializer = CourseSerializer(courses, many=True)
        return Response(courses_serializer.data)

class NewSectionView(APIView):
    def increment_section(self, classid):
        classobject = Class.objects.get(id=classid)
        classobject.num_sections += 1
        classobject.save()

    def post(self, request):
        section_serializer = SectionSerializer(data=request.data)
        if section_serializer.is_valid():
            section_serializer.save()
            self.increment_section(request.data['section_class'])
            return Response(section_serializer.data)
        else:
            return Response(section_serializer.errors)

@method_decorator(transaction.non_atomic_requests, name='dispatch')
class StudentProfile(APIView):
    #authentication_classes = (OAuth2AuthenticationAllowInactiveUser,JwtAuthentication)
    #permission_classes = (IsAuthenticated,)

    def get_school_students(self, school):
        try:
            user_mini_profile = UserMiniProfile.objects.filter(school=school, is_staff=False)
            print(user_mini_profile)
            return user_mini_profile
        except UserMiniProfile.DoesNotExist:
            raise Http404

    def get_user_school(self, organization):
        try:
            return School.objects.get(organization=organization)
        except School.DoesNotExist:
            return None

    def get(self, request, pk):
        print(pk)
        user_mini_profile = self.get_school_students(pk)
        user_mini_serializer = UserMiniProfileSerializer(user_mini_profile, many=True)
        return Response(user_mini_serializer.data)


    def get_object(self, pk):
        try:
            return UserMiniProfile.objects.get(pk=pk)
        except UserMiniProfile.DoesNotExist:
            raise Http404
    def put(self, request, pk):
        student = self.get_object(pk)
        serializer = UserMiniProfileSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(transaction.non_atomic_requests, name='dispatch')
class StudentNewProfile(APIView):
    authentication_classes = (OAuth2AuthenticationAllowInactiveUser,JwtAuthentication)
    permission_classes = (IsAuthenticated,)


    def post(self, request):
        """Creates a new user account for the site that calls this view
        To use, perform a token authenticated POST to the URL::
            /tahoe/api/v1/registrations/
        Required arguments (JSON data):
            "username"
            "email"
            "name"
        Optional arguments:
            "password"
            "send_activation_email"
        Returns:
            HttpResponse: 200 on success, {"user_id ": 9}
            HttpResponse: 400 if the request is not valid.
            HttpResponse: 409 if an account with the given username or email
                address already exists
        The code here is adapted from the LMS ``appsembler_api`` bulk registration
        code. See the ``appsembler/ginkgo/master`` branch
        """
        data = request.data
        password_provided = 'password' in data

        # set the honor_code and honor_code like checked,
        # so we can use the already defined methods for creating an user
        data['honor_code'] = "True"
        data['terms_of_service'] = "True"

        if password_provided:
            if 'send_activation_email' in data and data['send_activation_email'] == "False":
                data['send_activation_email'] = False
            else:
                data['send_activation_email'] = True
        else:
            data['password'] = create_password()
            data['send_activation_email'] = False

        email = request.data.get('email')
        username = request.data.get('username')

        # Handle duplicate email/username
        conflicts = check_account_exists(email=email, username=username)
        if conflicts:
            errors = {"user_message": "User already exists"}
            return Response(errors, status=409)

        try:
            user = create_account_with_params(
                request=request,
                params=data,
                send_activation_email_flag=data['send_activation_email'])
            # set the user as active if password is provided
            # meaning we don't have to send a password reset email
            user.is_active = password_provided
            user.save()
            if not password_provided:
                success = send_password_reset_email(request)
                if not success:
                    log.error('Tahoe Reg API: Error sending password reset '
                              'email to user {}'.format(user.username))
        except ValidationError as err:
            log.error('ValidationError. err={}'.format(err))
            # Should only get non-field errors from this function
            assert NON_FIELD_ERRORS not in err.message_dict
            # Only return first error for each field

            # TODO: Let's give a clue as to which are the error causing fields
            errors = {
                "user_message": "Invalid parameters on user creation"
            }
            return Response(errors, status=400)
        data['is_staff'] = "False"
        data['user'] = user.id
        data['birthday'] = data['birthday'][:10]
        print(data)
        user_mini_profile = UserMiniProfileSerializer(data = data)
        if user_mini_profile.is_valid():
            user_mini_profile.save()
        else:
            print(user_mini_profile.errors)
        user_section_mapping_serializer = UserSectionMappingSerializer(data=data)
        if user_section_mapping_serializer.is_valid():
            user_section_mapping_serializer.save()
        return Response({'user':user_mini_profile.data, 'user_section':user_section_mapping_serializer.data}, status=200)

class NewTeacherEnrollView(APIView):

    def post(self, request):
        data = request.data
        user_id = data['user_id']
        destination_course_key_string = data['destination_course_key']
        destination_course_key = CourseKey.from_string(destination_course_key_string)
        user = User.objects.get(id=user_id)
        enrollment = CourseEnrollment.enroll(user, destination_course_key)
        # add course intructor and staff roles to the new user
        CourseInstructorRole(destination_course_key).add_users(user)
        CourseStaffRole(destination_course_key).add_users(user)
        enrollment_serializer = CourseEnrollmentSerializer(enrollment)
        return Response(enrollment_serializer.data,
                        status=200)


class TeacherEnrollView(APIView):

    def get(self, request, course_key):
        destination_course_key = CourseKey.from_string(course_key)
        data = CourseInstructorRole(destination_course_key).users_with_role()
        print(data)
        user_mini_profile = UserMiniProfile.objects.filter(user_id__in=data)
        print(user_mini_profile)
        teachers_data = UserMiniProfileSerializer(user_mini_profile, many=True)
        return Response(teachers_data.data,
                        status=200)



class NewStudentEnrollView(APIView):

    def post(self, request):
        data = request.data
        user_id = data['user_id']
        destination_course_key_string = data['destination_course_key']
        destination_course_key = CourseKey.from_string(destination_course_key_string)
        user = User.objects.get(id=user_id)
        enrollment = CourseEnrollment.enroll(user, destination_course_key)
        enrollment_serializer = CourseEnrollmentSerializer(enrollment)
        return Response(enrollment_serializer.data,
                        status=200)

class BulkNewStudentEnrollView(APIView):
    def post(self, request):
        data = request.data
        user_ids = data['user_ids']
        for user_id in user_ids:
            destination_course_key_string = data['destination_course_key']
            destination_course_key = CourseKey.from_string(destination_course_key_string)
            user = User.objects.get(id=user_id)
            enrollment = CourseEnrollment.enroll(user, destination_course_key)
            enrollment_serializer = CourseEnrollmentSerializer(enrollment)
        return Response({'success':True},
                        status=200)

class SectionBulkNewStudentEnrollView(APIView):
    def post(self, request):
        data = request.data
        destination_course_key_string = data['destination_course_key']
        destination_course_key = CourseKey.from_string(destination_course_key_string)
        section = data['section']
        user_ids = UserSectionMapping.objects.filter(section=section).values_list('user',flat=True)
        for user_id in user_ids:
            user = User.objects.get(id=user_id)
            enrollment = CourseEnrollment.enroll(user, destination_course_key)
            print(enrollment)
        return Response({'success':True},
                        status=200)


class StudentEnrollView(APIView):
    def get(self, request, course_key):
        destination_course_key = CourseKey.from_string(course_key)
        users = CourseEnrollment.objects.filter(course=destination_course_key).values_list('user',flat=True)
        print(users)
        user_mini_profile =  UserMiniProfile.objects.filter(user_id__in=users)
        print(user_mini_profile)
        students_data = UserMiniProfileSerializer(user_mini_profile, many=True)
        return Response(students_data.data,
                        status=200)


class BulkNewStudentsView(APIView):
    def post(self, request):
        print(request.data)
        users = request.data['users']
        school = request.data['school']
        print(type(users))
        import ast
        users = ast.literal_eval(users)
        for user in users:
            try:
                with transaction.atomic():
                    user_model = User.objects.create_user(user['username'], user['email'], user['password'])
                    profile = UserProfile(user=user_model)
                    profile.name = user['name']
                    profile.save()
            except IntegrityError as e:
                user_model = User.objects.get(username=user['username'])
            data = user
            data['is_staff'] = "False"
            data['school'] = school
            data['user'] = user_model.id
            data['birthday'] = data['birthday'][:10]
            #print(data)
            user_model.is_active = True
            user_model.save()
            user_mini_profile = UserMiniProfileSerializer(data=data)
            #print(user_mini_profile)
            if user_mini_profile.is_valid():
                try:
                    with transaction.atomic():
                        user_mini_profile.save()
                except IntegrityError as e:
                    continue
            else:
                print(user_mini_profile.errors)
            print(data)
            user_section_mapping_serializer = UserSectionMappingSerializer(data=data)
            if user_section_mapping_serializer.is_valid():
                user_section_mapping_serializer.save()
            else:
                print(user_section_mapping_serializer.errors)
        return Response({'success': True},
                            status=200)


class ProgressLeaderBoard(APIView):
    def get(self, request):
        user = request.user
        engagementscores = StudentSocialEngagementProgressClassScore()
        class_id = None
        user_section = None
        user_section_relation = user.section
        user_engagement_score = 0
        class_average_score = 0
        user_position = None
        leader_board = None
        if user_section_relation:
            user_section = user_section_relation.section
        if user_section and user_section.section_class:
            class_id = user_section.section_class
        if class_id:
            user_engagement_score = engagementscores.get_user_engagement_score(class_id, user.id)
            if user_engagement_score == None:
                user_engagement_score = 0
            class_average_score = engagementscores.get_class_average_engagement_score(class_id)
            if class_average_score == None:
                class_average_score = 0
            user_position = engagementscores.get_user_leaderboard_position(class_id, user_id=user.id)
            if user_position == None:
                user_position = 0
            leaderboard = engagementscores.generate_leaderboard(class_id, count=10)
            print(leaderboard)
            return Response({'user_engagement_score': user_engagement_score, 'class_average_score': class_average_score,
                             'user_position': user_position, 'leaderboard': leaderboard},
                            status=200)

from django.views import View
class ProductsView(View):
    template_name = 'products.html'
    def get(self, request, *args, **kwargs):
        return render_to_response(self.template_name)

class SEPView(View):
    template_name = 'student_engagement.html'
    def get(self, request, *args, **kwargs):
        return render_to_response(self.template_name)

class SocialWallView(View):
    template_name = 'social_wall.html'
    def get(self, request, *args, **kwargs):
        return render_to_response(self.template_name)

class ExtraContentView(View):
    template_name = 'extra_content.html'
    def get(self, request, *args, **kwargs):
        return render_to_response(self.template_name)


