from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import JsonResponse, FileResponse
from django.views.generic import ListView, FormView, DetailView, TemplateView
from django.shortcuts import redirect
from django.urls import reverse_lazy

from .forms import CreateSchemas, EmptySchemaColumn
from .models import SchemaModel, CreatedCSV
from .services.create_schema import get_cleared_data_from_request
from .services.schema.schema import get_schema, get_schema_data_with_column_id
from .services.schemas import get_schemas_completed_for_template


class CustomLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy('login')


class Login(LoginView):
    template_name = 'createCSV/login.html'
    redirect_authenticated_user = reverse_lazy('schemas')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        context['css'] = 'login.css'
        return context

    def get_success_url(self):
        return reverse_lazy('schemas')


class Schemas(CustomLoginRequiredMixin, ListView):
    model = SchemaModel
    template_name = 'createCSV/schemas.html'
    context_object_name = 'schemas'

    def get_queryset(self):
        return get_schemas_completed_for_template(owner=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Schemas'
        context['css'] = 'schemas.css'
        return context


class CreateSchema(CustomLoginRequiredMixin, FormView):
    form_class = CreateSchemas
    template_name = 'createCSV/create_schema.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Schema'
        context['css'] = 'create_schema.css'
        context['empty_column'] = EmptySchemaColumn()
        return context

    def post(self, request, *args, **kwargs):
        try:
            schema_data, columns = get_cleared_data_from_request(request.POST.dict())
            SchemaModel(owner=request.user,
                        title=schema_data['name'],
                        delimiter=schema_data['delimiter'],
                        quotechar=schema_data['quotechar']).save(columns=columns)
            return JsonResponse(data={'success': True}, status=201)
        except ValueError as error:
            return JsonResponse(data={'error': error.__str__()}, status=400)


class Schema(CustomLoginRequiredMixin, TemplateView):
    model = SchemaModel
    template_name = 'createCSV/schema.html'
    context_object_name = 'created_by_schema'

    def post(self, request, *args, **kwargs):
        schema = SchemaModel.objects.get(pk=kwargs['pk'])
        CreatedCSV(schema=schema).save(row_number=int(request.POST.get('row_number')))
        return JsonResponse(data={'success': True, 'file status': 'Reade'})

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Schema'
        context['css'] = 'schema.css'
        context['created_by_schema'] = CreatedCSV.objects.select_related('schema'
                                                                         ).filter(schema__id=kwargs['pk'],
                                                                                  schema__owner=self.request.user)
        if context['created_by_schema']:
            schema = context['created_by_schema'][0].schema
        else:
            schema = SchemaModel.objects.get(owner=self.request.user, pk=kwargs['pk'])
        context['schema_columns'] = get_schema_data_with_column_id(get_schema(schema.csv_file.path,
                                                                              schema.delimiter,
                                                                              schema.quotechar))
        return context


def logout_user(request):
    logout(request)
    return redirect('login')


def download_csv_file(request, pk):
    if request.method == 'GET':
        created_file = CreatedCSV.objects.select_related('schema').get(pk=pk, schema__owner=request.user)
        return FileResponse(created_file.file.open(), as_attachment=True,
                            filename=f'{created_file.schema.title}.{created_file.file.name.split(".")[-1]}')
    else:
        return JsonResponse(data={'error': 'Not Found'}, status=404)
