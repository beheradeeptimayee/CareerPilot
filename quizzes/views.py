from django.shortcuts import render,get_object_or_404,redirect

# Create your views here.
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from roadmaps.models import LearningModule, UserModuleProgress
from quizzes.models import Quiz,QuizAttempt,QuizAnswer

@login_required
def quiz_start(request, quiz_id):
    quiz = get_object_or_404(Quiz.objects.select_related('module'),id=quiz_id,is_active=True)
    attempt = QuizAttempt.objects.create(user=request.user,quiz=quiz,status='IN_PROGRESS')

    return redirect('quiz_question',attempt_id=attempt.id)


@login_required
def quiz_question(request, attempt_id):

    attempt = get_object_or_404(
        QuizAttempt.objects.select_related(
            'quiz',
            'quiz__module'
        ),
        id=attempt_id,
        user=request.user,
        status='IN_PROGRESS'
    )

    answered_ids = attempt.answers.values_list('question_id',flat=True)

    question = (
        attempt.quiz.questions
        .exclude(id__in=answered_ids)
        .prefetch_related('options')
        .first()
    )

    if not question:
        return redirect('quiz_complete',attempt_id=attempt.id)

    if request.method == 'POST':
        selected_option_id = request.POST.get('selected_option')
        selected_option = get_object_or_404(question.options,id=selected_option_id)
        is_correct = selected_option.is_correct

        marks_awarded = (question.marks if is_correct else 0)

        QuizAnswer.objects.create(
            attempt=attempt,
            question=question,
            selected_option=selected_option,
            is_correct=is_correct,
            marks_awarded=marks_awarded
        )

        return redirect('quiz_question',attempt_id=attempt.id)

    total_questions = attempt.quiz.questions.count()

    answered_count = attempt.answers.count()

    return render(
        request,
        'quizzes/quiz_question.html',
        {
            'attempt': attempt,
            'question': question,
            'total_questions': total_questions,
            'answered_count': answered_count,
        }
    )


@login_required
def quiz_complete(request, attempt_id):

    attempt = get_object_or_404(
        QuizAttempt.objects.select_related(
            'quiz',
            'quiz__module'
        ),
        id=attempt_id,
        user=request.user
    )

    answers = attempt.answers.select_related('question')

    total_marks = sum(answer.question.marks for answer in answers)

    obtained_marks = sum(answer.marks_awarded for answer in answers)

    if total_marks > 0:

        score = (Decimal(obtained_marks) / Decimal(total_marks)) * Decimal('100')
    else:
        score = Decimal('0')

    attempt.score = score
    attempt.status = 'COMPLETED'
    attempt.completed_at = timezone.now()
    attempt.save()

    passed = (score >= attempt.quiz.passing_score)

    module_progress = None

    if passed:

        module = attempt.quiz.module

        module_progress, created = (
            UserModuleProgress.objects.get_or_create(
                user=request.user,
                module=module
            )
        )

        module_progress.status = 'COMPLETED'
        module_progress.progress = 100

        if not module_progress.started_at:
            module_progress.started_at = timezone.now()

        module_progress.completed_at = timezone.now()

        module_progress.save()

        roadmap_skill = module.roadmap_skill

        modules = roadmap_skill.learning_modules.filter(is_active=True)

        total_modules = modules.count()

        completed_modules = UserModuleProgress.objects.filter(
            user=request.user,
            module__in=modules,
            status='COMPLETED'
        ).count()

        if total_modules > 0:
            skill_progress = (Decimal(completed_modules)/ Decimal(total_modules)) * Decimal('100')
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

        roadmap = roadmap_skill.roadmap

        roadmap_skills = roadmap.roadmap_skills.all()

        if roadmap_skills.exists():
            total_progress = sum(skill.progress for skill in roadmap_skills)
            roadmap.overall_progress = (total_progress  / Decimal(roadmap_skills.count()))
            roadmap.save()

    return render(
        request,
        'quizzes/quiz_complete.html',
        {
            'attempt': attempt,
            'score': score,
            'passed': passed,
            'module_progress': module_progress,
        }
    )