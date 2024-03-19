# speeday_app/admin.py

from django.contrib import admin
from speeday_app.models import User, Task

admin.site.register(User)
admin.site.register(Task)
