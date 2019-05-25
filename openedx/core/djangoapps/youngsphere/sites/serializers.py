from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from opaque_keys.edx.locator import CourseLocator
from rest_framework import serializers
from organizations import api as organizations_api
from organizations.models import Organization

from openedx.core.djangoapps.site_configuration.models import SiteConfiguration
from openedx.core.djangoapps.youngsphere.sites.tasks import clone_course
from .models import School, Class, Section, Course, UserMiniProfile, UserSectionMapping, Page, Follow, GlobalGroup, \
    FeedModerator
from .utils import sass_to_dict, dict_to_sass, bootstrap_site


class SASSDictField(serializers.DictField):
    def to_internal_value(self, data):
        return dict_to_sass(data)

    def to_representation(self, value):
        return sass_to_dict(value)


class SiteConfigurationSerializer(serializers.ModelSerializer):
    values = serializers.DictField()
    #YoungSphere Later Stages
    #sassVariables = serializers.ListField(source='sass_variables')
    #pageElements = serializers.DictField(source='page_elements')

    class Meta:
        model = SiteConfiguration
        fields = ('id', 'values')

    def update(self, instance, validated_data):
        object = super(SiteConfigurationSerializer, self).update(instance, validated_data)
        return object


class SiteConfigurationListSerializer(SiteConfigurationSerializer):
    class Meta(SiteConfigurationSerializer.Meta):
        fields = ('id', 'name', 'domain')




class SiteSerializer(serializers.ModelSerializer):
    configuration = SiteConfigurationSerializer(read_only=True)
    #customDomainStatus = serializers.SerializerMethodField('custom_domain_status', read_only=True)

    class Meta:
        model = Site
        fields = ('id', 'name', 'domain', 'configuration')

    def create(self, validated_data):
        site = super(SiteSerializer, self).create(validated_data)
        organization, site, user = bootstrap_site(site)
        return site



class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('id', 'name', 'short_name', 'edx_uuid')

    def create(self, validated_data):
        return organizations_api.add_organization(**validated_data)


class RegistrationSerializer(serializers.Serializer):
    site = SiteSerializer()
    organization = OrganizationSerializer()
    user_email = serializers.EmailField(required=False)
    password = serializers.CharField(required=False)
    initial_values = serializers.DictField(required=False)

    def create(self, validated_data):
        site_data = validated_data.pop('site')
        site = Site.objects.create(**site_data)
        organization_data = validated_data.pop('organization')
        user_email = validated_data.pop('user_email', None)
        organization, site, user = bootstrap_site(site, organization_data, user_email)
        site_configuration = site.configuration
        initial_values = validated_data.get('initial_values', {})
        if initial_values:
            site_configuration.values['SITE_NAME'] = site.domain
            site_configuration.values['platform_name'] = initial_values.get('platform_name')
            site_configuration.values['logo_positive'] = initial_values.get('logo_positive')
            site_configuration.values['logo_negative'] = initial_values.get('logo_negative')
            site_configuration.values['primary-font'] = initial_values.get('font')
            site_configuration.values['accent-font'] = 'Delius Unicase'
            site_configuration.values['page_status'] = {
                'about': True,
                'blog': True,
                'contact': True,
                'copyright': True,
                'donate': False,
                'embargo': False,
                'faq': True,
                'help': True,
                'honor': True,
                'jobs': False,
                'news': True,
                'press': True,
                'privacy': True,
                'tos': True
            }
            #YoungSphere Later stages
            # site_configuration.set_sass_variables({
            #     '$brand-primary-color': initial_values.get('primary_brand_color'),
            #     '$base-text-color': initial_values.get('base_text_color'),
            #     '$cta-button-bg': initial_values.get('cta_button_bg'),
            #     '$primary-font-name': '"{}"'.format(initial_values.get('font')),
            #     '$accent-font-name': '"Delius Unicase"',
            # })
            site_configuration.save()

        # clone course
        if settings.CLONE_COURSE_FOR_NEW_SIGNUPS:
            source_course_locator = CourseLocator.from_string(settings.COURSE_TO_CLONE)
            destination_course_locator = CourseLocator(organization.name, 'My first course', '2017')
            clone_course.apply_async(
                (unicode(source_course_locator), unicode(destination_course_locator), user.id),
                queue="edx.core.cms.high"
            )
        return {
            'site': site,
            'organization': organization,
            'user_email': user_email,
            'password': 'hashed',
            'initial_values': initial_values,
        }


