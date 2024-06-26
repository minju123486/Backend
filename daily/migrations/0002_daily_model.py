# Generated by Django 4.0.3 on 2024-05-20 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daily', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='daily_model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=50)),
                ('content', models.CharField(max_length=10000)),
                ('title', models.CharField(max_length=200)),
                ('year', models.IntegerField()),
                ('month', models.IntegerField()),
                ('day', models.IntegerField()),
                ('hour', models.IntegerField()),
                ('minute', models.IntegerField()),
            ],
        ),
    ]
