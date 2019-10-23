from django.shortcuts import render
from django.db.models import Q
from profiles.models import ParentProfile

# Create your views here.
def search_parent(request):
    parents = ParentProfile.objects.filter(Q(first_name__icontains=request.GET.get('q', ''))|Q(last_name__icontains=request.GET.get('q', '')))
    return render(request, 'search-parents.html', {'parents': parents})