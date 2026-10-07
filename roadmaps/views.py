from django.shortcuts import render,get_object_or_404, redirect
from django.utils import timezone
# Create your views here.
from django.contrib.auth.decorators import login_required
from assessments.models import AssessmentAttempt, SkillResult
from careers.models import Career, CareerSkill
from roadmaps.models import LearningRoadmap,LearningModule,RoadmapSkill,UserModuleProgress
from decimal import Decimal

def calculate_priority(gap):
    if gap >= Decimal('40'):
        return 'HIGH'
    elif gap >= Decimal('20'):
        return 'MEDIUM'
    else:
        return 'LOW'

MODULE_TEMPLATES = {
    'Python': [
        ('Python Fundamentals', 'Introduction to Python, syntax, variables, and basic programming concepts.', 30, 'BEGINNER'),
        ('Variables and Data Types', 'Learn Python variables, numbers, strings, lists, tuples, sets, and dictionaries.', 30, 'BEGINNER'),
        ('Control Flow', 'Learn conditions, loops, break, continue, and pass statements.', 35, 'BEGINNER'),
        ('Functions', 'Learn how to create functions, use parameters, return values, and understand scope.', 40, 'BEGINNER'),
        ('Object-Oriented Programming', 'Learn classes, objects, inheritance, encapsulation, and polymorphism.', 50, 'INTERMEDIATE'),
        ('Exception Handling', 'Learn try, except, else, finally, and custom exceptions.', 35, 'INTERMEDIATE'),
    ],

    'Django': [
        ('Django Fundamentals', 'Understand Django architecture, projects, applications, and the MVT pattern.', 35, 'BEGINNER'),
        ('Django Project Structure', 'Learn Django settings, URLs, apps, templates, and static files.', 35, 'BEGINNER'),
        ('Models and ORM', 'Learn Django models, relationships, migrations, and ORM queries.', 50, 'INTERMEDIATE'),
        ('Views and URLs', 'Learn function-based views, URL routing, request handling, and responses.', 40, 'INTERMEDIATE'),
        ('Templates and Forms', 'Learn Django templates, template inheritance, forms, and validation.', 45, 'INTERMEDIATE'),
        ('Django REST Framework', 'Learn serializers, API views, authentication, and REST API development.', 60, 'ADVANCED'),
    ],

    'REST APIs': [
        ('REST API Fundamentals', 'Understand REST architecture, resources, endpoints, and HTTP methods.', 30, 'BEGINNER'),
        ('HTTP Methods and Status Codes', 'Learn GET, POST, PUT, PATCH, DELETE and common HTTP status codes.', 30, 'BEGINNER'),
        ('API Requests and Responses', 'Understand request data, response formats, headers, and JSON.', 35, 'INTERMEDIATE'),
        ('Authentication and Authorization', 'Learn authentication concepts and securing API endpoints.', 45, 'INTERMEDIATE'),
        ('API Validation and Error Handling', 'Learn input validation and consistent API error responses.', 40, 'INTERMEDIATE'),
    ],

    'SQL': [
        ('SQL Fundamentals', 'Learn databases, tables, records, and basic SQL syntax.', 30, 'BEGINNER'),
        ('SELECT and Filtering', 'Learn SELECT, WHERE, ORDER BY, DISTINCT, LIKE, and filtering.', 35, 'BEGINNER'),
        ('Joins', 'Learn INNER JOIN, LEFT JOIN, RIGHT JOIN, and SELF JOIN.', 45, 'INTERMEDIATE'),
        ('Aggregate Functions', 'Learn COUNT, SUM, AVG, MIN, MAX, GROUP BY, and HAVING.', 40, 'INTERMEDIATE'),
        ('Subqueries', 'Learn nested queries, correlated subqueries, and practical use cases.', 45, 'INTERMEDIATE'),
        ('Indexes and Query Optimization', 'Understand indexes and techniques for improving query performance.', 45, 'ADVANCED'),
    ],

    'PostgreSQL': [
        ('PostgreSQL Fundamentals', 'Understand PostgreSQL architecture, databases, schemas, and basic commands.', 30, 'BEGINNER'),
        ('PostgreSQL Data Types', 'Learn PostgreSQL-specific and commonly used data types.', 30, 'BEGINNER'),
        ('Constraints and Relationships', 'Learn primary keys, foreign keys, unique, check, and not-null constraints.', 40, 'INTERMEDIATE'),
        ('Sequences and Identity Columns', 'Understand sequences and identity columns for generated values.', 30, 'INTERMEDIATE'),
        ('Indexes and Views', 'Learn PostgreSQL indexes and database views.', 40, 'INTERMEDIATE'),
        ('Useful PostgreSQL Commands', 'Learn practical psql commands and database management operations.', 30, 'INTERMEDIATE'),
    ],

    'Git': [
        ('Git Fundamentals', 'Understand repositories, commits, branches, and Git workflow.', 30, 'BEGINNER'),
        ('Working with Commits', 'Learn add, commit, status, log, and viewing changes.', 30, 'BEGINNER'),
        ('Branches and Merging', 'Learn branch creation, switching, merging, and resolving conflicts.', 40, 'INTERMEDIATE'),
        ('Remote Repositories', 'Learn push, pull, fetch, and working with remote repositories.', 35, 'INTERMEDIATE'),
        ('Git Workflow', 'Learn practical Git workflows for software development projects.', 40, 'INTERMEDIATE'),
    ],

    'GitHub': [
        ('GitHub Fundamentals', 'Understand repositories, README files, issues, and project structure.', 30, 'BEGINNER'),
        ('Push Projects to GitHub', 'Learn how to connect local projects and push code to GitHub.', 30, 'BEGINNER'),
        ('Branches and Pull Requests', 'Learn GitHub branches, pull requests, and collaboration workflows.', 40, 'INTERMEDIATE'),
        ('GitHub Project Management', 'Learn issues, project organization, and repository management.', 35, 'INTERMEDIATE'),
        ('Professional GitHub Profile', 'Learn how to organize repositories and present projects professionally.', 30, 'INTERMEDIATE'),
    ],
}

