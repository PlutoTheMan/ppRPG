# Generated by Django 4.2.1 on 2023-05-29 21:04

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('banned', models.BooleanField(default=False)),
                ('vocation', models.IntegerField(choices=[(0, 'No Vocation'), (1, 'Warrior'), (2, 'Mage')], default=0)),
                ('level', models.IntegerField(default=1)),
                ('experience', models.IntegerField(default=0)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('pos_x', models.IntegerField(default=7)),
                ('pos_y', models.IntegerField(default=9)),
                ('logged_in_game', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('slot', models.IntegerField(choices=[(0, 'Left Hand'), (1, 'Right Hand'), (2, 'Helm'), (3, 'Chest'), (4, 'Legs'), (5, 'Boots'), (6, 'Belt'), (7, 'Ring'), (8, 'Amulet')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Skills',
            fields=[
                ('character', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='characters.character')),
                ('fist', models.CharField(default=1, max_length=4)),
                ('sword', models.CharField(default=1, max_length=4)),
                ('club', models.CharField(default=1, max_length=4)),
                ('axe', models.CharField(default=1, max_length=4)),
                ('shielding', models.CharField(default=1, max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='Favourites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favourites', models.ManyToManyField(to='characters.character')),
            ],
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('character', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='characters.character')),
                ('amulet', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='amulet', to='characters.item')),
                ('belt', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='belt', to='characters.item')),
                ('boots', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='boots', to='characters.item')),
                ('left_hand', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='left_hand', to='characters.item')),
                ('legs', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='legs', to='characters.item')),
                ('right_hand', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='right_hand', to='characters.item')),
                ('ring', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ring', to='characters.item')),
            ],
        ),
    ]
