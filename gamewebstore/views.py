from django.shortcuts import render, redirect
from .forms import UserDataForm, GameInfoForm, CompanyInfoForm, CompanyDeleteForm, NewCategoryForm
from django.contrib.auth.models import User
from django.db.models import Count, Sum, Case, When, Value, IntegerField
from django.db import IntegrityError
from django.db import transaction as DjangoTransaction
from django.conf import settings
from .models import *
from django.utils import timezone
from django.http import JsonResponse
import random
import re
from hashlib import md5


def is_logged_in_as_dev(user):
    return hasattr(user, 'profile') and user.profile.role == 'D'


def get_game_ids_with_access(user):
    if not user.is_authenticated():
        return set()

    user_companies = [i.id for i in user.companies.all()]
    return set([i.game.id for i in user.owned_games.filter(game__active=True)] +
               [i.id for i in OnlineGame.objects.filter(active=True, company__id__in=user_companies)])


def make_transaction_checksum(pid, amount):
    return md5("pid={}&sid={}&amount={}&token={}".format(
        pid,
        getattr(settings, "SIMPLE_PAYMENTS_ID", ""),
        amount,
        getattr(settings, "SIMPLE_PAYMENTS_KEY", "")
    ).encode('ascii')).hexdigest()


def make_transaction_confirm_checksum(pid, ref, result):
    return md5("pid={}&ref={}&result={}&token={}".format(
        pid,
        ref,
        result,
        getattr(settings, "SIMPLE_PAYMENTS_KEY", "")
    ).encode('ascii')).hexdigest()


def prepare_uuid_for_payment_processor(pid):
    return pid.hex


def prepare_uuid_from_payment_processor(pid):
    return uuid.UUID(pid)


def about(request):
    return render(request, "about.html", {})


def home(request):
    if is_logged_in_as_dev(request.user):
        return redirect("developerHome")
    else:
        return redirect("marketplaceHome")


def userDataCollection(request):
    form = UserDataForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        #form.save()
        instance = form.save(commit=False)
        instance.user = request.user
        name = form.cleaned_data.get("name")
        if not name:
            name = "New full name"
        instance.name = name

        instance.save()
        return render(request, "home.html")

    return render(request, "user_data_collection.html", context)


def developerHome(request):
    context = {}

    if not request.user.is_authenticated():
        return redirect("auth_login")

    if not is_logged_in_as_dev(request.user):
        return render(request, "403.html")

    context["companies"] = request.user.companies.all()

    return render(request, "developer/home.html", context)


def developerCompany(request, dev_id):
    context = {}

    if not request.user.is_authenticated():
        return redirect("auth_login")

    if not is_logged_in_as_dev(request.user):
        return render(request, "403.html")

    if not request.user.companies.filter(id=dev_id).exists():
        return render(request, "403.html")

    context["company"] = Company.objects.get(id=dev_id)

    return render(request, "developer/company.html", context)


def developerGame(request, dev_id, game_id):
    context = {}

    if not request.user.is_authenticated():
        return redirect("auth_login")

    if not is_logged_in_as_dev(request.user):
        return render(request, "403.html")

    if not request.user.companies.filter(id=dev_id).exists():
        return render(request, "403.html")

    context["company"] = Company.objects.get(id=dev_id)

    if not context["company"].games.filter(id=game_id).exists():
        return render(request, "404.html")

    context["game"] = OnlineGame.objects.get(id=game_id)
    context["ownerships"] = UserGameOwnership.objects.filter(game=game_id).order_by('-purchase_date')
    context["showing_all"] = request.GET.get('allowners', '0') == '1'

    if not context["showing_all"]:
        context["ownerships"] = context["ownerships"][:10]

    return render(request, "developer/game.html", context)


def developerCompanyAdd(request):
    context = {}

    if not request.user.is_authenticated():
        return redirect("auth_login")

    if not is_logged_in_as_dev(request.user):
        return render(request, "403.html")

    form = CompanyInfoForm(request.POST or None)
    if form.is_valid():
        print(request.POST)
        instance = form.save()
        instance.user.add(request.user)
        instance.save()

        return redirect("developerHome")

    context["form"] = form

    return render(request, "developer/dev_edit.html", context)


def developerCompanyDelete(request, dev_id):
    context = {}

    if not request.user.is_authenticated():
        return redirect("auth_login")

    if not is_logged_in_as_dev(request.user):
        return render(request, "403.html")

    if not request.user.companies.filter(id=dev_id).exists():
        return render(request, "403.html")

    company = Company.objects.get(id=dev_id)

    if request.method == 'POST':
        if request.POST["selection"] == 'no':
            return redirect("developerCompany", dev_id=dev_id)
        elif request.POST["selection"] == 'yes':
            company.user.clear()
            return redirect("developerHome")
        elif request.POST["selection"] == 'yes_and_deactivate':
            company.user.clear()
            for game in company.games.all():
                game.active = False
                game.save()
            company.save()
            return redirect("developerHome")

    context["company"] = company
    context["form"] = CompanyDeleteForm

    return render(request, "developer/dev_delete.html", context)


