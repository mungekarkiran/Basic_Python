# Generated by Django 2.2.4 on 2020-12-30 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmpInfo', '0002_auto_20201230_1301'),
    ]

    operations = [
        migrations.AddField(
            model_name='emp',
            name='age',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='emp',
            name='experience',
            field=models.FloatField(),
        ),
    ]