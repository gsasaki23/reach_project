# Generated by Django 2.2 on 2020-02-26 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reach_app', '0013_auto_20200226_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='contact',
            name='phone',
            field=models.CharField(default='', max_length=255),
        ),
    ]