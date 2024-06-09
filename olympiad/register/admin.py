from django.contrib import admin
from register.models import *

@admin.register(Register)
class Register(admin.ModelAdmin):
    pass

@admin.register(Register_send)
class Register_send(admin.ModelAdmin):
    pass

@admin.register(Register_admin)
class Register_admin(admin.ModelAdmin):
    pass

@admin.register(Recommendation)
class Recommendation(admin.ModelAdmin):
    pass


