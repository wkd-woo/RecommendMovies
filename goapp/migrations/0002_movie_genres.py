# Generated by Django 3.2.1 on 2021-05-19 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='genres',
            field=models.CharField(max_length=300, null=True),
        ),
    ]