from django.shortcuts import render
from django.views.generic.list import ListView
from studentorg.models import Organization, OrgMember, College, Student
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from studentorg.forms import OrganizationForm, OrgMemberForm, CollegeForm
from django.urls import reverse_lazy


# Create your views here.

class HomePageView(ListView):
    model = Organization
    context_object_name = 'home'
    template_name = "home.html"

class OrganizationList(ListView):
    model = Organization
    context_object_name = 'organization'
    template_name = 'org_list.html'
    success_url = reverse_lazy('organization-list')
    paginate_by = 10


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['college'] = self.object
        return context



