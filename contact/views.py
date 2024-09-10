from django.shortcuts import redirect
from django.views.generic.edit import CreateView

from .forms import ContactUsModelForm

# DRF Imports
from rest_framework.response import Response
from .serializer import ContactUsSerializer
# DRF Generics
from rest_framework import generics, status
# DRF Auth
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


# Create your views here.

def store_file(file):  # put file into a pieces for lower memory consuming
    with open('temp/image.jpg', "wb+") as dest:
        for chunk in file.chunks():
            dest.write(chunk)


# Class Base Views

class ContactUsView(CreateView):  # contract : at the end of class name use View
    # class ContactUsView(CreateView):  # contract : at the end of class name use View
    # auto-detect get and post
    # model = ContactUs # because it defines in ContactUsModelForm no need to define again
    template_name = 'contact/contact_us.html'
    form_class = ContactUsModelForm

    # fields = ['name', 'email', 'subject', 'message']

    # model = ContactUs
    # fields = '__all__'
    # success_url = '/contact-us/'

    def form_valid(self, form):
        form.save()
        return redirect('home-page')

    def get_context_data(self, **kwargs):
        context = super(ContactUsView, self).get_context_data()
        context['current_page'] = 'contact'
        context['contact_img'] = None  # Temporary Disabled
        return context


# DRF region
class ContactUsGenericApiView(generics.CreateAPIView):
    serializer_class = ContactUsSerializer

    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except:
            return Response(None, status=status.HTTP_400_BAD_REQUEST)

# endregion