@login_required
def build_roadmap(request, career_slug):

    career = get_object_or_404(Career,slug=career_slug,is_active=True)

    latest_attempt = (
        AssessmentAttempt.objects
        .filter(
            user=request.user,
            assessment__career=career,
            status='COMPLETED'
        )
        .order_by('-completed_at')
        .first()
    )

    # If the user has not completed an assessment,
    # send them back to the assessment page.
    if not latest_attempt:
        return redirect('assessment_intro',career_slug=career.slug)

    # Get the latest skill results.
    skill_results = {
        result.skill_id: result
        for result in SkillResult.objects.filter(
            attempt=latest_attempt
        ).select_related('skill')
    }

    # Get or create the user's roadmap.
    roadmap, created = LearningRoadmap.objects.get_or_create(
        user=request.user,
        career=career,
        defaults={
            'title': f'{career.name} Learning Roadmap',
            'status': 'ACTIVE',
            'overall_progress': Decimal('0'),
            'estimated_duration_weeks': 8,
        }
    )

    # Rebuild roadmap skills when generating a new roadmap.
    roadmap.roadmap_skills.all().delete()

    career_skills = (
        CareerSkill.objects
        .filter(career=career)
        .select_related('skill')
    )
    roadmap_skill_data = []

    for career_skill in career_skills:

        result = skill_results.get(career_skill.skill_id)

        if result:
            current_score = result.score
        else:
            current_score = Decimal('0')

        target_score = career_skill.target_proficiency

        gap_score = max(
            target_score - current_score,
            Decimal('0')
        )

        if current_score >= target_score:
            priority = 'LOW'
        else:
            priority = calculate_priority(gap_score)

        roadmap_skill_data.append({
            'skill': career_skill.skill,
            'priority': priority,
            'current_score': current_score,
            'target_score': target_score,
            'gap_score': gap_score,
        })


    # HIGH → MEDIUM → LOW
    priority_order = {
        'HIGH': 1,
        'MEDIUM': 2,
        'LOW': 3,
    }

    roadmap_skill_data.sort(
        key=lambda item: priority_order[item['priority']]
    )


    for order, data in enumerate(roadmap_skill_data, start=1):

        roadmap_skill = roadmap.roadmap_skills.create(
            skill=data['skill'],
            priority=data['priority'],
            current_score=data['current_score'],
            target_score=data['target_score'],
            gap_score=data['gap_score'],
            status='NOT_STARTED',
            progress=Decimal('0'),
            order=order,
        )


        # Create learning modules for this skill.
        module_templates = MODULE_TEMPLATES.get(
            data['skill'].name,
            []
        )

        for module_order, module_data in enumerate(module_templates,start=1):
            title, description, minutes, difficulty = module_data
            LearningModule.objects.create(
                roadmap_skill=roadmap_skill,
                title=title,
                description=description,
                order=module_order,
                estimated_minutes=minutes,
                difficulty=difficulty,
                is_active=True,
            )
    return redirect('roadmap_dashboard',career_slug=career.slug)


