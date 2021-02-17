from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from annoying.functions import get_object_or_None


from .models import *


def index(request):
    return render(request, "auctions/index.html")


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


@login_required(login_url='/login')
def listing(request):
    template_name = 'auctions/listings.html'
    products = Auction_listings.objects.all()
    empty = False
    if len(products) == 0:
        empty = True
    return render(request, template_name, {
        'products': products,
        'empty': empty
    })


@login_required(login_url='/login')
def new_listing(request):
    template_name = 'auctions/new_listing.html'
    if request.method == 'POST':
        listing = Auction_listings()
        listing.owner = request.user.username
        listing.product_name = request.POST.get('product_name')
        listing.description = request.POST.get('description')
        listing.category = request.POST.get('category')
        listing.first_bid = request.POST.get('first_bid')
        if request.POST.get('image'):
            listing.image = request.POST.get('image')
        else:
            listing.image = 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/No_image_available.svg/600px-No_image_available.svg.png'
        listing.save()
        return HttpResponseRedirect('listing')
    else:
        return render(request, template_name)


@login_required(login_url='/login')
def category(request, category):
    template_name = 'auctions/category.html'
    product_category = Auction_listings.objects.filter(category=category)
    empty = False
    if len(product_category) == 0:
        empty = True
    return render(request, template_name, {
        'category': category,
        'empty': empty,
        'products': product_category
    })


@login_required(login_url='/login')
def categories(request):
    template_name = 'auctions/categories.html'
    return render(request, template_name)


@login_required(login_url='/login')
def view_listing(request, product_id):
    template_name = 'auctions/view_listing.html'
    comments = Comment.objects.filter(auction_listing_id=product_id)
    if request.method == 'POST':
        item =  Auction_listings.objects.get(id=product_id)
        new_bid = int(request.POST.get('new_bid'))
        if item.first_bid >= new_bid:
            product = Auction_listings.objects.get(id=product_id)
            return render(request, template_name, {
                'product': product,
                'message': 'Your bid should be higher than the actual bid',
                'comments': comments
            })
        else:
            item.first_bid = new_bid
            item.save()
            bid = Bid.objects.filter(auction_listing_id=product_id)
            if bid:
                bid.delete()
            bidobcject = Bid()
            bidobcject.user = request.user.username
            bidobcject.title = item.product_name
            bidobcject.auction_listing_id = product_id
            bidobcject.bid = new_bid
            bidobcject.save()
            product = Auction_listings.objects.get(id=product_id)
            return render(request, template_name, {
                'product': product,
                'message': 'Bid added with success',
                'comments': comments
            })
    else:
        product = Auction_listings.objects.get(id=product_id)
        add = WatchList.objects.filter(auction_listing_id = product_id, user = request.user.username)
        return render(request, template_name, {
            'product': product,
            'add': add,
            'comments': comments
        })


@login_required(login_url='/login')
def watchlist(request, product_id):
    template_name = 'auctions/view_listing.html'
    item = WatchList.objects.filter(auction_listing_id=product_id, user=request.user.username)
    comments = Comment.objects.filter(auction_listing_id=product_id)
    if item:
        item.delete()
        product = Auction_listings.objects.get(id=product_id)
        add = WatchList.objects.filter(auction_listing_id=product_id, user=request.user.username)
        return render(request, template_name, {
            'product': product,
            'add': add,
            'comments': comments
        })
    else:
        item = WatchList()
        item.user = request.user.username
        item.auction_listing_id = product_id
        item.save()
        product = Auction_listings.objects.get(id=product_id)
        add = WatchList.objects.filter(auction_listing_id=product_id, user=request.user.username)
        return render(request, template_name, {
            'product': product,
            'add': add,
            'comments': comments
        }) 


@login_required(login_url='/login')
def addcomment(request, product_id):
    template_name = 'auctions/view_listing.html'
    if request.method == 'POST':
        item = Comment()
        item.comment = request.POST.get('comment')
        item.user = request.user.username
        item.auction_listing_id = product_id
        item.save()
        return HttpResponseRedirect(reverse('view_listing', args=[product_id]))


@login_required(login_url='/login')
def closebid(request, product_id):
    template_name = 'auctions/closelisting.html'
    winner_item = Auction_winner()
    listitem = Auction_listings.objects.get(id=product_id)
    item = get_object_or_None(Bid, auction_listing_id=product_id)
    if not item:
        message = 'Bid deleted without any winner'
    else:
        biditem = Bid.objects.get(auction_listing_id=product_id)
        winner_item.owner = request.user.username
        winner_item.winner = biditem.user
        winner_item.auction_listing_id = product_id
        winner_item.winnerPrice = biditem.bid
        winner_item.title = biditem.title
        winner_item.save()
        message = 'Bid closed'
        biditem.delete()
        return HttpResponseRedirect(reverse('closelisting'))
    if WatchList.objects.filter(auction_listing_id=product_id):
        watchitem = WatchList.objects.filter(auction_listing_id=product_id)
        watchitem.delete()
    if Comment.objects.filter(auction_listing_id=product_id):
        commentitem = Comment.objects.filter(auction_listing_id=product_id)
        commentitem.delete()
    listitem.delete()
    empty = False
    winners = Auction_winner.objects.all()
    if len(winners) == 0:
        empty = True
    return render(request, template_name, {
        'products': winners,
        'empty': empty,
        'message': message
    })


@login_required(login_url='/login')
def closelisting(request):
    template_name = 'auctions/closelisting.html'
    winners = Auction_winner.objects.all()
    empty = False
    if len(winners) == 0:
        empty = True
    return render(request, template_name, {
        'products': winners,
        'empty': empty
    })


@login_required(login_url='/login')
def info(request):
    template_name = 'auctions/info.html'
    winners = Auction_winner.objects.filter(winner=request.user.username)
    lst = WatchList.objects.filter(user=request.user.username)
    p = False
    product_list = []
    i = 0
    if lst:
        p = True
        for item in lst:
            product = Auction_listings.objects.get(id=item.auction_listing_id)
            product_list.append(product)
    print(product_list)
    return render(request, template_name, {
        'product_list': product_list,
        'p': p,
        'products': winners
    })