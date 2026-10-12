
from decimal import Decimal
# Create your views.
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from assessments.models import (
    Assessment,
    AssessmentAttempt,
    AssessmentAnswer,
    SkillResult,
    ProficiencyLevel,
)
from careers.models import Career, CareerSkill


# ============================================================
# 1. ASSESSMENT INTRO
# ============================================================

def assessment_intro(request, career_slug):
    assessment = get_object_or_404(
        Assessment.objects.select_related("career"),
        career__slug=career_slug,
        is_active=True,
    )

    questions = assessment.questions.select_related("skill")

    question_count = questions.count()

    skills_covered = (
        questions
        .values("skill_id", "skill__name")
        .distinct()
        .order_by("skill__name")
    )

    context = {
        "assessment": assessment,
        "question_count": question_count,
        "skills_covered": skills_covered,
    }

    return render(
        request,
        "assessments/assessment_intro.html",
        context,
    )


# ============================================================
# 2. START ASSESSMENT
# ============================================================

@login_required
def start_assessment(request, career_slug):
    assessment = get_object_or_404(
        Assessment.objects.select_related("career"),
        career__slug=career_slug,
        is_active=True,
    )

    if not assessment.questions.exists():
        return render(
            request,
            "assessments/assessment_intro.html",
            {
                "assessment": assessment,
                "question_count": 0,
                "skills_covered": [],
                "error": (
                    "This assessment has no questions yet. "
                    "Please try again later."
                ),
            },
        )

    attempt = AssessmentAttempt.objects.create(
        user=request.user,
        assessment=assessment,
    )

    return redirect(
        "assessment_question",
        attempt_id=attempt.id,
    )


# ============================================================
# 3. ASSESSMENT QUESTIONS
# ============================================================

@login_required
def assessment_question(request, attempt_id):
    attempt = get_object_or_404(
        AssessmentAttempt.objects.select_related("assessment"),
        id=attempt_id,
        user=request.user,
        status="IN_PROGRESS",
    )

    answered_question_ids = attempt.answers.values_list(
        "question_id",
        flat=True,
    )

    question = (
        attempt.assessment.questions
        .exclude(id__in=answered_question_ids)
        .order_by("order", "id")
        .first()
    )

    # Redirect to results after all questions are answered.
    if question is None:
        return redirect(
            "assessment_complete",
            attempt_id=attempt.id,
        )

    if request.method == "POST":
        selected_option_id = request.POST.get("selected_option")

        if not selected_option_id:
            return render(
                request,
                "assessments/assessment_question.html",
                {
                    "attempt": attempt,
                    "question": question,
                    "error": "Please select an answer before continuing.",
                },
            )

        selected_option = get_object_or_404(
            question.options,
            id=selected_option_id,
        )

        # Avoid saving a duplicate answer.
        if attempt.answers.filter(question=question).exists():
            return redirect(
                "assessment_question",
                attempt_id=attempt.id,
            )

        is_correct = selected_option.is_correct

        marks_awarded = (
            question.marks if is_correct else 0
        )

        AssessmentAnswer.objects.create(
            attempt=attempt,
            question=question,
            selected_option=selected_option,
            is_correct=is_correct,
            marks_awarded=marks_awarded,
        )

        return redirect(
            "assessment_question",
            attempt_id=attempt.id,
        )

    return render(
        request,
        "assessments/assessment_question.html",
        {
            "attempt": attempt,
            "question": question,
        },
    )


# ============================================================
# 4. PROFICIENCY LEVEL HELPER
# ============================================================

def get_proficiency_name(score):
    """
    Return the proficiency name as text because
    SkillResult.proficiency_level is a CharField,
    not a ForeignKey.
    """

    level = (
        ProficiencyLevel.objects.filter(
            minimum_score__lte=score,
            maximum_score__gte=score,
        )
        .order_by("minimum_score")
        .first()
    )

    if level:
        return level.name

    # Fallback if no matching ProficiencyLevel record exists.
    if score >= Decimal("80"):
        return "Advanced"
    elif score >= Decimal("60"):
        return "Intermediate"
    elif score >= Decimal("40"):
        return "Beginner"
    else:
        return "Needs Practice"


