# Generated by Django 2.2.13 on 2021-12-19 04:42

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
            name='Meal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Meal_Addition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('price', models.FloatField(blank=True, null=True)),
                ('meal', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.Meal')),
            ],
        ),
        migrations.CreateModel(
            name='Meal_Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('meal', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.Meal')),
                ('meal_addition', models.ManyToManyField(blank=True, to='orders.Meal_Addition')),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=0)),
                ('meal_type', models.ManyToManyField(to='orders.Meal_Type')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Size')),
            ],
        ),
        migrations.AddField(
            model_name='meal_type',
            name='size',
            field=models.ManyToManyField(to='orders.Size'),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(default=0)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('meal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Meal')),
                ('meal_addition', models.ManyToManyField(blank=True, to='orders.Meal_Addition')),
                ('meal_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Meal_Type')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Size')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
