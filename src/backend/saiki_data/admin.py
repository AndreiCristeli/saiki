"""
backend/saiki_data/admin.py

...
"""

from django.contrib import admin
from .models import Algorithm


@admin.register(Algorithm)
class AlgorithmAdmin(admin.ModelAdmin):
    list_display = ("name",  "category", "year")
    search_fields = ("name", "category")
    list_filter = ("category", "year")


if __name__ == "__main__":
    ...
