from django.shortcuts import render
from django.views import View
from django.shortcuts import reverse, redirect
from .forms import *
from .models import LatestNews

class AdminLatestNewsManager(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            latest_news = LatestNews.objects.all()

            form = NewLatestNewsForm()
            ctx = {
                'form': form,
                'latest_news': latest_news,
            }
            return render(request, 'admin_latest_news.html', ctx)
        else:
            return redirect(reverse('homepage'))

    def post(self, request):
        if request.user.is_authenticated and request.user.is_superuser:
            form = NewLatestNewsForm(request.POST, request.FILES)
            latest_news = LatestNews.objects.all()
            if form.is_valid():
                latest_new = form.save(commit=False)
                latest_new.author = request.user
                latest_new.save()

                ctx = {
                    'latest_news': latest_news,
                    'form': form,
                    'msg_success': 'Latest News saved successfully!'
                }
                return render(request, 'admin_latest_news.html', ctx)
            else:
                ctx = {
                    'latest_news': latest_news,
                    'form': form,
                    'msg_failed': 'Form has invalid data. Try again.'
                }
                return render(request, 'admin_latest_news.html', ctx)
        else:
            return redirect(reverse('homepage'))

class AdminLatestNewManager(View):
    def get(self, request, _id):
        if request.user.is_authenticated and request.user.is_superuser:
            latest_news = LatestNews.objects.filter(pk=_id).first()
            form = NewLatestNewsForm({
                'title': latest_news.title,
                'text': latest_news.text,
            })

            ctx = {
                'form': form,
                'latest_news': latest_news,
            }
            return render(request, 'admin_latest_news_edit.html', ctx)
        else:
            return redirect(reverse('homepage'))

    def post(self, request, _id=None):
        if request.user.is_authenticated and request.user.is_superuser:

            latest_news = LatestNews.objects.filter(pk=_id).first()
            form = NewLatestNewsForm({
                'title': latest_news.title,
                'text': latest_news.text,
                'image': latest_news.image,
            }, request.FILES)

            edit = request.POST.get('edit', False)
            delete = request.POST.get('delete', False)
            if edit:
                form = NewLatestNewsForm(request.POST, request.FILES)
                if form.is_valid():
                    form_latest_news = form.save(commit=False)
                    # Should change the author?
                    latest_news.author = request.user
                    latest_news.title = form_latest_news.title
                    latest_news.text = form_latest_news.text
                    if form_latest_news.image:
                        latest_news.image = form_latest_news.image
                    latest_news.save()
            elif delete:
                latest_news.delete()
                return redirect(reverse('admin_latest_news'))

            ctx = {
                'form': form,
                'latest_news': latest_news,
            }
            return render(request, 'admin_latest_news_edit.html', ctx)
        else:
            return redirect(reverse('homepage'))