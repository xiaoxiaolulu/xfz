# Generated by Django 3.0.2 on 2020-02-23 15:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_banner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='banner',
            options={'ordering': ['-priority']},
        ),
        migrations.RenameField(
            model_name='banner',
            old_name='position',
            new_name='priority',
        ),
    ]
