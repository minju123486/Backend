# Generated by Django 4.0.3 on 2024-05-20 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0002_like_check'),
    ]

    operations = [
        migrations.CreateModel(
            name='grade_search',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('watch', models.IntegerField()),
                ('grade', models.CharField(max_length=50)),
                ('content', models.CharField(max_length=50)),
            ],
        ),
    ]