from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import ListView, DetailView
from project.pokemon.models import Pokemon, Type
from project.pokemon.serializers import PokemonDetailSerializer


@ensure_csrf_cookie
def csrf_token_view(request):
    return JsonResponse({"detail": "CSRF cookie set."})

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
                queryset = queryset.filter(types__id=type_filter)
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

class AddToCompareView(View):
    def post(self, request, pokemon_id):
        compare_list = request.session.get("compare_list", [])
        pokemon_id = int(pokemon_id)

        if pokemon_id in compare_list:
            compare_list.remove(pokemon_id)
        else:
            if len(compare_list) >= 4:
                compare_list = compare_list[-3:]
            compare_list.append(pokemon_id)

        request.session["compare_list"] = compare_list
        return JsonResponse({"compare_list": compare_list})

class PokemonCompareView(View):
    def get(self, request):
        id_list = request.session.get("compare_list", [])
        pokemons = Pokemon.objects.filter(id__in=id_list).prefetch_related("types", "abilities")
        return render(request, "pokemon/compare.html", {"pokemons": pokemons})
