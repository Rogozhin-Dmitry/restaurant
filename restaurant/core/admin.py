from django.contrib import admin

from core.models import Category, Tag, Dish, Order, Table, OrderDish, Product, DishProduct


class CoreDishProductAdmin(admin.TabularInline):
    model = DishProduct
    extra = 0


@admin.register(Dish)
class CatalogItemAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "small_text",
        "category",
        "is_published",
        "coast"
    )
    list_editable = ("is_published",)
    filter_horizontal = (
        "tags",
    )
    inlines = [CoreDishProductAdmin]


@admin.register(Tag)
class CatalogTagAdmin(admin.ModelAdmin):
    list_display = ("name", "is_published")
    list_editable = ("is_published",)


@admin.register(Category)
class CatalogCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_published")
    list_editable = ("is_published",)


class OrderItemInline(admin.TabularInline):
    model = OrderDish
    extra = 0


@admin.register(Order)
class CookerOrderAdmin(admin.ModelAdmin):
    list_display = (
        "table",
        "is_done",
        "is_payed",
        "created_on",
    )
    list_editable = ("is_done", "is_payed",)
    inlines = [OrderItemInline]
    ordering = (
        "created_on",
    )


@admin.register(Table)
class CoreTableAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "is_private",
    )
    list_display_links = None
    list_editable = ("is_private", "name")


@admin.register(Product)
class CoreProductAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_display_links = None
    list_editable = ("name",)
