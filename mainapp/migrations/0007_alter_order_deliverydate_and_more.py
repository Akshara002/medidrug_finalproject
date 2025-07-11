# Generated by Django 5.1.7 on 2025-04-25 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainapp", "0006_alter_deliverydetail_deliverydate_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="deliverydate",
            field=models.CharField(
                blank=True, default="with in 24hour", max_length=100, null=True
            ),
        ),
        migrations.AlterField(
            model_name="prescription",
            name="deliverydate",
            field=models.CharField(
                blank=True, default="with in 24hours", max_length=100, null=True
            ),
        ),
        migrations.AlterField(
            model_name="prescriptiondeliverydetail",
            name="deliverydate",
            field=models.CharField(
                blank=True, default="with in 24hours", max_length=100, null=True
            ),
        ),
    ]
