# Generated by Django 4.0.1 on 2022-01-11 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=100)),
                ('thumbnail_url', models.URLField(max_length=2000)),
                ('release_date', models.DateField()),
            ],
            options={
                'db_table': 'movies',
            },
        ),
    ]
