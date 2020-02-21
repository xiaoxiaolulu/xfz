# Generated by Django 3.0.2 on 2020-02-21 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xfzauth', '0002_auto_20200221_2219'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='uuid',
            new_name='uid',
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=200),
        ),
    ]