from django.contrib import admin
from .models import Offer


# Register your models here
@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'status')
    search_fields = ('title',)
    list_filter = ('status',)
    ordering = ('-id',)

