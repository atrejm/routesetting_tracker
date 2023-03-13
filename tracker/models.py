from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
# Create your models here.
class Routesetter(models.Model):
    name = models.CharField(max_length=50)

    def get_boulder_list(self):
        boulders = []
        for boulder in self.problems.all(): #<---- related name = "problems" in BoulderProblem Model
            if boulder:
                boulders.append(boulder)
            else:
                print("no boulder for setter")
        
        return boulders

    def __str__(self):
        return self.name

class BoulderProblem(models.Model):
    
    class Meta:
        # simplest way to get formset to display boulders in order of grade
        ordering = ("grade",)

    COLOR_CHOICES = [
        ('Black','Black'),
        ('Blue','Blue'),
        ('Orange','Orange'),
        ('Pink','Pink'),
        ('Green','Green'),
        ('Yellow','Yellow'),
    ]

    GRADE_CHOICES = [
        (0,'V0'),
        (1,'V1'),
        (2,'V2'),
        (3,'V3'),
        (4,'V4'),
        (5,'V5'),
        (6,'V6'),
        (7,'V7'),
        (8,'V8'),
        (9,'V9'),
        (10,'V10'),
        (11,'V11'),
    ]

    color = models.CharField(max_length=20,choices=COLOR_CHOICES)
    setter = models.ForeignKey('tracker.Routesetter', related_name="problems",on_delete=models.CASCADE)
    zone_name = models.ForeignKey('tracker.ZoneModel',related_name="zone",on_delete=models.CASCADE)
    grade = models.IntegerField(choices=GRADE_CHOICES)
    created_date = models.DateTimeField(default=timezone.now)
    archived = models.BooleanField(default=False)

class ZoneModel(models.Model):
    ZONE_CHOICES = [
    ('Zone 1','Zone 1'),
    ('Zone 2',	'Zone 2'),
    ('Zone 3',	'Zone 3'),
    ('Zone 4',	'Zone 4'),
    ('Zone 5',	'Zone 5'),
    ('Zone 6',	'Zone 6'),
    ('Zone 7',	'Zone 7'),
    ('Zone 8',	'Zone 8'),
    ('Zone 9',	'Zone 9'),
    ('Zone 10',	'Zone 10'),
    ('Zone 11',	'Zone 11'),
    ('Zone 12',	'Zone 12'),
    ('Zone 13',	'Zone 13'),
    ('Zone 14',	'Zone 14'),
    ('Zone 15',	'Zone 15'),
    ('Zone 16',	'Zone 16'),
    ]
        
    zone_name = models.CharField(max_length=20,choices=ZONE_CHOICES)

    def __str__(self):
        return self.zone_name