def developerGameAdd(request, dev_id):
    context = {
        "isNewGame": True,
    }

    if not request.user.is_authenticated():
        return redirect("auth_login")

    if not is_logged_in_as_dev(request.user):
        return render(request, "403.html")

    if not request.user.companies.filter(id=dev_id).exists():
        return render(request, "403.html")

    context["company"] = Company.objects.get(id=dev_id)
    context["game"] = {}

    form = GameInfoForm(request.POST or None)

    if form.is_valid():
        print(request.POST)
        instance = form.save(commit=False)
        instance.company = context["company"]
        instance.save()

        # save category references, they aren't otherwise saved automatically with commit=false
        form.save_m2m()
        return redirect("developerGameEdit", dev_id=dev_id, game_id=instance.id)
    context["form"] = form

    return render(request, "developer/game_edit.html", context)


def developerGameEdit(request, dev_id, game_id):
    context = {
        "isNewGame": False
    }

    if not request.user.is_authenticated():
        return redirect("auth_login")

    if not is_logged_in_as_dev(request.user):
        return render(request, "403.html")

    if not request.user.companies.filter(id=dev_id).exists():
        return render(request, "403.html")

    context["company"] = Company.objects.get(id=dev_id)

    if not context["company"].games.filter(id=game_id).exists():
        return render(request, "404.html")

    game = OnlineGame.objects.get(id=game_id)
    context["game"] = game

    if request.method == 'POST':
        form = GameInfoForm(request.POST, instance=game)
        if form.is_valid():
            form.save()
            return redirect("developerGame", game_id=game_id, dev_id=dev_id)
    else:
        form = GameInfoForm(instance=game)

    context["form"] = form

    return render(request, "developer/game_edit.html", context)


def developerGameToggleActive(request, dev_id, game_id):
    context = {}

    if not request.user.is_authenticated():
        return redirect("auth_login")

    if not is_logged_in_as_dev(request.user):
        return render(request, "403.html")

    if not request.user.companies.filter(id=dev_id).exists():
        return render(request, "403.html")

    context["company"] = Company.objects.get(id=dev_id)

    if not context["company"].games.filter(id=game_id).exists():
        return render(request, "404.html")

    game = OnlineGame.objects.get(id=game_id)
    game.active = not game.active
    game.save()

    return redirect("developerGame", dev_id=dev_id, game_id=game_id)

def developerCategoryAdd(request, dev_id):
    context = {}

    if not request.user.is_authenticated():
        return redirect("auth_login")

    if not is_logged_in_as_dev(request.user):
        return render(request, "403.html")

    form = NewCategoryForm(request.POST or None)
    if form.is_valid():
        print(request.POST)
        instance = form.save()
        #instance.user.add(request.user)
        instance.save()

        return redirect("developerGameAdd", dev_id = dev_id)

    context["form"] = form

    return render(request, "developer/add_category.html", context)

def marketplaceHome(request):
    context = {}

    context["categories"] = Category.objects.annotate(
        active_games_count=Sum(
            Case(
                When(games__active=True, then=1),
                output_field=IntegerField()
            ),
            default=Value(0, output_field=IntegerField())
        )
    )

    games = OnlineGame.objects.filter(active=True).annotate(num_owners=Count('owners')).order_by('-num_owners')
    if games.count() > 0:
        context["random_picks"] = random.sample(list(games), min(3, games.count()))
    else:
        context["random_picks"] = []
    context["popular_games"] = games[:3]
    context["owned_games"] = get_game_ids_with_access(request.user)

    return render(request, "marketplace/home.html", context)


def marketplaceCategoryListing(request, category_id):
    context = {}

    if not Category.objects.filter(id=category_id).exists():
        return redirect("home")

    context["category"] = Category.objects.get(id=category_id)
    context["owned_games"] = get_game_ids_with_access(request.user)

    return render(request, "marketplace/category.html", context)


def marketplaceGameEntry(request, game_id):
    context = {}

    if not OnlineGame.objects.filter(id=game_id, active=True).exists():
        return redirect("home")

    context["game"] = OnlineGame.objects.get(id=game_id)
    context["owned_games"] = get_game_ids_with_access(request.user)

    return render(request, "marketplace/game.html", context)


