# Generated by Django 2.2.4 on 2020-12-28 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LoginReg', '0004_auto_20201228_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newusers',
            name='gender',
            field=models.CharField(max_length=10),
        ),
    ]