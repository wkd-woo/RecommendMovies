# Generated by Django 3.2.1 on 2021-05-26 16:24

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('analysisapp', '0005_alter_results_user_id'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='results',
            managers=[
                ('resultDF', django.db.models.manager.Manager()),
            ],
        ),
        migrations.RemoveField(
            model_name='results',
            name='resultDF',
        ),
    ]