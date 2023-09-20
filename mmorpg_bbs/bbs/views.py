from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.views.generic.edit import FormMixin

from .filters import AdFilter
from .forms import AdForm, AdImageForm, ResponseForm
from .models import Ad, Picture, Response


@login_required
def response_accept(request, pk):
    resp = Response.objects.get(pk=pk)
    acpt = resp.accepted
    resp.accepted = not acpt
    resp.save()
    messages.success(request, f"Response from {resp.user.username} {'rejected' if acpt else 'accepted'}!")
    return redirect(resp.ad.get_absolute_url())


@login_required
def response_delete(request, pk):
    resp = Response.objects.get(pk=pk)
    url = resp.ad.get_absolute_url()
    username = resp.user.username
    resp.delete()
    messages.success(request, f"Response from {username} 'deleted'!")
    return redirect(url)


class AdsList(ListView):
    model = Ad
    template_name = 'bbs/main.html'
    context_object_name = 'ads'
    ordering = '-created'
    paginate_by = 10


class AdDetail(FormMixin, DetailView):
    model = Ad
    template_name = 'bbs/ad.html'
    context_object_name = 'ad'
    form_class = ResponseForm

    def get_success_url(self):
        return reverse_lazy('bbs:detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(AdDetail, self).get_context_data(**kwargs)
        context['form'] = ResponseForm(initial={'ad': self.object, 'user': self.request.user})
        context['responses'] = Response.objects.filter(ad=self.object).order_by('-created')
        context['pictures'] = Picture.objects.filter(ad=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return super(AdDetail, self).form_valid(form)



class AdSearch(AdsList):
    template_name = 'bbs/search.html'
    paginate_by = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = AdFilter(self.request.GET, queryset=self.get_queryset())
        return context


@login_required
def create_ad(request, pk=None):
    if pk:
        instance = Ad.objects.get(pk=pk)
        caption = 'Edit Ad'
    else:
        instance = None
        caption = 'Create Ad'
    if request.method == "POST":
        form_ad = AdForm(request.POST, initial={'user': request.user})
        form_images = AdImageForm(request.POST, request.FILES)
        images = request.FILES.getlist('image')
        if form_ad.is_valid() and form_images.is_valid():
            if instance:
                instance.title=form_ad.cleaned_data['title']
                instance.text=form_ad.cleaned_data['text']
                instance.price=form_ad.cleaned_data['price']
                instance.category=form_ad.cleaned_data['category']
            else:
                instance = Ad.objects.create(
                    user=request.user,
                    title=form_ad.cleaned_data['title'],
                    text=form_ad.cleaned_data['text'],
                    price=form_ad.cleaned_data['price'],
                    category=form_ad.cleaned_data['category'],
                )
            instance.save()
            for img in images:
                pic = Picture.objects.create(ad=instance, image=img)
                pic.save()
            return redirect('bbs:main')
    else:
        
        form_ad = AdForm(initial={'user': request.user}, instance=instance)
        form_images = AdImageForm()
    context = {'form_ad': form_ad, 'form_images': form_images, 'caption': caption}
    return render(request, 'bbs/create.html', context)


class AdEdit(PermissionRequiredMixin, UpdateView):
    template_name = 'bbs/create.html'
    model = Ad
    fields = ('category', 'title', 'text','price')
    exclude = ('user',)
    permission_required = ('bbs.change_ad', )

    def get_success_url(self):
        return reverse_lazy('bbs:detail', kwargs={'pk': self.kwargs['pk']})

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Ad.objects.get(pk=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['caption'] = 'Edit Ad'
        return context


class AdDelete(PermissionRequiredMixin, DeleteView):
    template_name = 'bbs/delete.html'
    queryset = Ad.objects.all()
    success_url = reverse_lazy('bbs:main')
    permission_required = ('bbs.delete_ad', )
