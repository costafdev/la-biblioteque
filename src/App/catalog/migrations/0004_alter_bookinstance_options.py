# Generated by Django 4.1.7 on 2023-03-10 13:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_bookinstance_borrower_alter_author_data_morte_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': (('can_mark_returned', 'Marquer comme retourné'),)},
        ),
    ]
