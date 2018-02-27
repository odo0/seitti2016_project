from django.contrib import admin
from .forms import UserDataForm
from .models import *


class SignUpAdmin(admin.ModelAdmin):
    list_display = ["user", "name", "role"]
    form = UserDataForm
    # class Meta:
    #     model = SignUp


class GameAdmin(admin.ModelAdmin):
    list_display = ["name", "company", "url", "active", "price"]


admin.site.register(UserData, SignUpAdmin)
admin.site.register(Category)
admin.site.register(Company)
admin.site.register(OnlineGame, GameAdmin)
admin.site.register(UserGameOwnership)
admin.site.register(OnlineGameScore)
