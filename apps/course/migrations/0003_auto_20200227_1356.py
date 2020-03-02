# Generated by Django 3.0.2 on 2020-02-27 05:56

from django.db import migrations
import shortuuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_courseorder'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='courseorder',
            name='id',
        ),
        migrations.AddField(
            model_name='courseorder',
            name='uuid',
            field=shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22, primary_key=True, serialize=False),
        ),
    ]