class SchoolSerializer(serializers.ModelSerializer):
    organization = serializers.SlugRelatedField(queryset=Organization.objects.all(), slug_field='name')
    class Meta:
        model = School
        fields = ('id','organization', 'schoolname', 'principal', 'email', 'contact_number', 'address', 'website', 'board', 'schoollogo')


class ClassSerializer(serializers.ModelSerializer):
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all())

    class Meta:
        model = Class
        fields = ('id','organization','class_level', 'display_name', 'num_sections')


class SectionSerializer(serializers.ModelSerializer):
    section_class = serializers.PrimaryKeyRelatedField(queryset=Class.objects.all())
    section_class_level = serializers.ReadOnlyField(source='section_class.class_level')
    class Meta:
        model = Section
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all())
    course_class = serializers.PrimaryKeyRelatedField(queryset=Class.objects.all())
    course_section = serializers.PrimaryKeyRelatedField(queryset=Section.objects.all())

    class Meta:
        model = Course
        fields = '__all__'


class UserMiniProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    birthday = serializers.DateField(format="%d/%m/%Y")
    class Meta:
        model = UserMiniProfile
        fields = '__all__'


class UserSectionMappingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    section = serializers.PrimaryKeyRelatedField(queryset=Section.objects.all())

    class Meta:
        model = UserSectionMapping
        fields = '__all__'


class UserMiniReadOnlyProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    school = serializers.SlugRelatedField(read_only=True,
                                          source='school.page_id',
        slug_field='pageid')
    birthday = serializers.DateField(format="%d/%m/%Y")

    class Meta:
        model = UserMiniProfile
        fields = '__all__'


class UserSectionMappingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    section = serializers.PrimaryKeyRelatedField(queryset=Section.objects.all())

    class Meta:
        model = UserSectionMapping
        fields = '__all__'


class GlobalGroupSerializer(serializers.ModelSerializer):
    page_id = serializers.PrimaryKeyRelatedField(queryset=Page.objects.all())
    class Meta:
        model = GlobalGroup
        fields = '__all__'


class SchoolGroupSerializer(serializers.ModelSerializer):
    page_id = serializers.PrimaryKeyRelatedField(queryset=Page.objects.all())
    school = serializers.PrimaryKeyRelatedField(queryset=School.objects.all())
    globalgroup = serializers.PrimaryKeyRelatedField(queryset=GlobalGroup.objects.all())
    class Meta:
        model = School
        fields = '__all__'


class CourseGroupSerializer(serializers.ModelSerializer):
    page_id = serializers.PrimaryKeyRelatedField(queryset=Page.objects.all())
    school = serializers.PrimaryKeyRelatedField(queryset=School.objects.all())
    cousre_id = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    class Meta:
        model = Course
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    from_page = serializers.PrimaryKeyRelatedField(queryset=Page.objects.all())
    to_page = serializers.PrimaryKeyRelatedField(queryset=Page.objects.all())
    class Meta:
        model = Follow
        fields = '__all__'


class FriendSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    email = serializers.EmailField()
    birthday = serializers.DateField(format="%d/%m/%Y")
    username = serializers.CharField()
    schoolname = serializers.CharField()
    classname = serializers.CharField()
    section = serializers.CharField()
    name = serializers.CharField()
    is_staff = serializers.CharField()


class FeedModeratorSerializer(serializers.ModelSerializer):
    page = serializers.PrimaryKeyRelatedField(queryset=Page.objects.all())
    moderator = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = FeedModerator
        fields = '__all__'
