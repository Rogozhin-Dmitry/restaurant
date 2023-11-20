from django.db import models
from django.db.models import Prefetch
from django.utils import html
from sorl import thumbnail


class NameMixin(models.Model):
    name = models.CharField(
        verbose_name="Название", max_length=150, help_text="Макс 150 символов"
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name[:15]


class IsPublishedMixin(models.Model):
    is_published = models.BooleanField(
        verbose_name="В меню", default=True
    )

    class Meta:
        abstract = True


class DishManager(models.Manager):
    def get_sorry_dish(self):
        dish = self.unpublished_dishes_by_name('Комплимент от шеф повара')
        if not dish:
            dish = Dish()
            dish.name = 'Комплимент от шеф повара'
            dish.coast = 0
            dish.is_published = False
            category = Category.objects.published_category_by_name('Извинения')
            if not category:
                category = Category()
                category.name = "Извинения"
                category.is_published = False
                category.save()
            dish.category = category
            dish.save()
        return dish

    def published_dishes_by_id(self, dishes_id):
        return (
            self.get_queryset()
            .filter(is_published=True)
            .filter(pk=dishes_id)
            .first()
        )

    def unpublished_dishes_by_name(self, dishes_name):
        return (
            self.get_queryset()
            .filter(is_published=False)
            .filter(name=dishes_name)
            .first()
        )

    def published_dishes_by_ids(self, dishes_id):
        return (
            self.get_queryset()
            .filter(is_published=True)
            .filter(pk__in=dishes_id)
        )

    def published_dishes_name_by_ids(self, dishes_id):
        return (
            self.get_queryset()
            .filter(is_published=True)
            .filter(pk__in=dishes_id)
            .only("id", "name", "coast")
        )

    def published_dishes_ids(self):
        return (
            self.get_queryset()
            .filter(is_published=True)
            .select_related("category")
            .only(
                'category__is_published',
            )
            .filter(category__is_published=True)
            .prefetch_related(
                Prefetch(
                    "tags",
                    queryset=Tag.objects.filter(is_published=True).only('id'),
                )
            )
            .all()
            .values_list("id", flat=True)
        )

    def published_dishes_with_tags(self):
        dishes_id = list(self.published_dishes_ids())

        return (
            self.get_queryset()
            .filter(pk__in=dishes_id)
            .prefetch_related(
                Prefetch(
                    "tags",
                    queryset=Tag.objects.filter(is_published=True).only(
                        "name"
                    ),
                )
            )
            .only("id", "name", "text", "tags")
        )

    def published_dishes_with_category_name_and_tag_name(self):
        return (
            self.get_queryset()
            .filter(is_published=True)
            .select_related("category")
            .only(
                "id",
                "name",
                "text",
                "category__name",
                'category__is_published',
            )
            .filter(category__is_published=True)
            .prefetch_related(
                Prefetch(
                    "tags",
                    queryset=Tag.objects.filter(is_published=True).only(
                        "name"
                    ),
                )
            )
        )

    def published_dishes_with_category_name(self):
        return (
            self.get_queryset()
            .filter(is_published=True)
            .select_related("category")
            .only("name", "text", "category__name", "category__is_published")
            .filter(category__is_published=True)
            .prefetch_related(
                Prefetch(
                    "tags",
                    queryset=Tag.objects.filter(is_published=True).only(
                        "dish",
                        "quantity"
                    ),
                )
            )
        )


class Dish(IsPublishedMixin, NameMixin):
    text = models.TextField(
        verbose_name="Описание",
        help_text=(
            "Краткое описание для официанта",
        ),
    )
    category = models.ForeignKey(
        "Category",
        verbose_name="Категория",
        on_delete=models.CASCADE,
        related_name="dishes",
    )

    coast = models.IntegerField(
        verbose_name="Цена",
        default=1000
    )

    tags = models.ManyToManyField(
        "Tag",
        related_name="dishes",
        verbose_name="Теги",
    )

    main_image = thumbnail.ImageField(
        verbose_name="Основная картинка",
        help_text="Любая картинка, вам же на неё смотреть...",
        upload_to='uploads/',
        default='',
    )

    def get_image_1000x650(self):
        if self.main_image:
            return thumbnail.get_thumbnail(self.main_image, '1000x650', quality=51)
        return {"url": 'standard'}

    def get_image_300x255(self):
        if self.main_image:
            return thumbnail.get_thumbnail(self.main_image, '300x255', quality=51)
        return {"url": 'standard'}

    def small_text(self):
        if len(str(self.text)) > 101:
            return str(self.text)[:100]
        return str(self.text)

    def admin_image(self):
        if self.main_image:
            return html.format_html(
                f'<img src="{self.main_image.url}" '
                + 'style="width: 45px; height:45px;" />'
            )
        return 'Нет изображения'

    admin_image.allow_tags = True
    admin_image.short_description = 'Основная картинка'

    def __str__(self):
        return self.name

    small_text.short_description = 'Описание'

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"

    objects = DishManager()


class Tag(IsPublishedMixin, NameMixin):
    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"


class CategoryManager(models.Manager):
    def published_category_by_name(self, category_name):
        return (
            self.get_queryset()
            .filter(is_published=True)
            .filter(name=category_name)
            .first()
        )


class Category(IsPublishedMixin, NameMixin):
    objects = CategoryManager()

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class OrderManager(models.Manager):
    def actual_orders_this_dishes_done_nd_not_done(self) -> (list, list, list):
        orders = self.actual_orders_this_dishes()
        orders_payed = []
        orders_done = []
        orders_not_done = []
        for order in orders:
            if order.is_done:
                orders_payed.append(order)
            elif all(dish.is_done for dish in order.dishes.all()):
                orders_done.append(order)
            else:
                orders_not_done.append(order)
        return orders_not_done, orders_done, orders_payed

    def sum_to_pay_by_order_id(self, order_id):
        response = (
            self.get_queryset()
            .filter(is_payed=True, is_done=True)
            .filter(pk=order_id)
            .only("pk")
            .prefetch_related(
                Prefetch(
                    "dishes",
                    queryset=OrderDish.objects.only(
                        "quantity", "dish",
                    ).select_related("dish")
                    .only('dish__coast', )
                ),
            )
            .first()
        )
        print(response)
        if not response:
            return
        return sum(
            [dish.get_cost() for dish in response.dishes.all()]
        )

    def actual_order_by_id(self, order_id):
        return (
            self.get_queryset()
            .filter(is_payed=False)
            .filter(pk=order_id)
            .first()
        )

    def actual_orders_this_dishes(self):
        return (
            self.get_queryset()
            .filter(is_payed=False)
            .select_related("table")
            .only("pk", "created_on", "is_done", "table__name")
            .prefetch_related(
                Prefetch(
                    "dishes",
                    queryset=OrderDish.objects.only(
                        "quantity", "dish", "is_done"
                    ),
                )
            )
        )


class Order(models.Model):
    is_payed = models.BooleanField(
        verbose_name="Оплачен", default=False
    )

    is_done = models.BooleanField(
        verbose_name="Выполнен", default=False
    )

    table = models.ForeignKey(
        "Table",
        verbose_name="Столик",
        on_delete=models.CASCADE,
        related_name="orders",
    )

    created_on = models.DateTimeField(
        verbose_name="создан",
        help_text="Когда был создан",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    objects = OrderManager()


class TableManager(models.Manager):
    def un_private_table_by_id(self, table_id):
        return (
            self.get_queryset()
            .filter(is_private=False)
            .filter(pk=table_id)
            .first()
        )

    def un_private_tables(self):
        return (
            self.get_queryset()
            .filter(is_private=False)
            .order_by("name")
            .only("pk", "name")
            .all()
        )


class Table(NameMixin):
    is_private = models.BooleanField(
        verbose_name="Забронирован", default=False
    )

    class Meta:
        verbose_name = "Столик"
        verbose_name_plural = "Столики"

    objects = TableManager()


class OrderDish(models.Model):
    order = models.ForeignKey(Order, verbose_name="Заказ", related_name='dishes', on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, verbose_name="Блюдо", related_name='order_dishes', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="Количество", default=1)
    is_done = models.BooleanField(
        verbose_name="Готово", default=False
    )

    def get_cost(self):
        return self.dish.coast * self.quantity

    class Meta:
        verbose_name = "блюдо в заказ"
        verbose_name_plural = "Блюда в заказе"


class Product(NameMixin):
    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"


class DishProduct(models.Model):
    order = models.ForeignKey(Product, verbose_name="Продукт", related_name='dishes', on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, verbose_name="Блюдо", related_name='products', on_delete=models.CASCADE)
    weight = models.PositiveIntegerField(verbose_name="Масса в граммах", default=100)

    class Meta:
        verbose_name = "продукт в блюде"
        verbose_name_plural = "продукты в блюде"
