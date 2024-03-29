# Generated by Django 5.0.2 on 2024-02-29 01:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("financebuddyweb", "0003_budget"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="FinancialGoal",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("target_amount", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "current_amount",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                ("completion_date", models.DateField(blank=True, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="financial_goals",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
