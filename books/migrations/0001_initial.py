# Generated by Django 4.0.5 on 2022-06-21 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('isbn', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('author', models.TextField()),
                ('book_title', models.TextField()),
                ('book_info', models.TextField()),
                ('library_name', models.TextField()),
                ('price', models.TextField()),
                ('category', models.TextField()),
            ],
            options={
                'db_table': 'books',
            },
        ),
    ]