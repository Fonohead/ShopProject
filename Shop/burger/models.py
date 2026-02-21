from datetime import datetime
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0.0)

director = 'DI'
admin = 'AD'
cook = 'CO'
cashier = 'CA'
cleaner = 'CL'

POSITIONS = [
    (director, 'Директор'),
    (admin, 'Администратор'),
    (cook, 'Повар'),
    (cashier, 'Кассир'),
    (cleaner, 'Уборщик')
]

class Staff(models.Model):
    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=2, choices=POSITIONS, default=cashier)
    labour_contract = models.IntegerField()


class Order(models.Model):
    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(null=True)
    cost = models.FloatField(default=0.0)
    take_away = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through="ProductsOrder")

    def finish_order(self):
        self.time_out = datetime.now()
        self.time_out = True
        self.save()

    def order_duration(self):
        if self.complete:
            return (self.time_in - self.time_out).total_seconds() // 60
        else:
            return (datetime.now() - self.time_in).total_seconds() // 60


class ProductsOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    _amount = models.IntegerField(default=1, db_column="amount")

    def product_sum(self):
        return self.product.price * self.amount

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = int(value) if value >= 0 else 0
        self.save()




