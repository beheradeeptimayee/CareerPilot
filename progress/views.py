from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
# Create your views here.
from careers.models import Career
from roadmaps.models import LearningRoadmap,LearningModule,UserModuleProgress
from quizzes.models import QuizAttempt

@login_required
def progress_dashboard(request, career_slug):
    career = get_object_or_404(Career,slug=career_slug,is_active=True)
    roadmap = get_object_or_404(LearningRoadmap,user=request.user,career=career,status='ACTIVE')
    # Skill Progress
    roadmap_skills = roadmap.roadmap_skills.select_related('skill').all()
    total_skills = roadmap_skills.count()
    completed_skills = roadmap_skills.filter(status='COMPLETED').count()

    # Module Progress
    modules = LearningModule.objects.filter(
        roadmap_skill__roadmap=roadmap,
        is_active=True
    ).select_related(
        'roadmap_skill__skill'
    ).order_by(
        'roadmap_skill__order',
        'order'
    )

    total_modules = modules.count()

    completed_modules = UserModuleProgress.objects.filter(
        user=request.user,
        module__roadmap_skill__roadmap=roadmap,
        module__is_active=True,
        status='COMPLETED'
    ).count()

    # Continue Learning and Upcoming Modules
    next_module = None
    upcoming_modules = []

    for module in modules:
        module_progress, _ = UserModuleProgress.objects.get_or_create(
            user=request.user,
            module=module
        )
        if module_progress.status != 'COMPLETED':
            if next_module is None:
                next_module = module_progress

            if len(upcoming_modules) < 3:
                upcoming_modules.append(module_progress)

    # Recent Completed Modules
    recent_modules = UserModuleProgress.objects.filter(
        user=request.user,
        module__roadmap_skill__roadmap=roadmap,
        status='COMPLETED'
    ).select_related(
        'module',
        'module__roadmap_skill__skill'
    ).order_by('-completed_at')[:5]

    # Recent Quiz Attempts
    quiz_attempts = QuizAttempt.objects.filter(
        user=request.user,
        quiz__module__roadmap_skill__roadmap=roadmap,
        status='COMPLETED'
    ).select_related(
        'quiz',
        'quiz__module'
    ).order_by('-completed_at')

    quizzes_passed = sum(
        1
        for attempt in quiz_attempts
        if attempt.score >= attempt.quiz.passing_score
    )

    recent_quizzes = quiz_attempts[:5]

    # Dashboard Context
    context = {
        'career': career,
        'roadmap': roadmap,
        'roadmap_skills': roadmap_skills,
        'skill_progress': roadmap_skills,
        'total_skills': total_skills,
        'completed_skills': completed_skills,
        'total_modules': total_modules,
        'completed_modules': completed_modules,
        'next_module': next_module,
        'upcoming_modules': upcoming_modules,
        'recent_modules': recent_modules,
        'recent_quizzes': recent_quizzes,
        'quizzes_passed': quizzes_passed,
    }

    return render(request,'progress/progress_dashboard.html',context)