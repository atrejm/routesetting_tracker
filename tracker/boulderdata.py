import collections

def get_boulders_by_attr(boulders, attr, filter=False):
    # Get boulder data from DB and return it an a format that Chart.js understands
    num_boulders_by_attr = {}
    for boulder in boulders:
        attribute = getattr(boulder, attr)

        if attribute in num_boulders_by_attr:
            num_boulders_by_attr[attribute] += 1

            continue

        num_boulders_by_attr[attribute] = 1

    if(attr == "grade"):
        sorted_num_boulders_by_attr = sort_by_grade(num_boulders_by_attr)
    else:
        sorted_num_boulders_by_attr = num_boulders_by_attr

    labels = []
    values = []
    for key, value in sorted_num_boulders_by_attr.items():
        labels.append(key)
        values.append(value)

    return labels, values, sorted_num_boulders_by_attr

def sort_by_grade(boulders):
    for i in range(0, 12):
        if i not in boulders:
            boulders[i] = 0.1

    od = collections.OrderedDict(sorted(boulders.items()))
    return od