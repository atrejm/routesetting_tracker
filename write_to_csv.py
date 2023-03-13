import csv
from tracker.models import BoulderProblem, Routesetter



def write_boulders():
    boulderfile = open("boulders.csv", "w", newline="")

    boudlerwriter = csv.writer(boulderfile, delimiter=" ",quotechar="|",quoting=csv.QUOTE_MINIMAL)

    routesetters = Routesetter.objects.all()

    for routesetter in routesetters:
        print(routesetter.name)
        problems = routesetter.get_boulder_list()
        
        if problems:
            for problem in problems:
                print([routesetter.name, problem.color, problem.grade])
                boudlerwriter.writerow([routesetter.name, problem.color, problem.grade])
        else:
            print("NO BOULDERS IN LIST")


