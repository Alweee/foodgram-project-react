from django.contrib import admin

from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    RecipeIngredient,
    RecipeTag,
    ShoppingCart,
    Tag,
)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


class IngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through
    min_num = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientInline, ]

    list_display = ('id', 'name', 'author', 'is_favorite_count')
    list_filter = ('author', 'name', 'tags')

    @admin.display(description='is_favorite_count')
    def is_favorite_count(self, obj):
        return Favorite.objects.filter(recipe=obj).count()


class RecipeTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'tag')


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount')


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')


admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeTag, RecipeTagAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
