from django.contrib import admin
from .models import Routesetter, BoulderProblem, ZoneModel

# Register your models here.
admin.site.register(Routesetter)
admin.site.register(BoulderProblem)
admin.site.register(ZoneModel)