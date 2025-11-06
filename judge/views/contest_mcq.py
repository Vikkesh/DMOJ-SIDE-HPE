from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext as _
from django.views.generic import DetailView, ListView, View
from django.utils import timezone

from judge.models import Contest, ContestMCQ, MCQQuestion, MCQOption, MCQSubmission, ContestParticipation
from judge.utils.views import TitleMixin, generic_message

__all__ = ['ContestMCQListView', 'ContestMCQDetailView', 'ContestMCQSubmitView']


class ContestMCQMixin:
    """Mixin to handle contest access and participation checks"""
    
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        contest_key = kwargs.get('contest')
        self.contest = get_object_or_404(Contest, key=contest_key)
        
        # Check if user can access the contest
        try:
            self.contest.access_check(request.user)
        except (Contest.Inaccessible, Contest.PrivateContest):
            raise Http404()
        
        # Get user's participation if they are in contest
        self.participation = None
        if request.user.is_authenticated:
            self.participation = ContestParticipation.objects.filter(
                contest=self.contest,
                user=request.user.profile,
                virtual=ContestParticipation.LIVE
            ).first()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contest'] = self.contest
        context['participation'] = self.participation
        context['in_contest'] = self.participation is not None and not self.participation.ended
        context['can_participate'] = (
            self.request.user.is_authenticated and 
            self.contest.started and 
            not self.contest.ended
        )
        return context


class ContestMCQListView(ContestMCQMixin, TitleMixin, ListView):
    """View to display all MCQ questions in a contest"""
    template_name = 'contest/mcq_list.html'
    context_object_name = 'contest_mcqs'
    
    def get_title(self):
        return _('MCQ Questions - %s') % self.contest.name
    
    def get_queryset(self):
        # Get all MCQ questions for this contest, ordered by their position
        return ContestMCQ.objects.filter(
            contest=self.contest
        ).select_related('mcq_question').order_by('order')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get user's submissions for these MCQs if authenticated
        if self.request.user.is_authenticated:
            mcq_ids = [cm.mcq_question_id for cm in context['contest_mcqs']]
            
            if self.participation:
                # Get contest submissions
                submissions = MCQSubmission.objects.filter(
                    user=self.request.user.profile,
                    question_id__in=mcq_ids,
                    participation=self.participation
                ).values('question_id', 'is_correct', 'points_earned')
            else:
                # Get regular submissions
                submissions = MCQSubmission.objects.filter(
                    user=self.request.user.profile,
                    question_id__in=mcq_ids,
                    participation__isnull=True
                ).values('question_id', 'is_correct', 'points_earned')
            
            # Create a dictionary for easy lookup
            submission_dict = {s['question_id']: s for s in submissions}
            context['user_submissions'] = submission_dict
        else:
            context['user_submissions'] = {}
        
        return context


class ContestMCQDetailView(ContestMCQMixin, TitleMixin, DetailView):
    """View to display a single MCQ question in contest and allow answering"""
    template_name = 'contest/mcq_detail.html'
    context_object_name = 'contest_mcq'
    
    def get_object(self):
        mcq_code = self.kwargs.get('mcq_code')
        return get_object_or_404(
            ContestMCQ,
            contest=self.contest,
            mcq_question__code=mcq_code
        )
    
    def get_title(self):
        return self.object.mcq_question.name
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mcq_question = self.object.mcq_question
        
        # Get options for this question
        context['options'] = mcq_question.options.all().order_by('order')
        
        # Check if user has already submitted
        context['previous_submission'] = None
        if self.request.user.is_authenticated:
            if self.participation:
                # Check for contest submission
                submission = MCQSubmission.objects.filter(
                    user=self.request.user.profile,
                    question=mcq_question,
                    participation=self.participation
                ).first()
            else:
                # Check for regular submission
                submission = MCQSubmission.objects.filter(
                    user=self.request.user.profile,
                    question=mcq_question,
                    participation__isnull=True
                ).first()
            
            if submission:
                context['previous_submission'] = submission
                context['selected_option_ids'] = list(
                    submission.selected_options.values_list('id', flat=True)
                )
        
        context['mcq_question'] = mcq_question
        context['contest_points'] = self.object.points
        
        return context


class ContestMCQSubmitView(LoginRequiredMixin, ContestMCQMixin, View):
    """Handle MCQ answer submission in contest"""
    
    def post(self, request, *args, **kwargs):
        mcq_code = kwargs.get('mcq_code')
        
        # Get the ContestMCQ object
        contest_mcq = get_object_or_404(
            ContestMCQ,
            contest=self.contest,
            mcq_question__code=mcq_code
        )
        
        mcq_question = contest_mcq.mcq_question
        
        # Check if contest allows submissions
        if not self.contest.started:
            return JsonResponse({
                'success': False,
                'error': _('Contest has not started yet.')
            }, status=400)
        
        if self.contest.ended and not self.participation:
            return JsonResponse({
                'success': False,
                'error': _('Contest has ended.')
            }, status=400)
        
        # Check if user is in contest
        if self.participation and self.participation.ended:
            return JsonResponse({
                'success': False,
                'error': _('Your contest time has ended.')
            }, status=400)
        
        # Get selected options
        selected_option_ids = request.POST.getlist('options[]')
        
        # Create or update submission
        if self.participation:
            # Contest submission
            submission, created = MCQSubmission.objects.get_or_create(
                user=request.user.profile,
                question=mcq_question,
                participation=self.participation,
                contest_object=contest_mcq,
                defaults={'submitted_at': timezone.now()}
            )
        else:
            # Regular submission (practice mode)
            submission, created = MCQSubmission.objects.get_or_create(
                user=request.user.profile,
                question=mcq_question,
                participation__isnull=True,
                contest_object=contest_mcq,
                defaults={'submitted_at': timezone.now()}
            )
        
        # Update submission time if not newly created
        if not created:
            submission.submitted_at = timezone.now()
            submission.save()
        
        # Clear previous selections
        submission.selected_options.clear()
        
        # Add selected options
        if selected_option_ids:
            selected_options = MCQOption.objects.filter(
                id__in=selected_option_ids,
                question=mcq_question
            )
            submission.selected_options.set(selected_options)
        else:
            # No options selected
            selected_options = MCQOption.objects.none()
        
        # Calculate score using contest points
        original_points = mcq_question.points
        mcq_question.points = contest_mcq.points  # Use contest points temporarily
        submission.calculate_score()
        mcq_question.points = original_points  # Restore original points
        
        # Get correct options
        correct_options = list(mcq_question.options.filter(is_correct=True).values_list('id', flat=True))
        
        return JsonResponse({
            'success': True,
            'is_correct': submission.is_correct,
            'points_earned': submission.points_earned,
            'max_points': contest_mcq.points,
            'correct_options': correct_options,
            'message': _('Correct!') if submission.is_correct else _('Incorrect.')
        })
