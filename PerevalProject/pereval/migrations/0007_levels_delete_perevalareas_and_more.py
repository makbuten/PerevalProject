# Generated by Django 4.2.4 on 2023-11-25 15:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pereval', '0006_rename_id_images_perevalimages_images_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Levels',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('winter', models.CharField(choices=[('', 'не указано'), ('1A', '1a'), ('1B', '1б'), ('2А', '2а'), ('2В', '2б'), ('3А', '3а'), ('3В', '3б')], default='', max_length=2, verbose_name='зима')),
                ('summer', models.CharField(choices=[('', 'не указано'), ('1A', '1a'), ('1B', '1б'), ('2А', '2а'), ('2В', '2б'), ('3А', '3а'), ('3В', '3б')], default='', max_length=2, verbose_name='лето')),
                ('autumn', models.CharField(choices=[('', 'не указано'), ('1A', '1a'), ('1B', '1б'), ('2А', '2а'), ('2В', '2б'), ('3А', '3а'), ('3В', '3б')], default='', max_length=2, verbose_name='осень')),
                ('spring', models.CharField(choices=[('', 'не указано'), ('1A', '1a'), ('1B', '1б'), ('2А', '2а'), ('2В', '2б'), ('3А', '3а'), ('3В', '3б')], default='', max_length=2, verbose_name='весна')),
            ],
        ),
        migrations.DeleteModel(
            name='PerevalAreas',
        ),
        migrations.RemoveField(
            model_name='perevaladded',
            name='autumn',
        ),
        migrations.RemoveField(
            model_name='perevaladded',
            name='spring',
        ),
        migrations.RemoveField(
            model_name='perevaladded',
            name='summer',
        ),
        migrations.RemoveField(
            model_name='perevaladded',
            name='winter',
        ),
        migrations.AddField(
            model_name='images',
            name='pereval',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='pereval.perevaladded'),
        ),
        migrations.DeleteModel(
            name='PerevalImages',
        ),
        migrations.AddField(
            model_name='perevaladded',
            name='levels',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='pereval.levels'),
            preserve_default=False,
        ),
    ]
