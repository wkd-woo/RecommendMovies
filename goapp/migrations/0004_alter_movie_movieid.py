# Generated by Django 3.2.1 on 2021-05-19 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goapp', '0003_auto_20210520_0230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='movieId',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]
