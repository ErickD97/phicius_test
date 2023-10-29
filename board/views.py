from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, ListView

from django_tables2 import SingleTableMixin
from django_filters.views import FilterView

from board.filters import BoardFilter
from board.forms import CreateBoardForm
from board.models import Board
from board.tables import BoardTable

User = get_user_model()


class BoardList(SingleTableMixin, FilterView):
    template_name = "board/board_list.html"
    paginate_by = 8
    table_class = BoardTable
    filterset_class = BoardFilter
    context_object_name = "board_list"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset.filter(
            Q(player_cross=self.request.user) | Q(player_circle=self.request.user)
        )
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        games_as_circle = self.request.user.circle.all()
        context["boards_as_circle"] = games_as_circle
        context["victories_as_circle"] = games_as_circle.filter(status=3).count()
        context["draws_as_circle"] = games_as_circle.filter(status=4).count()
        games_as_cross = self.request.user.cross.all()
        context["boards_as_cross"] = games_as_cross
        context["victories_as_cross"] = games_as_cross.filter(status=2).count()
        context["draws_as_cross"] = games_as_cross.filter(status=4).count()
        return context

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        kwargs['request'] = self.request
        return kwargs

board_list = BoardList.as_view()


@method_decorator(login_required, name="dispatch")
class CreateBoard(CreateView):
    model = Board
    form_class = CreateBoardForm
    success_url = reverse_lazy("board:board_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user_id"] = self.request.user.pk
        return kwargs

    def form_valid(self, form):
        try:
            with transaction.atomic():
                cross_or_circle = int(form.cleaned_data["cross_or_circle"])
                opponent = form.cleaned_data["opponent"]
                player_circle = self.request.user if cross_or_circle == 1 else opponent
                player_cross = self.request.user if cross_or_circle == 2 else opponent
                Board.objects.create(
                    player_cross=player_cross,
                    player_circle=player_circle,
                )
        except Exception as e:
            pass
        return HttpResponseRedirect(self.success_url)


create_board = CreateBoard.as_view()


@method_decorator(login_required, name="dispatch")
class BoardPlay(DetailView):
    model = Board


board_play = BoardPlay.as_view()
