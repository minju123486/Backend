# Generated by Django 4.0.3 on 2024-05-19 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='feedback_list',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30)),
                ('coursename', models.CharField(max_length=30)),
                ('feedback', models.CharField(max_length=1000, null=True)),
                ('year', models.IntegerField()),
                ('month', models.IntegerField()),
                ('day', models.IntegerField()),
                ('count', models.IntegerField()),
                ('cnt', models.IntegerField()),
                ('correct_count', models.CharField(max_length=30)),
                ('problem_1', models.CharField(max_length=1000, null=True)),
                ('problem_2', models.CharField(max_length=1000, null=True)),
                ('problem_3', models.CharField(max_length=1000, null=True)),
                ('problem_4', models.CharField(max_length=1000, null=True)),
                ('problem_5', models.CharField(max_length=1000, null=True)),
                ('problem_6', models.CharField(max_length=1000, null=True)),
                ('problem_7', models.CharField(max_length=1000, null=True)),
                ('problem_8', models.CharField(max_length=1000, null=True)),
                ('problem_9', models.CharField(max_length=1000, null=True)),
                ('problem_10', models.CharField(max_length=1000, null=True)),
            ],
        ),
    ]
