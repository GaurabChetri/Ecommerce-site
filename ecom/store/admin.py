from django.contrib import admin
from store.models import Customer,Category,Product,Order,Profile
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Profile)

#mix profile info and user info

class ProfielInLine(admin.StackedInline):
    model=Profile


#extend user model
class UserAdmin(admin.ModelAdmin):
    model = User
    field = ['username','first_name','last_name','email']
    inlines = [ProfielInLine]
    
#unregister the old way
admin.site.unregister(User)

#register the new way
admin.site.register(User,UserAdmin)