# Generated by Django 4.2.4 on 2023-11-25 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pereval', '0008_rename_author_perevaladded_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='mail',
            field=models.EmailField(max_length=254, verbose_name='почта'),
        ),
    ]
