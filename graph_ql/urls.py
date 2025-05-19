from django.urls import path

# GraphQL
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from .schema import schema

# urls.py
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class SuperuserGraphQLView(GraphQLView):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser and not request.user.is_staff:
            return JsonResponse({"error": "Access denied"}, status=403)
        return super().dispatch(request, *args, **kwargs)


urlpatterns = [
    # GraphQL
    path("", csrf_exempt(SuperuserGraphQLView.as_view(graphiql=True, schema=schema))),
]
