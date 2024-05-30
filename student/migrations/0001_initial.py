# Generated by Django 5.0.5 on 2024-05-18 10:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Std_Id', models.CharField(default=0, max_length=10, unique=True)),
                ('Roll_No', models.IntegerField(null=True)),
                ('Full_Name', models.CharField(max_length=75)),
                ('Nationality', models.CharField(max_length=25)),
                ('Std', models.IntegerField(null=True)),
                ('Div', models.CharField(max_length=3)),
                ('Email', models.EmailField(max_length=254)),
                ('Category', models.CharField(max_length=25)),
                ('Father', models.CharField(max_length=50)),
                ('Mother', models.CharField(max_length=50)),
                ('Father_No', models.IntegerField(null=True)),
                ('Mother_No', models.IntegerField(null=True)),
                ('Father_Job', models.CharField(max_length=50)),
                ('Mother_Job', models.CharField(max_length=50)),
                ('Board_Code', models.CharField(max_length=25)),
                ('Residental_Add', models.TextField(null=True)),
                ('Parmanenet_Add', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Marks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('English', models.IntegerField()),
                ('Hindi', models.IntegerField()),
                ('Marathi', models.IntegerField()),
                ('Science', models.IntegerField()),
                ('Mathematics', models.IntegerField()),
                ('SocialScience', models.IntegerField()),
                ('target', models.IntegerField(default=100)),
                ('score', models.IntegerField()),
                ('Sid', models.ForeignKey(db_column='Sid', on_delete=django.db.models.deletion.CASCADE, to='student.student')),
            ],
        ),
    ]