# ============================================================
# 5. ASSESSMENT COMPLETE / RESULTS
# ============================================================
@login_required
def assessment_complete(request, attempt_id):
    attempt = get_object_or_404(
        AssessmentAttempt.objects.select_related(
            "assessment",
            "assessment__career",
        ),
        id=attempt_id,
        user=request.user,
    )

    total_questions = attempt.assessment.questions.count()

    # Do not finish an assessment if questions are unanswered.
    if attempt.status == "IN_PROGRESS":
        if attempt.answers.count() < total_questions:
            return redirect(
                "assessment_question",
                attempt_id=attempt.id,
            )

    answers = list(
        attempt.answers.select_related(
            "question",
            "question__skill",
        )
    )

    answered_questions = len(answers)
    correct_answers = sum(
        1 for answer in answers if answer.is_correct
    )

    if total_questions:
        score = (
            Decimal(correct_answers)
            / Decimal(total_questions)
            * Decimal("100")
        ).quantize(Decimal("0.01"))
    else:
        score = Decimal("0.00")

    # Rebuild results if this attempt is new or its results are missing.
    if (
        attempt.status != "COMPLETED"
        or not attempt.skill_results.exists()
    ):
        with transaction.atomic():
            skill_data = {}

            for answer in answers:
                skill = answer.question.skill

                if skill.id not in skill_data:
                    skill_data[skill.id] = {
                        "skill": skill,
                        "attempted": 0,
                        "correct": 0,
                    }

                skill_data[skill.id]["attempted"] += 1

                if answer.is_correct:
                    skill_data[skill.id]["correct"] += 1

            # Remove incomplete results before rebuilding them.
            attempt.skill_results.all().delete()

            for data in skill_data.values():
                attempted = data["attempted"]
                correct = data["correct"]

                if attempted == 0:
                    continue

                skill_score = (
                    Decimal(correct) / Decimal(attempted)
                    * Decimal("100")
                ).quantize(Decimal("0.01"))

                level = ProficiencyLevel.objects.filter(
                    minimum_score__lte=skill_score,
                    maximum_score__gte=skill_score,
                ).order_by("minimum_score").first()

                # Store a string because proficiency_level is a CharField.
                if level:
                    proficiency_name = level.name
                elif skill_score >= 80:
                    proficiency_name = "Advanced"
                elif skill_score >= 60:
                    proficiency_name = "Intermediate"
                elif skill_score >= 40:
                    proficiency_name = "Beginner"
                else:
                    proficiency_name = "Needs Practice"

                SkillResult.objects.create(
                    attempt=attempt,
                    skill=data["skill"],
                    score=skill_score,
                    proficiency_level=proficiency_name,
                    questions_attempted=attempted,
                    questions_correct=correct,
                )

            attempt.total_score = score
            attempt.status = "COMPLETED"

            if not attempt.completed_at:
                attempt.completed_at = timezone.now()

            attempt.save(
                update_fields=[
                    "total_score",
                    "status",
                    "completed_at",
                ]
            )

    # Load saved results. Only "skill" is a database relationship here.
    skill_results = list(
        SkillResult.objects.filter(
            attempt=attempt,
        ).select_related(
            "skill",
        ).order_by("skill__name")
    )

    strong_skills = [
        result.skill.name
        for result in skill_results
        if result.score >= Decimal("70")
    ]

    improvement_skills = [
        result.skill.name
        for result in skill_results
        if result.score < Decimal("70")
    ]

    context = {
        "attempt": attempt,
        "total_questions": total_questions,
        "answered_questions": answered_questions,
        "correct_answers": correct_answers,
        "score": score,
        "skill_results": skill_results,
        "strong_skills": strong_skills,
        "improvement_skills": improvement_skills,
    }

    return render(
        request,
        "assessments/assessment_complete.html",
        context,
    )
# ============================================================
# 6. SKILL GAP ANALYSIS
# ============================================================

@login_required
def skill_gap_analysis(request, career_slug):
    career = get_object_or_404(
        Career,
        slug=career_slug,
        is_active=True,
    )

    # Find the latest completed assessment for this career.
    attempt = (
        AssessmentAttempt.objects.filter(
            user=request.user,
            assessment__career=career,
            status="COMPLETED",
        )
        .order_by("-completed_at", "-id")
        .first()
    )

    skill_results = {}

    if attempt:
        results = (
            SkillResult.objects.filter(attempt=attempt)
            .select_related("skill")
        )

        for result in results:
            skill_results[result.skill_id] = result

    # Skills required for the selected career.
    career_skills = (
        CareerSkill.objects.filter(career=career)
        .select_related("skill")
        .order_by("skill__name")
    )

    skill_gap_data = []

    for career_skill in career_skills:
        result = skill_results.get(career_skill.skill_id)

        target_score = Decimal(
            str(career_skill.target_proficiency)
        )

        if result:
            current_score = Decimal(str(result.score))

            gap = max(
                target_score - current_score,
                Decimal("0"),
            )

            if current_score >= target_score:
                status = "Strong"
            elif current_score >= target_score - Decimal("20"):
                status = "Moderate"
            else:
                status = "Needs Improvement"

        else:
            current_score = None
            gap = target_score
            status = "Not Assessed"

        skill_gap_data.append({
            "skill": career_skill.skill,
            "importance": career_skill.importance,
            "current_score": current_score,
            "target_score": target_score,
            "gap": gap,
            "status": status,
        })

    # Calculate readiness using skills that were assessed.
    assessed_skills = [
        item
        for item in skill_gap_data
        if item["current_score"] is not None
    ]

    assessed_skills_count = len(assessed_skills)

    if assessed_skills:
        total_current_score = sum(
            (
                item["current_score"]
                for item in assessed_skills
            ),
            Decimal("0"),
        )

        overall_readiness = (
            total_current_score
            / Decimal(assessed_skills_count)
        )
    else:
        overall_readiness = Decimal("0")

    # Prioritize skills with the largest gaps.
    focus_areas = sorted(
        [
            item
            for item in skill_gap_data
            if item["status"] in [
                "Moderate",
                "Needs Improvement",
                "Not Assessed",
            ]
        ],
        key=lambda item: item["gap"],
        reverse=True,
    )

    context = {
        "career": career,
        "attempt": attempt,
        "skill_gap_data": skill_gap_data,
        "overall_readiness": overall_readiness,
        "assessed_skills_count": assessed_skills_count,
        "focus_areas": focus_areas,
    }

    return render(
        request,
        "assessments/skill_gap.html",
        context,
    )
