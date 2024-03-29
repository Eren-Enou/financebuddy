# Generated by Django 5.0.2 on 2024-02-29 22:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("financebuddyweb", "0005_account_bill"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="account",
            name="interest_rate",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=4, null=True
            ),
        ),
        migrations.AddField(
            model_name="account",
            name="name",
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="account",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="accounts",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
