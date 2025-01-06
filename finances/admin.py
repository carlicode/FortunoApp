from django.contrib import admin
from .models import User, Category, Transaction, UserBalance  

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Transaction)
admin.site.register(UserBalance) 