# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-03-08 11:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organizations', '0009_merge_20181113_1517_appsembler'),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_level', models.CharField(max_length=5)),
                ('display_name', models.CharField(max_length=10)),
                ('num_sections', models.IntegerField(default=0)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.Organization')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('course_name', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.CharField(blank=True, max_length=144, null=True)),
                ('year', models.IntegerField(default=2020)),
                ('courseno', models.CharField(blank=True, max_length=50, null=True)),
                ('courserun', models.CharField(blank=True, max_length=30, null=True)),
                ('course_id', models.CharField(default=b'default_course', max_length=80, primary_key=True, serialize=False)),
                ('course_status', models.CharField(blank=True, max_length=3, null=True)),
                ('course_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='youngsphere_sites.Class')),
            ],
        ),
        migrations.CreateModel(
            name='CourseGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=400)),
                ('course_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course_group', to='youngsphere_sites.Course')),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organization_course_groups', to='organizations.Organization')),
            ],
        ),
        migrations.CreateModel(
            name='FeedModerator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of_page', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification', jsonfield.fields.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('pageid', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('ownertype', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schoolname', models.CharField(blank=True, max_length=50, null=True)),
                ('principal', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('contact_number', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('website', models.CharField(blank=True, max_length=50, null=True)),
                ('board', models.CharField(blank=True, max_length=20, null=True)),
                ('schoollogo', models.ImageField(blank=True, default=b'school_logo/no-image.jpg', upload_to=b'school_logo')),
                ('school_feed', models.BooleanField(default=False)),
                ('organization', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='school_profile', to='organizations.Organization')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_name', models.CharField(max_length=5)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('section_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='youngsphere_sites.Class')),
            ],
        ),
        migrations.CreateModel(
            name='UnReadNotificationCount',
            fields=[
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('unread_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='UserMiniProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('first_name', models.CharField(blank=True, max_length=40, null=True)),
                ('last_name', models.CharField(blank=True, max_length=40, null=True)),
                ('gender', models.CharField(blank=True, max_length=1, null=True)),
                ('email', models.CharField(blank=True, max_length=40, null=True)),
                ('contact_number', models.CharField(blank=True, max_length=40, null=True)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('is_staff', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='UserSectionMapping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='youngsphere_sites.Section')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='section', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GlobalGroup',
            fields=[
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=400)),
                ('page_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='globalgroup', serialize=False, to='youngsphere_sites.Page')),
            ],
        ),
        migrations.CreateModel(
            name='SchoolGroup',
            fields=[
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=400)),
                ('page_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='schoolgroup', serialize=False, to='youngsphere_sites.Page')),
                ('globalgroup', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organizationgroups', to='youngsphere_sites.GlobalGroup')),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='organization_groups', to='organizations.Organization')),
            ],
        ),
        migrations.AddField(
            model_name='userminiprofile',
            name='page_id',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to='youngsphere_sites.Page'),
        ),
        migrations.AddField(
            model_name='userminiprofile',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='youngsphere_sites.School', to_field=b'organization'),
        ),
        migrations.AddField(
            model_name='school',
            name='page_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='school', to='youngsphere_sites.Page'),
        ),
        migrations.AddField(
            model_name='notification',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='follow',
            name='from_page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_follow', to='youngsphere_sites.Page'),
        ),
        migrations.AddField(
            model_name='follow',
            name='to_page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_follow', to='youngsphere_sites.Page'),
        ),
        migrations.AddField(
            model_name='feedmoderator',
            name='moderator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='page_moderated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='feedmoderator',
            name='page',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='moderators', to='youngsphere_sites.Page'),
        ),
        migrations.AddField(
            model_name='coursegroup',
            name='page_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='coursegroup', to='youngsphere_sites.Page'),
        ),
        migrations.AddField(
            model_name='course',
            name='course_section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='youngsphere_sites.Section'),
        ),
        migrations.AddField(
            model_name='course',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations.Organization'),
        ),
        migrations.AddField(
            model_name='course',
            name='page_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course', to='youngsphere_sites.Page'),
        ),
    ]
