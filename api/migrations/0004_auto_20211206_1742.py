# Generated by Django 2.2.16 on 2021-12-06 17:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_auto_20211205_1327"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="editingright",
            options={
                "ordering": ("editor",),
                "verbose_name": "Право на редактирование",
                "verbose_name_plural": "Права на редактирование",
            },
        ),
    ]