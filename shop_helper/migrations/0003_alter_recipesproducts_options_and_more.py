# Generated by Django 4.1.4 on 2022-12-09 11:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop_helper', '0002_alter_product_category_alter_recipesproducts_product_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipesproducts',
            options={'verbose_name': 'Продукт в рецепте', 'verbose_name_plural': 'Продукты в рецептах'},
        ),
        migrations.AlterField(
            model_name='recipesproducts',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products_recipes', to='shop_helper.product', verbose_name='Продукт'),
        ),
        migrations.AlterField(
            model_name='recipesproducts',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='recipes_products', to='shop_helper.recipe', verbose_name='Рецепт'),
        ),
    ]