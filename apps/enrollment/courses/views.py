# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts               import render_to_response
from django.template                import RequestContext

from apps.enrollment.courses.models         import *
from apps.enrollment.records.models          import *

from apps.enrollment.courses.exceptions import NonCourseException
from apps.users.models import BaseUser

import logging
logger = logging.getLogger()

''' generates template data for filtering and list of courses '''
def prepare_courses_list_to_render(request):
    semesters = Semester.objects.filter(visible=True)
    courses = Course.visible.all()

    try:
        student = request.user.student
        records_history = student.get_records_history()
        student = True
    except Student.DoesNotExist:
        records_history = []
        student = False
    employee = BaseUser.is_employee(request.user)

    semester_courses = []
    for semester in semesters:
        semester_courses.append({
            'id': semester.pk,
            'name': semester.get_name(),
            'is_current': semester.is_current_semester(),
            'courses': courses.filter(semester__id__exact=semester.pk).
                order_by('name').values('id', 'name', 'type', 'slug')
        })
    for semester in semester_courses:
        for course in semester['courses']:
            course.update( { 'was_enrolled' : course['id'] in records_history } )

    render_data = {
        'is_student' : student,
        'is_employee' : employee,
        'semester_courses': semester_courses,
        'types_list' : Type.get_all_for_jsfilter(),
        'default_semester': Semester.get_default_semester()
    }
    return render_data


@login_required
def courses(request):
    return render_to_response('enrollment/courses/courses_list.html',
        prepare_courses_list_to_render(request), context_instance=RequestContext(request))

   
@login_required
def course(request, slug):
    try:
        course = Course.visible.get(slug=slug)
        records = Record.enrolled.filter(group__course=course)
        queues = Queue.queued.filter(group__course=course)
        groups = list(Group.objects.filter(course=course))
        try:
            student = request.user.student
            course.is_recording_open = course.is_recording_open_for_student(student)
            course.can_enroll_from = course.get_enrollment_opening_time(student)
            if course.can_enroll_from:
                course.can_enroll_interval = course.can_enroll_from - datetime.now()
            
            student_queues = queues.filter(student=student)
            student_queues_groups = map(lambda x: x.group, student_queues)
            student_groups = map(lambda x: x.group, records.filter(student=student))

            for g in groups:
                if g in student_queues_groups:
                    g.priority = student_queues.get(group=g).priority
                g.enrolled = records
                g.is_in_diff = [group.id for group in student_groups if group.type == g.type]
                if g in student_groups:
                    g.signed = True


            '''records = Record.objects.filter(student=student)    <--- prawdopodobnie niepotrzebne...
            if records:
                for record in records:
                    if ( record.group.course == course ):
                        if record.group.type == '2':
                            course.user_enrolled_to_exercise = True;
                            break;
                        elif record.group.type == '3':
                            course.user_enrolled_to_laboratory = True;
                            break;
                        elif record.group.type == '4':
                            course.user_enrolled_to_eaoratory = True;
                            break;
                        elif record.group.type == '5':
                            course.user_enrolled_to_exlaboratory = True;
                            break;
                        elif record.group.type == '6':
                            course.user_enrolled_to_seminar = True;
                            break;
                        elif record.group.type == '7':
                            course.user_enrolled_to_langoratory = True;
                            break;
                        elif record.group.type == '8':
                            course.user_enrolled_to_ssoratory = True;
                            break;
                        else:
                            break;'''
        except Student.DoesNotExist:
            student = None
            course.is_recording_open = False
            student_queues = None
            student_groups = None
            for g in groups:
                g.priority = None
                g.is_in_diff = False
                g.signed = False
            pass

        
        lectures = []
        exercises = []
        laboratories = []
        exercises_adv = []
        exer_labs = []
        seminar = []
        language = []
        sport = []
        repertory = []
        project = []


        for g in groups:
            g.enrolled = records.filter(group=g).count()
            g.queued = queues.filter(group=g).count()

            if (g.enrolled >= g.limit):
                g.is_full = True
            else:
                g.is_full = False

            if g.type == '1': #faster in good case, bad case - same
                lectures.append(g);
            elif g.type == '2':
                exercises.append(g);
            elif g.type == '3':
                laboratories.append(g);
            elif g.type == '4':
                exercises_adv.append(g);
            elif g.type == '5':
                exer_labs.append(g);
            elif g.type == '6':
                seminar.append(g);
            elif g.type == '7':
                language.append(g);
            elif g.type == '8':
                sport.append(g);
            elif g.type == '9':
                repertory.append(g);
            elif g.type == '10':
                project.append(g);
            else:
                break;

        '''lectures = groups.filter(type='1') #probably better, but you can't extend objects in QuerySet
        exercises = groups.filter(type='2')
        laboratories = groups.filter(type='3')
        exercises_adv = groups.filter(type='4')
        exer_labs = groups.filter(type='5')
        seminar = groups.filter(type='6')
        language = groups.filter(type='7')
        sport = groups.filter(type='8')

        lectures.name = "Wykłady"
        exercises.name = "Ćwiczenia"
        laboratories.name = "Pracownia"
        exercises_adv.name = "Ćwiczenia (poziom zaawansowany)"
        exer_labs.name = "Ćwiczenio-pracownie"
        seminar.name = "Seminarium"
        language.name = "Lektorat"
        sport.name = "Zajęcia"'''

        tutorials = [
            { 'name' : 'Wykłady', 'groups' : lectures, 'type' : 1},
            { 'name' : 'Repetytorium', 'groups' : repertory, 'type' : 9},
            { 'name' : 'Ćwiczenia', 'groups' : exercises, 'type' : 2},
            { 'name' : 'Pracownia', 'groups' : exercises_adv, 'type' : 4},
            { 'name' : 'Ćwiczenia (poziom zaaansowany)', 'groups' : laboratories, 'type' : 3},
            { 'name' : 'Ćwiczenio-pracownie', 'groups' : seminar, 'type' : 6},
            { 'name' : 'Seminarium', 'groups' : exer_labs, 'type' : 5},
            { 'name' : 'Lektorat', 'groups' : language, 'type' : 7},
            { 'name' : 'Zajęcia', 'groups' : sport, 'type' : 8},
            { 'name' : 'Project', 'groups' : project, 'type' : 10},
            ]
        

        data = prepare_courses_list_to_render(request)
        data.update({
            'course' : course,
            'tutorials' : tutorials,
        })

        return render_to_response( 'enrollment/courses/course.html', data, context_instance = RequestContext( request ) )

    except (Course.DoesNotExist, NonCourseException):
        logger.error('Function course(slug = %s) throws Course.DoesNotExist exception.' % unicode(slug) )
        request.user.message_set.create(message="Przedmiot nie istnieje.")
        return render_to_response('common/error.html', context_instance=RequestContext(request))