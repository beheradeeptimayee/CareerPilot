from django.shortcuts import render,get_object_or_404,redirect

# Create your views here.
from assessments.models import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from decimal import Decimal
from careers.models import  Career,CareerSkill

# ASSESSMENT INTRO

def assessment_intro(request, career_slug):

    assessment = get_object_or_404(
        Assessment.objects.select_related('career'),career__slug=career_slug,is_active=True)

    return render(request,'assessments/assessment_intro.html',{'assessment': assessment})


# START ASSESSMENT

@login_required
def start_assessment(request, career_slug):

    assessment = get_object_or_404(Assessment.objects.select_related('career'),career__slug=career_slug,is_active=True)

    attempt = AssessmentAttempt.objects.create(user=request.user,assessment=assessment)
    
    return redirect('assessment_question',attempt_id=attempt.id)

# ASSESSMENT QUESTION

@login_required
def assessment_question(request, attempt_id):

    attempt = get_object_or_404(
        AssessmentAttempt.objects.select_related('assessment'),
        id=attempt_id,
        user=request.user,
        status='IN_PROGRESS'
    )

    answered_question_ids = attempt.answers.values_list('question_id',flat=True)

    question = (
        attempt.assessment.questions
        .exclude(id__in=answered_question_ids)
        .order_by('order')
        .first()
    )

    if not question:

        return redirect('assessment_complete',attempt_id=attempt.id)

    if request.method == 'POST':

        selected_option_id = request.POST.get('selected_option')

        selected_option = get_object_or_404(question.options,id=selected_option_id)

        is_correct = selected_option.is_correct

        marks_awarded = (question.marks if is_correct else 0)

        AssessmentAnswer.objects.create(
            attempt=attempt,
            question=question,
            selected_option=selected_option,
            is_correct=is_correct,
            marks_awarded=marks_awarded
        )

        return redirect('assessment_question',attempt_id=attempt.id)

    return render(request,'assessments/assessment_question.html',{'attempt': attempt,'question': question,})

# ASSESSMENT COMPLETE / RESULTS

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

    correct_answers = answers.filter(is_correct=True).count()

    if total_questions > 0:

        score = (Decimal(correct_answers) / Decimal(total_questions)) * Decimal('100')

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


    # Remove old results if processed again
    
    attempt.skill_results.all().delete()

    skill_results = []

    # Create SkillResult records
    
    for data in skill_data.values():

        attempted = data['attempted']
        correct = data['correct']

        if attempted > 0:

            skill_score = (Decimal(correct) / Decimal(attempted)) * Decimal('100')

        else:

            skill_score = Decimal('0')

        proficiency_level = (
            ProficiencyLevel.objects.filter(minimum_score__lte=skill_score,maximum_score__gte=skill_score).first()
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
        if result.score >= Decimal('70')]

    improvement_skills = [
        result
        for result in skill_results
        if result.score < Decimal('70')]

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

# SKILL GAP ANALYSIS

@login_required
def skill_gap_analysis(request, career_slug):

    # Get the career
    
    career = get_object_or_404(Career,slug=career_slug,is_active=True)
    # Get user's latest completed attempt
    # for this career
    
    attempt = (
        AssessmentAttempt.objects.filter(
            user=request.user,
            assessment__career=career,
            status='COMPLETED').order_by('-completed_at').first())

    # Get skill results
    
    skill_results = {}

    if attempt:

        results = (
            SkillResult.objects.filter(attempt=attempt).select_related('skill')
        )

        for result in results:

            skill_results[result.skill_id] = result

    # Get required skills for career
    
    career_skills = (
        CareerSkill.objects
        .filter(career=career)
        .select_related('skill')
        .order_by('-importance', 'skill__name')
    )

    # Calculate skill gaps
    
    skill_gap_data = []

    for career_skill in career_skills:

        result = skill_results.get(career_skill.skill_id)

        target_score = career_skill.target_proficiency

        if result:

            current_score = result.score

            gap = max(target_score - current_score,Decimal('0'))

            if current_score >= target_score:

                status = 'Strong'

            elif current_score >= (target_score - Decimal('20')):

                status = 'Moderate'

            else:

                status = 'Needs Improvement'

        else:

            current_score = None

            gap = target_score

            status = 'Not Assessed'

        skill_gap_data.append({
            'skill': career_skill.skill,
            'importance': career_skill.importance,
            'current_score': current_score,
            'target_score': target_score,
            'gap': gap,
            'status': status,
        })

    # OVERALL READINESS
    
    assessed_skills = [
        item
        for item in skill_gap_data
        if item['current_score'] is not None
    ]
    assessed_skills_count = len(assessed_skills)

    if assessed_skills:

        total_current_score = sum(
            item['current_score']
            for item in assessed_skills
        )

        overall_readiness = (
            total_current_score
            / Decimal(len(assessed_skills))
        )

    else:

        overall_readiness = Decimal('0')

    # FOCUS AREAS

    focus_areas = sorted(
    [
        item
        for item in skill_gap_data
        if item['status'] in [
            'Moderate',
            'Needs Improvement'
        ]
    ],
    key=lambda item: item['gap'],
    reverse=True
)
 
    # RENDER SKILL GAP PAGE

    return render(
        request,
        'assessments/skill_gap.html',
        {
            'career': career,
            'skill_gap_data': skill_gap_data,
            'overall_readiness': overall_readiness,
            'assessed_skills_count': assessed_skills_count,
            'focus_areas': focus_areas,
        }
    )