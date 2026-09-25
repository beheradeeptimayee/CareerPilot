from django.shortcuts import render,get_object_or_404

# Create your views here.
from careers.models import Career


def career_list(request):

    careers = Career.objects.filter(is_active=True).select_related('category')
    return render(request,'careers/career_list.html',{  'careers': careers})


def career_detail(request, slug):

    career = get_object_or_404(Career.objects.select_related('category').prefetch_related('skills'),
        slug=slug,
        is_active=True
    )

    return render(
        request,
        'careers/career_detail.html',
        {
            'career': career
        }
    )