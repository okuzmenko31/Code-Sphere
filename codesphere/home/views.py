from django.shortcuts import render
from django.views import View


class WelcomePage(View):

    def get(self, *args, **kwargs):
        return render(self.request, 'home/welcome.html')
