# Generated by Django 5.1.1 on 2024-10-02 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('description', models.TextField()),
                ('adoption_fee', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