def marketplaceGamePurchase(request, game_id):
    context = {}

    if not OnlineGame.objects.filter(id=game_id, active=True).exists():
        return redirect("home")

    if not request.user.is_authenticated():
        return redirect("auth_login")

    owned_games = get_game_ids_with_access(request.user)
    game = OnlineGame.objects.get(id=game_id)
    context["game"] = game

    if int(game_id) in owned_games:
        return render(request, "marketplace/game_purchase_alreadyowned.html", context)

    # Clear any previous transactions for this user-game pair
    # This only happens if the user doesn't own the game (checked above)
    # so successful transactions should never be destroyed here
    Transaction.objects.filter(user=request.user, game=game).delete()

    transaction = Transaction(
        user=request.user,
        game=game,
        pending=True,
        amount=game.price,
        expires=timezone.now() + timezone.timedelta(hours=1)
    )
    try:
        transaction.full_clean()
    except:
        return render(request, "500.html")

    transaction.save()

    # Payment portal specifies that dashes are not allowed in the PID. That makes some preprocessing necessary,
    # as we're using UUIDs which are very useful here otherwise.
    pid = prepare_uuid_for_payment_processor(transaction.id)

    context["sid"] = getattr(settings, "SIMPLE_PAYMENTS_ID", None)
    context["pid"] = pid
    context["checksum"] = make_transaction_checksum(pid, game.price)

    return render(request, "marketplace/game_purchase.html", context)


def marketplaceGamePurchaseThankYou(request, game_id):
    context = {}

    if not OnlineGame.objects.filter(id=game_id, active=True).exists():
        return render(request, "403.html")

    if not request.user.is_authenticated():
        return render(request, "403.html")

    # This view can be accessed by a game owner even if the purchase was finished at a previous date.
    # That is a minor issue that doesn't really hurt that much so we're leaving it in due to lack of time.

    owned_games = get_game_ids_with_access(request.user)
    game = OnlineGame.objects.get(id=game_id)
    context["game"] = game

    if int(game_id) not in owned_games:
        print(owned_games)
        return render(request, "403.html")

    return render(request, "marketplace/game_purchase_thankyou.html", context)


def marketplaceCompanyGamesListing(request, dev_id):
    context = {}

    if not Company.objects.filter(id=dev_id).exists():
        return redirect("home")

    context["company"] = Company.objects.get(id=dev_id)
    context["owned_games"] = get_game_ids_with_access(request.user)

    return render(request, "marketplace/dev_games.html", context)


def libraryHome(request):
    context = {}

    if not request.user.is_authenticated():
        return redirect("auth_login")

    context["purchased_games"] = request.user.owned_games.filter(game__active=True)

    return render(request, "library/home.html", context)


def transactionsConfirm(request):
    context = {}

    if not request.user.is_authenticated():
        return render(request, "403.html")

    pid = request.GET.get("pid", None)
    ref = request.GET.get("ref", None)
    result = request.GET.get("result", None)
    checksum = request.GET.get("checksum", None)

    if pid is None or ref is None or result is None or checksum is None:
        return render(request, "403.html")

    try:
        uuid = prepare_uuid_from_payment_processor(pid)
    except:
        # ID was invalid, probably faked
        return render(request, "403.html")

    if not Transaction.objects.filter(id=uuid, expires__gt=timezone.now(), pending=True).exists():
        return render(request, "403.html")

    transaction = Transaction.objects.get(id=uuid)

    if not transaction.user == request.user:
        return render(request, "403.html")

    if not make_transaction_confirm_checksum(pid, ref, result) == checksum:
        return render(request, "403.html")

    try:
        with DjangoTransaction.atomic():
            transaction.pending = False
            transaction.expires = None
            transaction.save()

            ownership = UserGameOwnership(user=request.user, game=transaction.game)
            ownership.save()

            scoredata = OnlineGameScore(user=request.user, game=transaction.game)
            scoredata.save()
    except IntegrityError as e:
        return render(request, "500.html")

    # We could render the view here directly, but a nicer URL is preferred instead.
    return redirect("marketplaceGamePurchaseThankYou", game_id=transaction.game.id)


def transactionsCancel(request):
    context = {}

    if not request.user.is_authenticated():
        return render(request, "403.html")

    pid = request.GET.get("pid", None)
    ref = request.GET.get("ref", None)
    result = request.GET.get("result", None)
    checksum = request.GET.get("checksum", None)

    if pid is None or ref is None or result is None or checksum is None:
        return render(request, "403.html")

    try:
        uuid = prepare_uuid_from_payment_processor(pid)
    except:
        # ID was invalid, probably faked
        return render(request, "403.html")

    if not Transaction.objects.filter(id=uuid, expires__gt=timezone.now(), pending=True).exists():
        return render(request, "403.html")

    transaction = Transaction.objects.get(id=uuid)

    if not transaction.user == request.user:
        return render(request, "403.html")

    if not make_transaction_confirm_checksum(pid, ref, result) == checksum:
        return render(request, "403.html")

    game_id = transaction.game.id
    transaction.delete()

    return redirect("marketplaceGameEntry", game_id=game_id)


