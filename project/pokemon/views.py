from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView
from project.pokemon.models import Pokemon, Type
from project.pokemon.serializers import PokemonDetailSerializer


@method_decorator(cache_page(600), name='get')
class PokemonListView(ListView):
    model = Pokemon
    template_name = "pokemon/list.html"
    context_object_name = "pokemons"
    paginate_by = 24

    def get_queryset(self):
        queryset = super().get_queryset()

        if search_query := self.request.GET.get("search"):
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(species__name__icontains=search_query)
            )

        if type_filter := self.request.GET.get("type"):
            try:
                type_ids = [int(t) for t in type_filter.split(",") if t]
                queryset = queryset.filter(types__id__in=type_ids).distinct()
            except ValueError:
                pass

        queryset = queryset.select_related("species").prefetch_related("types")

        return queryset.order_by("order")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["types"] = dict(Type.objects.all().values_list("id", "name"))
        if view_mode := self.request.GET.get("view", None):
            context["view_mode"] = view_mode
        return context


@method_decorator(cache_page(60 * 60), name='get')
class PokemonDetailView(DetailView):
    model = Pokemon
    template_name = 'pokemon/detail.html'
    context_object_name = 'pokemon'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        serializer = PokemonDetailSerializer(self.object)
        context['pokemon'] = serializer.data
        return context
