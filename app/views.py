from django.conf import settings
from django.shortcuts import redirect, render
from accounts.utils import send_activation_email
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required

from app.models import Catalogue, Label

# Create your views here.

@login_required(login_url='accounts:login', redirect_field_name='')
def index(request):
    if SocialAccount.objects.filter(user=request.user).exists():
        if not request.user.is_email_verified:
            send_activation_email(request, request.user)
    if not request.user.is_email_verified:
        return redirect('accounts:verify')
    return render(request, 'app/home.html')

def get_started(request):
    # check the last galaxy labeld by user
    if Label.objects.filter(labelled_by=request.user).exists():
        label = Label.objects.filter(labelled_by=request.user).last()
        galaxy = label.catalogue
        return redirect('app:galaxy', galaxy_name=galaxy.fcg)

    # get the first galaxy and redirect to it
    galaxy = Catalogue.objects.first()
    return redirect('app:galaxy', galaxy_name=galaxy.fcg)


def galaxy(request, galaxy_name):
    if request.method == 'GET':
        galaxy = Catalogue.objects.get(fcg=galaxy_name)

        # check if galaxy is labeled by user
        if Label.objects.filter(labelled_by=request.user, catalogue=galaxy).exists():
            is_labeled = True
            label = Label.objects.get(labelled_by=request.user, catalogue=galaxy)
            comment = label.comment if label.comment else None
            confidence_score = label.confidence_score if label.confidence_score else None
            label = label.label
        else:
            is_labeled = False
            label = None
            comment = None
            confidence_score = None

        try:
            galaxy_next = galaxy.get_next_by_timestamp()
        except:
            galaxy_next = galaxy

        try:
            galaxy_prev = galaxy.get_previous_by_timestamp()
        except:
            galaxy_prev = galaxy

        context = {
            'galaxy_name': galaxy.fcg,
            'galaxy_image': galaxy.fcg+'.png',
            'comments': galaxy.com,
            'next': True if galaxy_next.fcg != galaxy.fcg else False,
            'prev': True if galaxy_prev.fcg != galaxy.fcg else False,
            'is_labeled': is_labeled,
            'label': label,
            'comment': comment,
            'confidence_score': confidence_score,
        }

        return render(request, 'app/galaxy.html', context)

    if request.method == 'POST':
        label_text = request.POST['radio']
        galaxy = Catalogue.objects.get(fcg=galaxy_name)

        # check if galaxy is labeled by user
        if Label.objects.filter(labelled_by=request.user, catalogue=galaxy).exists():
            label = Label.objects.get(labelled_by=request.user, catalogue=galaxy)
            label.label = label_text
            label.comment = request.POST['comment']
            label.confidence_score = request.POST['confidence_score']
            label.save()
        else:
            label = Label(
                    label=label_text, 
                    confidence_score=request.POST['confidence_score'], 
                    comment=request.POST['comment'], 
                    labelled_by=request.user, 
                    catalogue=galaxy
                )
            label.save()

        return redirect('app:galaxy_next', galaxy_name=galaxy_name)

def galaxy_next(request, galaxy_name):
    if request.method == 'GET':
        galaxy = Catalogue.objects.get(fcg=galaxy_name)
        try:
            galaxy_next = galaxy.get_next_by_timestamp()
        except:
            galaxy_next = galaxy

        return redirect('app:galaxy', galaxy_name=galaxy_next.fcg)

def galaxy_prev(request, galaxy_name):
    if request.method == 'GET':
        galaxy = Catalogue.objects.get(fcg=galaxy_name)
        try:
            galaxy_prev = galaxy.get_previous_by_timestamp()
        except:
            galaxy_prev = galaxy

        return redirect('app:galaxy', galaxy_name=galaxy_prev.fcg)