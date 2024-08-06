from django.db import models


class CompanyInfoModel(models.Model):
    proposal_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    profile = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    rating = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class WasteInfoModel(models.Model):
    proposal_id = models.ForeignKey(CompanyInfoModel, related_name="waste_infos", on_delete=models.CASCADE,
                                    to_field="proposal_id")
    image = models.ImageField(upload_to='image/', blank=True, null=True)
    type = models.CharField(max_length=255)
    amount = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=3)

    def __str__(self):
        return f'{self.type}-{self.amount}'
