# Generated by Django 5.1.4 on 2024-12-20 06:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chat',
            old_name='respomse',
            new_name='response',
        ),
    ]
