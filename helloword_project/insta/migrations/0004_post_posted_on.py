# Generated by Django 3.0.8 on 2020-07-28 03:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Insta', '0003_auto_20200727_1742'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='posted_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
