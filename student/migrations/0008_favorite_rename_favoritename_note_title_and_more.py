# Generated by Django 4.2.16 on 2024-09-24 12:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0007_alter_student_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('F_id', models.IntegerField(auto_created=True, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('type', models.IntegerField(blank=True, null=True)),
                ('S_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student.student')),
                ('link', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student.favorite')),
            ],
        ),
        migrations.RenameField(
            model_name='note',
            old_name='favoritename',
            new_name='title',
        ),
        migrations.RemoveField(
            model_name='note',
            name='S_id',
        ),
        migrations.RemoveField(
            model_name='note',
            name='follow_num',
        ),
        migrations.RemoveField(
            model_name='note',
            name='like_num',
        ),
        migrations.RemoveField(
            model_name='note',
            name='type',
        ),
        migrations.AlterField(
            model_name='note',
            name='N_id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.DeleteModel(
            name='FavoriteISopen',
        ),
        migrations.AddField(
            model_name='note',
            name='F_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student.favorite'),
        ),
    ]
