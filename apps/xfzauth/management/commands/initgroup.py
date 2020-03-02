from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, ContentType
from apps.course.models import Course, CourseCategory, Teacher, CourseOrder
from apps.news.models import News, NewCategory, Banner, Comment
from apps.payinfo.models import PayInfo, PayInfoOrder


class Command(BaseCommand):

    def handle(self, *args, **options):
        edit_content_type = [
            ContentType.objects.get_for_model(News),
            ContentType.objects.get_for_model(NewCategory),
            ContentType.objects.get_for_model(Banner),
            ContentType.objects.get_for_model(Comment),
            ContentType.objects.get_for_model(Course),
            ContentType.objects.get_for_model(CourseCategory),
            ContentType.objects.get_for_model(Teacher),
            ContentType.objects.get_for_model(PayInfo),
        ]

        edit_permissions = Permission.objects.filter(content_type__in=edit_content_type)
        editGroup = Group.objects.create(name='编辑')
        editGroup.permissions.set(edit_permissions)
        editGroup.save()
        self.stdout.write(self.style.SUCCESS('编辑分组创建成功'))

        finance_content_type = [
            ContentType.objects.get_for_model(CourseOrder),
            ContentType.objects.get_for_model(PayInfoOrder)
        ]
        finance_permissions = Permission.objects.filter(content_type__in=finance_content_type)
        financeGroup = Group.objects.create(name='财务')
        financeGroup.permissions.set(finance_permissions)
        financeGroup.save()
        self.stdout.write(self.style.SUCCESS('财务分组创建成功'))

        admin_permissions = edit_permissions.union(finance_permissions)
        adminGroup = Group.objects.create(name='管理员')
        adminGroup.permissions.set(admin_permissions)
        adminGroup.save()
        self.stdout.write(self.style.SUCCESS('管理员分组创建成功'))