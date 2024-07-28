from django.contrib import admin
from .models import Rating, Medal, League, PersonalMedal
from result.models import *


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'points', 'league')
    search_fields = ('user__username', 'league')


@admin.register(Medal)
class MedalAdmin(admin.ModelAdmin):
    list_display = ('type', 'user', 'olympiad')
    search_fields = ('user__username', 'olympiad__name')


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('type', 'min_points', 'max_points')
    search_fields = ('type',)


@admin.register(PersonalMedal)
class PersonalMedalAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'date_awarded')
    search_fields = ('name', 'user__username')
