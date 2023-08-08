# Generated by Django 4.2.3 on 2023-08-01 19:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_genre_featured_book'),
    ]

    operations = [
        migrations.CreateModel(
            name='Borrow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_issue', models.DateTimeField(auto_now_add=True)),
                ('borrowed_status', models.CharField(choices=[('N', 'Not happened yet'), ('P', 'Pending'), ('C', 'Complete')], default='N', max_length=1)),
            ],
        ),
        migrations.AlterField(
            model_name='review',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='library.book'),
        ),
        migrations.AlterField(
            model_name='student',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='students/image'),
        ),
        migrations.DeleteModel(
            name='Borrower',
        ),
        migrations.AddField(
            model_name='borrow',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.student'),
        ),
    ]