@login_required
def roadmap_dashboard(request, career_slug):

    career = get_object_or_404(Career,slug=career_slug,is_active=True)

    roadmap = get_object_or_404(LearningRoadmap,user=request.user,career=career,status='ACTIVE')

    roadmap_skills = roadmap.roadmap_skills.select_related('skill').prefetch_related('learning_modules')

    return render(
        request,
        'roadmaps/roadmap_dashboard.html',
        {
            'career': career,
            'roadmap': roadmap,
            'roadmap_skills': roadmap_skills,
        }
    )

@login_required
def skill_learning(request, career_slug, skill_id):
    career = get_object_or_404(Career,slug=career_slug,is_active=True)
    roadmap = get_object_or_404(LearningRoadmap,user=request.user,career=career,status='ACTIVE')
    roadmap_skill = get_object_or_404(roadmap.roadmap_skills.select_related('skill'),skill_id=skill_id)
    modules = (roadmap_skill.learning_modules.filter(is_active=True).order_by('order'))

    return render(
        request,
        'roadmaps/skill_learning.html',
        {
            'career': career,
            'roadmap': roadmap,
            'roadmap_skill': roadmap_skill,
            'modules': modules,
        }
    )

@login_required
def module_learning(request, career_slug, skill_id, module_id):

    career = get_object_or_404(Career,slug=career_slug,is_active=True)
    roadmap = get_object_or_404(LearningRoadmap,user=request.user,career=career,status='ACTIVE')
    roadmap_skill = get_object_or_404(RoadmapSkill.objects.select_related('skill'),roadmap=roadmap,skill_id=skill_id)
    module = get_object_or_404(
        LearningModule,
        id=module_id,
        roadmap_skill=roadmap_skill,
        is_active=True
    )

    progress, created = UserModuleProgress.objects.get_or_create(user=request.user,module=module)

    if request.method == 'POST':

        progress.status = 'COMPLETED'
        progress.progress = 100
        progress.completed_at = timezone.now()

        if not progress.started_at:
            progress.started_at = timezone.now()

        progress.save()

        # UPDATE SKILL PROGRESS
    

        modules = roadmap_skill.learning_modules.filter(
            is_active=True
        )

        total_modules = modules.count()

        completed_modules = UserModuleProgress.objects.filter(
            user=request.user,
            module__in=modules,
            status='COMPLETED'
        ).count()

        if total_modules > 0:

            skill_progress = (
                Decimal(completed_modules)
                / Decimal(total_modules)
            ) * Decimal('100')

        else:
            skill_progress = Decimal('0')

        roadmap_skill.progress = skill_progress

        if skill_progress >= Decimal('100'):
            roadmap_skill.status = 'COMPLETED'
        elif skill_progress > Decimal('0'):
            roadmap_skill.status = 'IN_PROGRESS'
        else:
            roadmap_skill.status = 'NOT_STARTED'

        roadmap_skill.save()

        # UPDATE ROADMAP PROGRESS

        roadmap_skills = roadmap.roadmap_skills.all()

        if roadmap_skills.exists():

            total_progress = sum(skill.progress for skill in roadmap_skills)

            roadmap.overall_progress = (total_progress / Decimal(roadmap_skills.count()))
        else:

            roadmap.overall_progress = Decimal('0')

        roadmap.save()

        return redirect('skill_learning',career_slug=career.slug,skill_id=skill_id)

    return render(
        request,
        'roadmaps/module_learning.html',
        {
            'career': career,
            'roadmap': roadmap,
            'roadmap_skill': roadmap_skill,
            'module': module,
            'progress': progress,
        }
    )