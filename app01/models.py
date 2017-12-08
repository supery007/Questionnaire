from django.db import models


class UserInfo(models.Model):
    """
    员工表
    """
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = '员工表'

    def __str__(self):
        return self.username


class ClassList(models.Model):
    """
    班级表
    """
    title = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = '班级列表'

    def __str__(self):
        return self.title


class Student(models.Model):
    """
    学生表
    """
    user = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)
    cls = models.ForeignKey(to='ClassList')

    class Meta:
        verbose_name_plural = '学生列表'

    def __str__(self):
        return self.user


class Questionnaire(models.Model):
    """
    问卷表
    """
    title = models.CharField(max_length=64)
    cls = models.ForeignKey(to=ClassList,verbose_name='所调查问卷班级')
    creator = models.ForeignKey(to='UserInfo',verbose_name='创建人')

    count_answer = models.IntegerField(default=0,verbose_name='统计回答问卷的学生数')



    class Meta:
        verbose_name_plural = '问卷调查表'

    def __str__(self):
        return self.title


class Question(models.Model):
    """
    问题
    """
    caption = models.CharField(max_length=64, verbose_name='问题内容')

    question_types = (
        (1, '打分'),
        (2, '单选'),
        (3, 'c'),
    )
    tp = models.IntegerField(choices=question_types)
    naire = models.ForeignKey(to=Questionnaire, default=1)
    class Meta:
        verbose_name_plural = '问题表'

    def __str__(self):
        return self.caption


class Option(models.Model):
    """
    单选题的选项
    """
    name = models.CharField(verbose_name='选项名称', max_length=32)
    score = models.IntegerField(verbose_name='选项对应的分值')
    qs = models.ForeignKey(to='Question', verbose_name='管理问题')

    class Meta:
        verbose_name_plural = '单选题选项'

    def __str__(self):
        return self.name


class Answer(models.Model):
    """
    回答
    """
    stu = models.ForeignKey(to='Student')
    question = models.ForeignKey(to='Question')

    option = models.ForeignKey(to="Option", null=True, blank=True,verbose_name='所回答的问题')
    val = models.IntegerField(null=True, blank=True)
    content = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = '回卷表'

