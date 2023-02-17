from django.contrib import admin

from borrowing.models import Borrowing


@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    readonly_fields = ("borrow_date",)
