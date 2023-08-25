

from django.shortcuts import render, redirect
from .models import Question, QuizType, Answer
from realacc.models import Paid_quizz, Account, Pay_quizz
from django.contrib import messages
from decimal import Decimal
import logging


def quiz_view_02(request):
    quiz_types = QuizType.objects.all()
    selected_quiz_type_id = request.GET.get('quiz_type_02')

    if selected_quiz_type_id:
        questionsss = Question.objects.filter(quiz_type__id=selected_quiz_type_id).order_by('?')[:3]
    else:
        questionsss = []

    total_quiz_duration = sum(question.timer_duration for question in questionsss)

    context = {
        'questionsss': questionsss,
        'quiz_types': quiz_types,
        'selected_quiz_type_id': selected_quiz_type_id,
        'total_quiz_duration': total_quiz_duration,
    }

    return render(request, 'quizzes_02/quiz_02.html', context)





logger = logging.getLogger(__name__)

def results_02(request):
    questionsss = Question.objects.all()
    if request.method == 'POST':
        score = 0
        displayed_questions = len(request.POST) - 1  # Subtract 1 for the CSRF token
        
        for question in questionsss:
            selected_answer_id = request.POST.get('question_02' + str(question.id))
            if selected_answer_id:
                selected_answer = Answer.objects.get(pk=selected_answer_id)
                if selected_answer.is_correct:
                    score += 1

        passing_score = int(0.9 * displayed_questions)
        passed = score >= passing_score
    
        context = {
            'questionsss': questionsss,
            'score': score,
            'total_questions': displayed_questions,
            'passing_score': passing_score,
            'passed': passed,
        }

        if passed:
            try:
                payquizzes = Pay_quizz.objects.get(user=request.user)
                payquizzzes_amount = payquizzes.amount 
                paidquizzzes_amount = int(payquizzzes_amount * 10)

                account = Account.objects.get(user=request.user)
                account.balance += Decimal(paidquizzzes_amount)  # Convert to Decimal
                account.save()

                Paid_quizz.objects.create(user=request.user, amount=Decimal(paidquizzzes_amount))
                messages.success(request, f'Congratulations! You have won {paidquizzzes_amount} paid quizzes.')

                return render(request, 'quizzes_02/congs_02.html')
            except Pay_quizz.DoesNotExist:
                logger.error("Pay_quizz entry not found for user: %s", request.user)
            except Exception as e:
                logger.error("Error: %s", e)
                messages.error(request, "An error occurred while processing your request.")

        return render(request, 'quizzes_02/results_02.html', context)

    return redirect('quiz_view_02')