def transactionsError(request):
    context = {}

    if not request.user.is_authenticated():
        return render(request, "403.html")

    pid = request.GET.get("pid", None)
    ref = request.GET.get("ref", None)
    result = request.GET.get("result", None)
    checksum = request.GET.get("checksum", None)

    if pid is None or ref is None or result is None or checksum is None:
        return render(request, "403.html")

    try:
        uuid = prepare_uuid_from_payment_processor(pid)
    except:
        # ID was invalid, probably faked
        return render(request, "403.html")

    if not Transaction.objects.filter(id=uuid, expires__gt=timezone.now(), pending=True).exists():
        return render(request, "403.html")

    transaction = Transaction.objects.get(id=uuid)

    if not transaction.user == request.user:
        return render(request, "403.html")

    if not make_transaction_confirm_checksum(pid, ref, result) == checksum:
        return render(request, "403.html")

    context["game"] = transaction.game
    transaction.delete()

    return render(request, "marketplace/game_purchase_error.html", context)


def playGame(request, game_id):
    context = {}
    if not OnlineGame.objects.filter(id=game_id, active=True).exists():
        return redirect("home")

    if not request.user.is_authenticated():
        return redirect("auth_login")

    owned_games = get_game_ids_with_access(request.user)

    if not int(game_id) in owned_games:
        return render(request, "403.html", context)

    game = OnlineGame.objects.get(id=game_id)
    context["scores"] = game.scores.all().order_by('-score')
    context["game"] = game
    return render(request, "player/game.html", context)


def playApiLoadSavedData(request, game_id):
    if not (request.method == "POST" and
            OnlineGame.objects.filter(id=game_id, active=True).exists() and
            request.user.is_authenticated()):
        return JsonResponse({'error': 'unauthorized'}, status=403)

    owned_games = get_game_ids_with_access(request.user)

    if not int(game_id) in owned_games:
        return JsonResponse({'error': 'unauthorized'}, status=403)

    try:
        state = OnlineGameSaveState.objects.get(user=request.user, game_id=game_id)
        return JsonResponse({'data': str(state.data, encoding="UTF-8")}, status=200)
    except OnlineGameSaveState.DoesNotExist:
        return JsonResponse({'error': 'no save data present'}, status=404)


def playApiSaveData(request, game_id):
    if not (request.method == "POST" and
            OnlineGame.objects.filter(id=game_id, active=True).exists() and
            request.user.is_authenticated()):
        return JsonResponse({'error': 'unauthorized'}, status=403)

    owned_games = get_game_ids_with_access(request.user)

    if not int(game_id) in owned_games:
        return JsonResponse({'error': 'unauthorized'}, status=403)

    data = request.POST.get("data", None)
    if data is None:
        return JsonResponse({'error': 'invalid request'}, status=400)

    try:
        state = OnlineGameSaveState.objects.get(user=request.user, game_id=game_id)
        state.data = bytes(data, encoding="UTF-8")
        state.save()

        return JsonResponse({'data': 'success'}, status=200)
    except OnlineGameSaveState.DoesNotExist:
        try:
            state = OnlineGameSaveState(user=request.user, game_id=game_id, data=bytes(data, encoding="UTF-8"))
            state.save()
            return JsonResponse({'data': 'success'}, status=200)
        except:
            return JsonResponse({'error': 'server error'}, status=500)
    except:
        return JsonResponse({'error': 'server error'}, status=500)


def playApiSaveScore(request, game_id):
    if not (request.method == "POST" and
                OnlineGame.objects.filter(id=game_id, active=True).exists() and
                request.user.is_authenticated()):
        return JsonResponse({'error': 'unauthorized'}, status=403)

    owned_games = get_game_ids_with_access(request.user)

    if not int(game_id) in owned_games:
        return JsonResponse({'error': 'unauthorized'}, status=403)

    score = request.POST.get("score", None)
    if score is None:
        return JsonResponse({'error': 'invalid request'}, status=400)

    try:
        state = OnlineGameScore.objects.get(user=request.user, game_id=game_id)
        state.score = max(state.score, float(score))
        state.save()

        return JsonResponse({'data': 'success'}, status=200)
    except OnlineGameScore.DoesNotExist:
        try:
            state = OnlineGameScore(user=request.user, game_id=game_id, score=score)
            state.save()

            return JsonResponse({'data': 'success'}, status=200)
        except:
            return JsonResponse({'error': 'server error'}, status=500)
    except:
        return JsonResponse({'error': 'server error'}, status=500)
