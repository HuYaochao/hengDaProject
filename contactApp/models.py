from django.db import models
from django.utils import timezone
from datetime import datetime

# Create your models here.
class Ad(models.Model):
    title = models.CharField(max_length=50, verbose_name='招聘岗位')
    description = models.TextField(verbose_name='岗位要求')
    publishDate = models.DateTimeField(max_length=20,
                                       default=timezone.now,
                                       verbose_name='发布时间')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '招聘广告'
        verbose_name_plural = '招聘广告'
        ordering = ('-publishDate', )

class Resume(models.Model):
    name = models.CharField(max_length=20, verbose_name='姓名')
    personID = models.CharField(max_length=30, verbose_name='身份证号')
    sex = models.CharField(max_length=5, default='男', verbose_name='性别')
    email = models.EmailField(max_length=30, verbose_name='邮箱')
    birth = models.DateField(max_length=20,
                             default=datetime.strftime(datetime.now(),
                                                       "%Y-%m-%d"),
                             verbose_name='出生日期')
    edu = models.CharField(max_length=5, default='本科', verbose_name='学历')
    school = models.CharField(max_length=40, verbose_name='毕业院校')
    major = models.CharField(max_length=40, verbose_name='专业')
    position = models.CharField(max_length=40, verbose_name='申请职位')
    experience = models.TextField(blank=True,
                                  null=True,
                                  verbose_name='学习或工作经历')
    photo = models.ImageField(upload_to='contact/recruit/%Y_%m_%d',
                              verbose_name='个人照片')
    grade_list = (
        (1, '未审'),
        (2, '通过'),
        (3, '未通过'),
    )
    status = models.IntegerField(choices=grade_list,
                                 default=1,
                                 verbose_name='面试成绩')
    publishDate = models.DateTimeField(max_length=20,
                                       default=timezone.now,
                                       verbose_name='提交时间')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '简历'
        verbose_name_plural = '简历'
        ordering = ('-status', '-publishDate')


from django.db.models.signals import post_init,post_save
from django.dispatch import receiver
from django.core.mail import send_mail
import os
from docxtpl import DocxTemplate
from docxtpl import InlineImage
from docx.shared import Mm, Inches, Pt
 
@receiver(post_init, sender=Resume)
def before_save_resume(sender, instance, **kwargs):
    instance.__original_status = instance.status

@receiver(post_save, sender=Resume) 
def post_save_resume(sender, instance, **kwargs):
    print(instance.__original_status)
    print(instance.status)
    email = instance.email   # 应聘者邮箱
    EMAIL_FROM = '1723856501@qq.com'   # 企业qq邮箱
    if instance.__original_status == 1 and instance.status == 2:
        template_path = os.getcwd()+ '/media/recruit.docx'   # 模板文件
        template = DocxTemplate(template_path)  # 建立模板文件
        # 从instance实例中获取当前简历字段信息
        name = instance.name
        personID = instance.personID
        sex = instance.sex
        email = instance.email
        birth = instance.birth
        school = instance.school
        major = instance.major
        position = instance.position
        experience = instance.experience
        photo = instance.photo
        edu = instance.edu

        context = {
            'name': name,
            'personID': personID,
            'sex': sex,
            'email': email,
            'birth': birth,
            'school': school,
            'major': major,
            'position': position,
            'experience': experience,
            'edu': edu,
            'photo': InlineImage(template, photo, width=Mm(30), height=Mm(40)),
        }
        template.render(context)
        filename = '%s/media/contact/recruit/%s_%d.docx' % (
            os.getcwd(), instance.name, instance.id)
        template.save(filename)

        email_title = '通知：恒达科技招聘初试结果'
        email_body = '恭喜您通过本企业初试'
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])    
    elif instance.__original_status == 1 and instance.status == 3:
        email_title = '通知：恒达科技招聘初试结果'
        email_body = '很遗憾，您未能通过本企业初试，感谢您的关注'
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])