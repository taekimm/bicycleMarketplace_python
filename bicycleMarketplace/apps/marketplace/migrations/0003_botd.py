# Generated by Django 2.0.1 on 2018-02-01 22:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0002_bike_imgid'),
    ]

    operations = [
        migrations.CreateModel(
            name='BotD',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('bike', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='marketplace.Bike')),
            ],
        ),
    ]