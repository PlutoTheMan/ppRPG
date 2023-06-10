# Generated by Django 4.2.1 on 2023-06-08 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('characters', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Guild',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, unique=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('leader', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='characters.character')),
                ('members', models.ManyToManyField(related_name='guild_members', to='characters.character')),
                ('pending_invites', models.ManyToManyField(related_name='guild_invites', to='characters.character')),
            ],
        ),
    ]
