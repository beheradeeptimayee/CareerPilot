from django.shortcuts import render,get_object_or_404,redirect

# Create your views here.
from assessments.models import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from decimal import Decimal

def assessment_intro(request, career_slug):
    assessment = get_object_or_404(
        Assessment.objects.select_related('career'),
        career__slug=career_slug,
        is_active=True
    )

    return render(
        request,
        'assessments/assessment_intro.html',
        {
            'assessment': assessment
        }
    )


@login_required
def start_assessment(request, career_slug):

    assessment = get_object_or_404(
        Assessment.objects.select_related('career'),
        career__slug=career_slug,
        is_active=True
    )

    attempt = AssessmentAttempt.objects.create(
        user=request.user,
        assessment=assessment
    )

    return redirect(
        'assessment_question',
        attempt_id=attempt.id
    )


@login_required
def assessment_question(request, attempt_id):

    attempt = get_object_or_404(
        AssessmentAttempt.objects.select_related('assessment'),
        id=attempt_id,
        user=request.user,
        status='IN_PROGRESS'
    )

    answered_question_ids = attempt.answers.values_list(
        'question_id',
        flat=True
    )

    question = (
        attempt.assessment.questions
        .exclude(id__in=answered_question_ids)
        .order_by('order')
        .first()
    )

    if not question:
        return redirect(
            'assessment_complete',
            attempt_id=attempt.id
        )

    if request.method == 'POST':

        selected_option_id = request.POST.get(
            'selected_option'
        )

        selected_option = get_object_or_404(
            question.options,
            id=selected_option_id
        )

        is_correct = selected_option.is_correct

        marks_awarded = (
            question.marks
            if is_correct
            else 0
        )

        AssessmentAnswer.objects.create(
            attempt=attempt,
            question=question,
            selected_option=selected_option,
            is_correct=is_correct,
            marks_awarded=marks_awarded
        )

        return redirect(
            'assessment_question',
            attempt_id=attempt.id
        )

    return render(
        request,
        'assessments/assessment_question.html',
        {
            'attempt': attempt,
            'question': question,
        }
    )


@login_required
def assessment_complete(request, attempt_id):

    attempt = get_object_or_404(
        AssessmentAttempt.objects.select_related('assessment'),
        id=attempt_id,
        user=request.user
    )

    answers = attempt.answers.select_related(
        'question__skill'
    )

    
    # Overall assessment score
    
    total_questions = answers.count()

    correct_answers = answers.filter(
        is_correct=True
    ).count()

    if total_questions > 0:

        score = (
            Decimal(correct_answers)
            / Decimal(total_questions)
        ) * Decimal('100')

    else:

        score = Decimal('0')

    attempt.total_score = score
    attempt.status = 'COMPLETED'
    attempt.completed_at = timezone.now()
    attempt.save()

    
    # Calculate skill-wise performance


    skill_data = {}

    for answer in answers:

        skill = answer.question.skill

        if skill.id not in skill_data:

            skill_data[skill.id] = {
                'skill': skill,
                'attempted': 0,
                'correct': 0,
            }

        skill_data[skill.id]['attempted'] += 1

        if answer.is_correct:

            skill_data[skill.id]['correct'] += 1

    
    # Remove old results if this
    # completion is processed again
    

    attempt.skill_results.all().delete()

    skill_results = []

    
    # Create SkillResult records
    

    for data in skill_data.values():

        attempted = data['attempted']
        correct = data['correct']

        if attempted > 0:

            skill_score = (
                Decimal(correct)
                / Decimal(attempted)
            ) * Decimal('100')

        else:

            skill_score = Decimal('0')

        proficiency_level = (
            ProficiencyLevel.objects
            .filter(
                minimum_score__lte=skill_score,
                maximum_score__gte=skill_score
            )
            .first()
        )

        if proficiency_level:

            skill_result = SkillResult.objects.create(
                attempt=attempt,
                skill=data['skill'],
                score=skill_score,
                proficiency_level=proficiency_level,
                questions_attempted=attempted,
                questions_correct=correct,
            )

            skill_results.append(
                skill_result
            )

    
    # Separate strong and improvement skills

    strong_skills = [
        result
        for result in skill_results
        if result.score >= Decimal('70')
    ]

    improvement_skills = [
        result
        for result in skill_results
        if result.score < Decimal('70')
    ]

    # Render results page

    return render(
        request,
        'assessments/assessment_complete.html',
        {
            'attempt': attempt,
            'total_questions': total_questions,
            'correct_answers': correct_answers,
            'score': score,
            'skill_results': skill_results,
            'strong_skills': strong_skills,
            'improvement_skills': improvement_skills,
        }
    )