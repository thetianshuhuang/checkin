# Generated by Django 2.2.4 on 2019-09-07 02:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_token', models.TextField()),
                ('share_token', models.TextField()),
                ('start', models.FloatField(null=True)),
                ('end', models.FloatField(null=True)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_id', models.CharField(max_length=50)),
                ('parent', models.CharField(max_length=50, null=True)),
                ('name', models.TextField(null=True)),
                ('desc', models.TextField(null=True)),
                ('node_id', models.CharField(max_length=50, null=True)),
                ('type', models.CharField(max_length=10, null=True)),
                ('start', models.FloatField(null=True)),
                ('end', models.FloatField(null=True)),
                ('meta', models.TextField(null=True)),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Program')),
            ],
        ),
        migrations.CreateModel(
            name='QueuedRecord',
            fields=[
                ('record_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.Record')),
            ],
            bases=('api.record',),
        ),
    ]
