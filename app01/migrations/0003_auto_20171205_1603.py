# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-05 08:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_auto_20171204_1854'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'verbose_name_plural': '回卷表'},
        ),
        migrations.AlterModelOptions(
            name='classlist',
            options={'verbose_name_plural': '班级列表'},
        ),
        migrations.AlterModelOptions(
            name='option',
            options={'verbose_name_plural': '单选题选项'},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'verbose_name_plural': '问题表'},
        ),
        migrations.AlterModelOptions(
            name='questionnaire',
            options={'verbose_name_plural': '问卷调查表'},
        ),
        migrations.AlterModelOptions(
            name='student',
            options={'verbose_name_plural': '学生列表'},
        ),
        migrations.AlterModelOptions(
            name='userinfo',
            options={'verbose_name_plural': '员工表'},
        ),
        migrations.AlterField(
            model_name='answer',
            name='option',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.Option', verbose_name='所回答的问题'),
        ),
        migrations.AlterField(
            model_name='option',
            name='qs',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Question', verbose_name='管理问题'),
        ),
        migrations.AlterField(
            model_name='questionnaire',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.UserInfo', verbose_name='创建人'),
        ),
        migrations.AlterField(
            model_name='questionnaire',
            name='question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.Question', verbose_name='问题内容'),
        ),
    ]