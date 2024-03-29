# Generated by Django 5.0.2 on 2024-02-22 00:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RestAPI', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='price',
            new_name='total',
        ),
        migrations.AlterUniqueTogether(
            name='cart',
            unique_together=set(),
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RestAPI.cart')),
                ('menu_item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='RestAPI.menuitem')),
            ],
            options={
                'unique_together': {('cart', 'menu_item')},
            },
        ),
        migrations.AddField(
            model_name='cart',
            name='menu_items',
            field=models.ManyToManyField(through='RestAPI.CartItem', to='RestAPI.menuitem'),
        ),
        migrations.RemoveField(
            model_name='cart',
            name='menu_item',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='unit_price',
        ),
    ]
