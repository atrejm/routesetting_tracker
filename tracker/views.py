from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView, DetailView
from .models import Routesetter, BoulderProblem, ZoneModel
from .forms import (RoutesetterForm, BoulderProblemForm, 
                    AddBoulderForm, AddBoulderFormSetHelper, 
                    ManageBoulderFormSetHelper, EditZoneFormSetHelper,
                    DateInputForm, ZoneChoiceForm, ArchiveZoneForm)
from django.forms import formset_factory, modelformset_factory, inlineformset_factory
from .boulderdata import get_boulders_by_attr
import datetime

# Create your views here.
class Index(TemplateView):
    template_name = "tracker/index.html"

class RoutesetterListView(ListView):
    model = Routesetter
    template_name="tracker/setter_list.html"

# class RoutesetterDetailView(DetailView):
#     model = Routesetter
#     template_name="tracker/setter_detail.html"

def routesetter_detail_view(request, pk):
    setter = get_object_or_404(Routesetter, pk=pk)
    all_setters = Routesetter.objects.all()
    boulders = setter.get_boulder_list()

    color_labels, color_values, num_boulders_by_color = get_boulders_by_attr(boulders, "color")
    grade_labels, grade_values, num_boulders_by_grade = get_boulders_by_attr(boulders, "grade")
    
    contextDict = {
        'all_setters':all_setters,
        'setter':setter,
        'boulders_by_color':num_boulders_by_color,
        'color_labels':color_labels,
        'color_values':color_values,
        'grade_labels':grade_labels, 
        'grade_values':grade_values, 
        'num_boulders_by_grade':num_boulders_by_grade,
    }

    return render(request, "tracker/setter_detail.html",context=contextDict)

def chart_boulders_view(request):
    # Check if user submitted a date range to filter boulders
    if request.method == "POST":
        form = DateInputForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            dateFilter = True
            startDate = form.cleaned_data['start_date']
            endDate = form.cleaned_data['end_date']
    else:
        dateFilter = False
        form = DateInputForm()

    if dateFilter:
        boulders = BoulderProblem.objects.filter(created_date__gte=startDate, 
                                                 created_date__lte=endDate)
    else:
        boulders = BoulderProblem.objects.all()

    

    color_labels, color_values, num_boulders_by_color = get_boulders_by_attr(boulders, "color")
    grade_labels, grade_values, num_boulders_by_grade = get_boulders_by_attr(boulders, "grade")
    contextDict = {
        'boulders_by_color':num_boulders_by_color,
        'color_labels':color_labels,
        'color_values':color_values,
        'grade_labels':grade_labels, 
        'grade_values':grade_values, 
        'num_boulders_by_grade':num_boulders_by_grade,
        'form':form,
    }

    return render(request, "tracker/boulder_chart.html",context=contextDict)

@login_required
def add_boulder_view(request, zone_name="Z1"):

    zone_obj=ZoneModel.objects.get(zone_name__iexact=zone_name)
    all_zones=ZoneModel.objects.all()

    BoulderFormSet = formset_factory(AddBoulderForm, extra=5)
    form_set = BoulderFormSet(request.POST or None)
    zone_form = ZoneChoiceForm(request.POST or None)
    helper = AddBoulderFormSetHelper()

    if request.method == "POST":
        form_set = BoulderFormSet(request.POST, request.FILES)
        print("Formset Valid?", form_set.is_valid())
        if form_set.is_valid():
            for form in form_set:
                if form.is_valid():
                    if form.cleaned_data != {}:
                        boulder = form.save(commit=False)
                        boulder.zone_name = zone_obj
                        boulder.save()
            return redirect('boulderchart')
    else:
        form_set = BoulderFormSet()

    return render(request, "tracker/add_boulder.html", {'form_set':form_set,
                                                        'helper':helper,
                                                        'zone_form':zone_form,
                                                        'zone_obj':zone_obj,
                                                        'all_zones':all_zones})

@login_required
def manage_boulders(request, pk):
    setter = Routesetter.objects.get(pk=pk)


    BoulderInlineFormSet = inlineformset_factory(Routesetter, BoulderProblem, fields=('zone_name','grade','color'), can_delete=True)
    helper = ManageBoulderFormSetHelper()

    if request.method == "POST":
        formset = BoulderInlineFormSet(request.POST, request.FILES, instance=setter)
        if formset.is_valid():
            formset.save()
            # Do something. Should generally end with a redirect. For example:
            return redirect("routesetter_detail", pk=setter.pk)
    else:
        formset = BoulderInlineFormSet(instance=setter)
    return render(request, 'tracker/manage_boulders.html', {'formset': formset,
                                                            'setter': setter,
                                                            'helper':helper})

@login_required
def edit_zone_view(request, zone):
    zone_obj=ZoneModel.objects.get(zone_name__iexact=zone)
    all_zones=ZoneModel.objects.all()
    boulders = BoulderProblem.objects.filter(zone_name__exact=zone_obj.id)
    grade_labels, grade_values, num_boulders_by_grade = get_boulders_by_attr(boulders, "grade")

    BoulderInlineFormSet = inlineformset_factory(ZoneModel, BoulderProblem, fields=('setter','grade','color'), can_delete=True)
    helper = EditZoneFormSetHelper()

    if request.method == "POST":
        form = ArchiveZoneForm(request.POST)
        if form.is_valid():
            return redirect("archive_confirmation", zone=zone_obj.zone_name) 
        
        formset = BoulderInlineFormSet(request.POST, request.FILES, instance=zone_obj)
        if formset.is_valid():
            formset.save()
            # Do something. Should generally end with a redirect. For example:
            return redirect("edit_zone", zone=zone_obj.zone_name)
    else:
        formset = BoulderInlineFormSet(instance=zone_obj)
        form = ArchiveZoneForm()
    return render(request, 'tracker/edit_zone.html', {'formset': formset,
                                                      'form':form,
                                                        'zone_obj': zone_obj,
                                                        'all_zones':all_zones,
                                                        'helper':helper,
                                                        'grade_labels':grade_labels,
                                                        'grade_values':grade_values,
                                                        'num_boulders_by_grade':num_boulders_by_grade})

@login_required
def add_routesetter(request):
    
    if request.method == "POST":
        form = RoutesetterForm(request.POST)
        if form.is_valid():
            setter = form.save()
            # Do something. Should generally end with a redirect. For example:
            return redirect("routesetter_detail", pk=setter.pk)
    else:
        form = RoutesetterForm()
    return render(request, 'tracker/add_setter.html', {'form': form })

@login_required
def archive_confirmation(request, zone):
    return render(request, 'tracker/archive_confirmation.html', {'zone':zone})