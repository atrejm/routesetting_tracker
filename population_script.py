import random
from collections import OrderedDict
from tracker.models import BoulderProblem, Routesetter, ZoneModel

COLOR_CHOICES = []
GRADE_CHOICES = []
ZONE_CHOICES = []

for choice in BoulderProblem.COLOR_CHOICES:
    COLOR_CHOICES.append(choice[0])

for choice in BoulderProblem.GRADE_CHOICES:
    GRADE_CHOICES.append(choice[0])

for choice in ZoneModel.ZONE_CHOICES:
    ZONE_CHOICES.append(choice[0])

def list_setters():
    for setter in Routesetter.objects.all():
        print(setter.name, setter.pk)

def add_random_boulders(number_of_boulders):
    
    setters = Routesetter.objects.all()
    zones = ZoneModel.objects.all()

    for i in range(number_of_boulders):
        weighted_grade_choice_index = get_weighted_gauss_guess()
        add_boulder(random.choice(setters).name, GRADE_CHOICES[weighted_grade_choice_index], random.choice(COLOR_CHOICES), random.choice(zones))
    

def add_setter(name):
    setter = Routesetter(name=name)
    setter.save()

def add_boulder(settername, grade, color, zone):

    if grade not in GRADE_CHOICES:
        print("Invalid Grade")
        return

    if color not in COLOR_CHOICES:
        print("Invalid Color")
        return
    
    if zone.zone_name not in ZONE_CHOICES:
        print("Invalid Zone")
        return

    for setter in Routesetter.objects.all():
        if setter.name == settername:
            
            print("Adding a {} {} to {}'s sheet in {}".format(color,grade,setter,zone.zone_name))
            boulder = BoulderProblem(id=None,setter=setter,grade=grade,color=color,zone_name=zone)
            boulder.save()
            
def create_zones():
    for zone_name in ZONE_CHOICES:
        zone_obj = ZoneModel(zone_name = zone_name)
        print("Created {} object.".format(zone_name))
        zone_obj.save()

def get_weighted_gauss_guess():
    #exclude any guess below 0 or above 11
    #5,2.5 hardcoded because its a reasonable distribution in this case

    guess = int(random.gauss(5, 2.5))
    guessValid = (guess >= 0) and (guess < 11)
    while not guessValid:
        guess = int(random.gauss(5, 3))
        guessValid = (guess >= 0) and (guess < 11)
    
    return guess
