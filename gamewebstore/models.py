from django.db import models
from django.contrib.auth.models import User
import uuid


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    user = models.ManyToManyField(User, related_name='companies')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class OnlineGame(models.Model):
    name = models.CharField(max_length=255, unique=True)
    company = models.ForeignKey(Company, related_name='games')
    categories = models.ManyToManyField(Category, related_name='games')
    active = models.BooleanField()
    url = models.URLField()
    price = models.DecimalField(decimal_places=2, max_digits=5)
    description = models.TextField(default='')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return "{} ({}, {}, {:03.2f}€)".format(self.name, self.company, self.url, self.price)


class OnlineGameScore(models.Model):
    user = models.ForeignKey(User, related_name='scores')
    game = models.ForeignKey(OnlineGame, related_name='scores')
    score = models.FloatField(default=0.0)

    class Meta:
        unique_together = ('user', 'game')

    def __str__(self):
        return "{} - {} ({} points)".format(self.game, self.user, self.score)


class OnlineGameSaveState(models.Model):
    user = models.ForeignKey(User, related_name='saves')
    game = models.ForeignKey(OnlineGame, related_name='saves')

    # JSON blob
    data = models.BinaryField()

    class Meta:
        unique_together = ('user', 'game')

    def __str__(self):
        return "{} - {}".format(self.game, self.user)


class UserData(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    name = models.CharField(max_length=255)

    # expect to be either 'U' or 'D'
    # TODO: make this a real enum if we have time
    role = models.CharField(max_length=16)

    def __str__(self):
        return "{} user data ({})".format(self.user, self.role)


class UserGameOwnership(models.Model):
    user = models.ForeignKey(User, related_name='owned_games')
    game = models.ForeignKey(OnlineGame, related_name='owners')
    purchase_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'game')

    def __str__(self):
        return "{} - {}".format(self.game, self.user)


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name='transactions')
    game = models.ForeignKey(OnlineGame, related_name='transactions')
    pending = models.BooleanField(default=True)
    # The price can change between the user confirming and the control returning from the payment processor,
    # so it will be stored here instead of looking from the game entry itself
    amount = models.DecimalField(decimal_places=2, max_digits=5)
    expires = models.DateTimeField(null=True)

    class Meta:
        unique_together = ('user', 'game')

    def __str__(self):
        return "{} - {} ({:03.2f}€{})".format(self.game, self.user, self.amount,
                                              (", expires " + str(self.expires) if self.pending else ""))
