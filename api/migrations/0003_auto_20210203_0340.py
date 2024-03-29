# Generated by Django 3.1.6 on 2021-02-02 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20210203_0337'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='follow',
            name='unique',
        ),
        migrations.RenameField(
            model_name='follow',
            old_name='author',
            new_name='following',
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('user', 'following'), name='unique'),
        ),
    ]
