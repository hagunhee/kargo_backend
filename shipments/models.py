from django.db import models


class Shipments(models.Model):
    company = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    discount_percentage = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    weight_100g = models.PositiveIntegerField(blank=True, null=True)
    weight_200g = models.PositiveIntegerField(blank=True, null=True)
    weight_300g = models.PositiveIntegerField(blank=True, null=True)
    weight_400g = models.PositiveIntegerField(blank=True, null=True)
    weight_500g = models.PositiveIntegerField(blank=True, null=True)
    weight_600g = models.PositiveIntegerField(blank=True, null=True)
    weight_700g = models.PositiveIntegerField(blank=True, null=True)
    weight_800g = models.PositiveIntegerField(blank=True, null=True)
    weight_900g = models.PositiveIntegerField(blank=True, null=True)
    weight_1000g = models.PositiveIntegerField(blank=True, null=True)
    weight_1100g = models.PositiveIntegerField(blank=True, null=True)
    weight_1200g = models.PositiveIntegerField(blank=True, null=True)
    weight_1300g = models.PositiveIntegerField(blank=True, null=True)
    weight_1400g = models.PositiveIntegerField(blank=True, null=True)
    weight_1500g = models.PositiveIntegerField(blank=True, null=True)
    weight_1600g = models.PositiveIntegerField(blank=True, null=True)
    weight_1700g = models.PositiveIntegerField(blank=True, null=True)
    weight_1800g = models.PositiveIntegerField(blank=True, null=True)
    weight_1900g = models.PositiveIntegerField(blank=True, null=True)
    weight_2000g = models.PositiveIntegerField(blank=True, null=True)
    weight_2100g = models.PositiveIntegerField(blank=True, null=True)
    weight_2200g = models.PositiveIntegerField(blank=True, null=True)
    weight_2300g = models.PositiveIntegerField(blank=True, null=True)
    weight_2400g = models.PositiveIntegerField(blank=True, null=True)
    weight_2500g = models.PositiveIntegerField(blank=True, null=True)
    weight_2600g = models.PositiveIntegerField(blank=True, null=True)
    weight_2700g = models.PositiveIntegerField(blank=True, null=True)
    weight_2800g = models.PositiveIntegerField(blank=True, null=True)
    weight_2900g = models.PositiveIntegerField(blank=True, null=True)
    weight_3000g = models.PositiveIntegerField(blank=True, null=True)
    weight_3100g = models.PositiveIntegerField(blank=True, null=True)
    weight_3200g = models.PositiveIntegerField(blank=True, null=True)
    weight_3300g = models.PositiveIntegerField(blank=True, null=True)
    weight_3400g = models.PositiveIntegerField(blank=True, null=True)
    weight_3500g = models.PositiveIntegerField(blank=True, null=True)
    weight_3600g = models.PositiveIntegerField(blank=True, null=True)
    weight_3700g = models.PositiveIntegerField(blank=True, null=True)
    weight_3800g = models.PositiveIntegerField(blank=True, null=True)
    weight_3900g = models.PositiveIntegerField(blank=True, null=True)
    weight_4000g = models.PositiveIntegerField(blank=True, null=True)

    def calculate_shipping_cost(self, product_weight):
        if product_weight < 450:
            added_weight = 150
        elif product_weight >= 450:
            added_weight = 250
        elif product_weight >= 900:
            added_weight = 350
        elif product_weight >= 1600:
            added_weight = 450
        elif product_weight >= 2600:
            added_weight = 550
            total_weight = product_weight + added_weight
            cost = self.get_shipping_cost(total_weight)
            discount_cost = cost * (1 - self.discount_percentage / 100)
            return cost

    def get_shipping_cost(self, weight):
        while weight <= 1000:
            # 해당 무게의 배송비 데이터가 존재하면 반환
            if getattr(self, f"weight_{weight}g") is not None:
                return getattr(self, f"weight_{weight}g")
            else:
                weight += 100
        raise ValueError("cannot find shipping cost")
