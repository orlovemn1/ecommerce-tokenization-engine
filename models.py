from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Categories(models.Model):
    title = models.CharField(max_length=255)


class Goods(models.Model):
    title = models.CharField(max_length=255)
    amount = models.IntegerField(default=0)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)


AREA_MAP = {
    "ЦАО": "A01",
    "САО": "A02",
    "СВАО": "A03",
    "ВАО": "A04",
    "ЮВАО": "A05",
    "ЮАО": "A06",
    "ЮЗАО": "A07",
    "ЗАО": "A08",
    "СЗАО": "A09",
    "ЗЕЛАО": "A10",
    "НАО": "A11",
    "ТАО": "A12",
}


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # U
    district_name = models.CharField(max_length=100, default="ЦАО")  # A
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)  # C
    is_express = models.BooleanField(default=False)  # S
    created_at = models.DateTimeField(auto_now_add=True)  # T

    # Метод для T
    def get_t_token(self):
        return f"T{self.created_at.hour:02d}"

    # Метод для S
    def get_s_token(self):
        return "S1" if self.is_express else "S0"

    # Метод для C
    def get_c_token(self):
        if self.total_cost < 1000:
            return "C1"
        elif self.total_cost < 3000:
            return "C2"
        elif self.total_cost < 6000:
            return "C3"
        elif self.total_cost < 10000:
            return "C4"
        else:
            return "C5"

    # Метод для A
    def get_a_token(self):
        name = str(self.district_name).strip().upper()
        return AREA_MAP.get(name, "A00")

    # Метод для U
    def get_u_token(self):
        total_spent = (
            Order.objects
            .filter(user=self.user)
            .aggregate(Sum("total_cost"))["total_cost__sum"] or 0
        )

        if total_spent < 2500:
            return "U1"
        elif total_spent < 10000:
            return "U2"
        elif total_spent < 25000:
            return "U3"
        elif total_spent < 60000:
            return "U4"
        else:
            return "U5"

    def get_full_token(self):
        tokens = [
            self.get_t_token(),
            self.get_a_token(),
            self.get_s_token(),
            self.get_c_token(),
            self.get_u_token(),
        ]
        return " ".join(tokens)

    def save_token_to_file(self):
        with open("orders_tokens.txt", "a", encoding="utf-8") as f:
            f.write(self.get_full_token() + "\n")