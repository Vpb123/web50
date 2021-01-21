from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import Form
from django.utils import timezone
from .models import *



def index(request):
    data=Listing.objects.filter(ended=False)
    return render(request, "auctions/index.html",{
        'listExist':True if len(data)!=0 else False,
        'list':data,
        'title':'Active Listings'
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create(request) :
    if request.method == "POST":
        form=Form(request.POST)
        if form.is_valid:
            listing=form.save(commit=False)
            listing.user=request.user
            listing.addedTime=timezone.now()
            listing.save()
            return HttpResponseRedirect(reverse('index'))
        return HttpResponseRedirect(reverse('create'))
    else:
        form=Form()
        return render(request,'auctions/create.html',{'form':form})



def watchlist(request):
    list = Watchlist.objects.filter(user=request.user)
    data = []
    for i in range(len(list)):
        data.append(Listing.objects.get(title=list[i].listing))
    return render(request, "auctions/index.html",{
        'listExist':True if len(data)!=0 else False,
        'list': data,
        'title':"Watchlist"
    })
    
def comment(request, title):
     listing=Listing.objects.get(title=title)
     user=User.objects.filter(username=request.user)[0]
     entry=request.POST["comment"]
     data=Comment(user=user,listing=listing,entry=entry)
     data.save()
     return HttpResponseRedirect(reverse('index'))


def watchlistAdd(request, title):
    listing = Listing.objects.get(title=title)
    user = User.objects.filter(username=request.user)[0]
    data = Watchlist(user=user,listing=listing)
    data.save()
    return HttpResponseRedirect(reverse("watchlist"))

def watchlistRem(request,title):
     listing=Listing.objects.get(title=title)
     user=User.objects.filter(username=request.user)[0]
     Watchlist.objects.filter(listing=listing,user=user).delete()
     return  HttpResponseRedirect(reverse('watchlist'))

def bid(request,title):
    listing=Listing.objects.get(title=title,ended=False)
    amount=request.POST['bid']
    if float(listing.price)<float(amount):
        listing.price=amount
        listing.winner=request.user
        listing.save()
        bid=Bid(value=amount,listing=listing,user=request.user)
        bid.save()
        return render(request,'auctions/bid.html',{
            'title':title,
             'bid':amount
        })
    else:
        return render(request,'auctions/error.html',{
            'message':"Your bid is less than current price"
        })

def listing(request, title):
    data=Listing.objects.get(title=title)
    comments=Comment.objects.filter(listing=data.id)
    try:
        watching, own, win = False, False, False
        for item in Watchlist.objects.filter(user=request.user):
            if item.listing.title==title:
                watching=True
        if request.user==data.user:
                own=True
        if request.user==data.winner and data.ended:
                win=True
        return render(request,"auctions/listing.html",{
                "item":data,
                "comments":comments,
                "watching":watching,
                "own":own,
                "win":win,
                "anon":False
            })
    except:
        return render(request,"auctions/listing.html",{
            "item":data,
            "comments":comments,
            "anon":True
        })

def category(request,category):
    data=Listing.objects.filter(ended=False,category=category)
    return render(request,'auctions/index.html',{
        'listExist':True if len(data)!=0 else False,
        'list':data,
        'title':category.replace("_"," ")
    })

def menu(request):
    return render(request,'auctions/menu.html')
    
def ended(request, title):
    listing = Listing.objects.get(title=title)
    listing.ended = True
    listing.save()
    return HttpResponseRedirect(reverse("index"))