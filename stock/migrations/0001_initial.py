# Generated by Django 3.2.8 on 2021-11-07 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BalanceSheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stockName', models.CharField(max_length=50)),
                ('product_year', models.CharField(default='', max_length=50)),
                ('shareCapital', models.IntegerField(default=0)),
                ('Reserves', models.IntegerField(default=0)),
                ('Borrowings', models.IntegerField(default=0)),
                ('OtherLiabilities', models.IntegerField(default=0)),
                ('totalLiabilities', models.IntegerField(default=0)),
                ('fixedAssets', models.IntegerField(default=0)),
                ('cwip', models.IntegerField(default=0)),
                ('investments', models.IntegerField(default=0)),
                ('otherAssets', models.IntegerField(default=0)),
                ('totalAssets', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ProfitAndLoss',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('year', models.IntegerField(default=0)),
                ('sales', models.IntegerField(default=0)),
                ('expenses', models.IntegerField(default=0)),
                ('operatingProfit', models.IntegerField(default=0)),
                ('opm', models.IntegerField(default=0)),
                ('otherIncome', models.IntegerField(default=0)),
                ('interest', models.IntegerField(default=0)),
                ('depreciation', models.IntegerField(default=0)),
                ('pbt', models.IntegerField(default=0)),
                ('tax', models.IntegerField(default=0)),
                ('netProfit', models.IntegerField(default=0)),
                ('eps', models.IntegerField(default=0)),
                ('dividend', models.IntegerField(default=0)),
            ],
        ),
    ]
