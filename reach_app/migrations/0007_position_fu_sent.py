# Generated by Django 2.2 on 2020-02-25 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reach_app', '0006_position_ty_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='fu_sent',
            field=models.BooleanField(default=False),
        ),
    ]
