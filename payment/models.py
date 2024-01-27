# payment/models.py
from django.db import models
from django.contrib.auth.models import User

class USDT_TRC20(models.Model):
    coin_name = models.CharField(max_length=255)
    qr_code = models.ImageField(upload_to='usdt_trc20_qrcodes/')
    wallet_address = models.CharField(max_length=255)
    network = models.CharField(max_length=50)

    def __str__(self):
        return self.coin_name

    class Meta:
        verbose_name = "USDT TRC20"
        verbose_name_plural = "USDT TRC20"

class USDT_ERC20(models.Model):
    coin_name = models.CharField(max_length=255)
    qr_code = models.ImageField(upload_to='usdt_erc20_qrcodes/')
    wallet_address = models.CharField(max_length=255)
    network = models.CharField(max_length=50)

    def __str__(self):
        return self.coin_name

    class Meta:
        verbose_name = "USDT ERC20"
        verbose_name_plural = "USDT ERC20"

class BTC(models.Model):
    coin_name = models.CharField(max_length=255)
    qr_code = models.ImageField(upload_to='btc_qrcodes/')
    wallet_address = models.CharField(max_length=255)
    network = models.CharField(max_length=50)

    def __str__(self):
        return self.coin_name

    class Meta:
        verbose_name = "BTC"
        verbose_name_plural = "BTC"

class Funds(models.Model):
    ACCOUNT_TYPES = [
        ('USDT_TRC20', 'USDT TRC20'),
        ('USDT_ERC20', 'USDT ERC20'),
        ('BTC', 'BTC'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    confirmed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Override save method to update AccountSummary when funding is approved
        super().save(*args, **kwargs)
        if self.confirmed:
            AccountSummary.update_summary(self.user, self.account_type)

    def __str__(self):
        return f"{self.user.username} - {self.account_type} - {self.amount}"

    class Meta:
        verbose_name = "Funds"
        verbose_name_plural = "Funds"


class AccountSummary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=20, choices=Funds.ACCOUNT_TYPES, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.username} - {self.account_type} - {self.total_amount}"

    @classmethod
    def update_summary(cls, user, account_type):
        # Update or create an AccountSummary entry based on approved funds
        funds_total = Funds.objects.filter(user=user, account_type=account_type, confirmed=True).aggregate(sum_amount=models.Sum('amount'))['sum_amount'] or 0
        summary, created = cls.objects.get_or_create(user=user, account_type=account_type)
        summary.total_amount = funds_total
        summary.save()
