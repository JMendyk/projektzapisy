# -*- coding: utf-8 -*-
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from apps.offer.desiderata.models import Desiderata, DesiderataOther
from apps.offer.desiderata.forms import DesiderataFormSet, DesiderataOtherForm
from apps.users.decorators import employee_required
from apps.enrollment.courses.models import Semester


@employee_required
def change_desiderata(request):
    """
    This view is to change desiderata for semester
    in which the desiderata is currently open.
    """
    user = request.user
    employee = user.employee
    semester = Semester.get_default_semester()

    desiderata = Desiderata.get_desiderata(employee, semester)
    other = DesiderataOther.get_desiderata_other(employee, semester)
    desiderata_formset_initial = Desiderata.get_desiderata_to_formset(desiderata)

    if request.method == 'POST':
        formset = DesiderataFormSet(request.POST)
        other_form = DesiderataOtherForm(request.POST, instance=other)
        if formset.is_valid():
            formset.save(desiderata, employee, semester)
            desiderata = Desiderata.get_desiderata(employee, semester)
            desiderata_formset_initial = Desiderata.get_desiderata_to_formset(desiderata)
        if other_form.is_valid():
            other_form.save()
            
    else:
        other_form = DesiderataOtherForm(instance=other)
    formset = DesiderataFormSet(initial=desiderata_formset_initial)
    data = {
        'formset': formset,
        'other_form': other_form,
        'semester': semester
    }
    return render_to_response('offer/desiderata/change_desiderata.html', data, context_instance=RequestContext(request))


    