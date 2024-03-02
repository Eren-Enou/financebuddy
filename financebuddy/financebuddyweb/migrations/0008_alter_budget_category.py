# Generated by Django 5.0.2 on 2024-03-02 03:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("financebuddyweb", "0007_reminder"),
    ]

    operations = [
        migrations.AlterField(
            model_name="budget",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="financebuddyweb.category",
            ),
        ),
    ]