from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from studentorg.models import Organization, OrgMember, College, Student, Program
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from studentorg.forms import OrganizationForm, OrgMemberForm, CollegeForm, StudentForm, ProgramForm
from django.urls import reverse_lazy
from typing import Any
from django.db.models.query import QuerySet
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.

@method_decorator(login_required, name='dispatch')
class HomePageView(ListView):
    model = Organization
    context_object_name = 'home'
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        if user.is_authenticated:
            context['user_first_name'] = user.first_name
            context['user_last_name'] = user.last_name
            context['user_email'] = user.email
        else:
            context['user_first_name'] = ''
            context['user_last_name'] = ''
            context['user_email'] = ''

        return context

class OrganizationList(ListView):
    model = Organization
    context_object_name = 'organization'
    template_name = 'org_list.html'
    success_url = reverse_lazy('organization-list')
    paginate_by = 10

    def get_queryset(self, *args, **kwargs):
        qs = super(OrganizationList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") is not None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(name__icontains=query) | Q(description__icontains=query) | Q(college__college_name__icontains=query))
        return qs

class OrganizationCreateView(CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_add.html'  
    success_url = reverse_lazy('organization-add')

class OrganizationUpdateView(UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_edit.html'
    success_url = reverse_lazy('organization-list')

class OrganizationDeleteView(DeleteView):
    model = Organization
    template_name = 'org_del.html'
    success_url = reverse_lazy('organization-list')


class OrgMemberList(ListView):
    model = OrgMember
    template_name = 'org_mem_list.html'
    context_object_name = 'org_members'
    success_url = reverse_lazy('orgmember-list')

    def get_queryset(self, *args, **kwargs):
        qs = super(OrgMemberList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") is not None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(student__firstname__icontains=query) | Q(student__lastname__icontains=query) | Q(student__middlename__icontains=query) | Q(organization__name__icontains=query) | Q(student__program__prog_name__icontains=query))
        return qs
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        for member in queryset:
            try:
                member.program = Student.objects.get(id=member.student_id).program
            except Student.DoesNotExist:
                member.program = None

        return queryset
    
class OrgMemberCreateView(CreateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = 'org_mem_add.html'  
    success_url = reverse_lazy('orgmember-list')

class OrgMemberUpdateView(UpdateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = 'org_mem_edit.html'
    success_url = reverse_lazy('orgmember-list')

class OrgMemberDeleteView(DeleteView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = 'org_mem_delete.html'
    success_url = reverse_lazy('orgmember-list')


class CollegeList(ListView):
    model = College
    template_name = 'college_list.html'
    context_object_name = 'college'
    success_url = reverse_lazy('college-list')

    def get_queryset(self, *args, **kwargs):
        qs = super(CollegeList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") is not None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(college_name__icontains=query))
        return qs
    
class CollegeAddView(CreateView):
    model = College
    form_class = CollegeForm
    template_name = 'college_add.html'  
    success_url = reverse_lazy('college-list')

class CollegeUpdateView(UpdateView):
    model = College
    form_class = CollegeForm
    template_name = 'college_edit.html'
    success_url = reverse_lazy('college-list')

class CollegeDeleteView(DeleteView):
    model = College
    form_class = CollegeForm
    template_name = 'college_delete.html'
    success_url = reverse_lazy('college-list')


class StudentList(ListView):
    model = Student
    template_name = 'student_list.html'
    context_object_name = 'student'
    success_url = reverse_lazy('student-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['colleges'] = College.objects.all()
        return context
    
    def get_queryset(self, *args, **kwargs):
        qs = super(StudentList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") is not None:
            query = self.request.GET.get('q')
            print(query)
            qs = qs.filter(Q(student_id__icontains=query) | Q(firstname__icontains=query) | Q(lastname__icontains=query) | Q(middlename__icontains=query) | Q(program__college__college_name__icontains=query) | Q(program__prog_name__icontains=query))
        return qs
    
class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'student_add.html'  
    success_url = reverse_lazy('student-list')

class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'student_edit.html'
    success_url = reverse_lazy('student-list')

class StudentDeleteView(DeleteView):
    model = Student
    form_class = StudentForm
    template_name = 'student_delete.html'
    success_url = reverse_lazy('student-list')



class ProgramList(ListView):
    model = Program
    template_name = 'program_list.html'
    context_object_name = 'student'
    success_url = reverse_lazy('program-list')

    def get_queryset(self, *args, **kwargs):
        qs = super(ProgramList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get("q") is not None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(prog_name__icontains=query) | Q(college__college_name__icontains=query))
        return qs

class ProgramAddView(CreateView):
    model = Program
    form_class = ProgramForm
    template_name = 'program_add.html'
    success_url = reverse_lazy('program-list')
    
class ProgramUpdateView(UpdateView):
    model = Program
    form_class = ProgramForm
    template_name = 'program_edit.html'
    success_url = reverse_lazy('program-list')

class ProgramDeleteview(DeleteView):
    model = Program
    form_class = ProgramForm
    template_name = 'program_delete.html'
    success_url = reverse_lazy('program-list')



