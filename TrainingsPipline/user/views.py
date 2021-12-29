import django.contrib.auth.models
from django.shortcuts import render, redirect
from django.db.models import Q
from .form import AddReservation
from django.utils import timezone
from django.contrib import messages
from server.models import ServerReservation, ServerManagement
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from .client import *
from django.contrib.auth.decorators import login_required


# parentdir = Path(os.getcwd())
#
# sys.path.append("..")


# Create your views here.

def deletezip():
    for f in Path(os.path.join(parentdir, 'media')).glob('*.zip'):
        try:
            f.unlink()
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))


def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                messages.success(request, "Successfully Login with username: " + username)
                login(request, user)
                return redirect('dashboard')

            else:
                print("Someone tried to login and failed.")
                print("They used username: {} and password: {}".format(username, password))

                return redirect('/')
        except Exception as identifier:
            print(identifier)
            return redirect('/')

    else:
        return render(request, 'user/login/login.html')


def reservation(request):
    context = {}
    if request.POST.get('server'):
        request.session['server'] = request.POST.get('server')
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        context['form'] = AddReservation(request.POST)
        # check whether it's valid:
        if context['form'].is_valid():
            # process the data in form.cleaned_data as required
            # ...
            context['form'].save()
            # redirect to a new URL:
            del request.session['server']
            return redirect('dashboard')

    # if a GET (or any other method) we'll create a blank form
    else:
        context['form'] = AddReservation()
    return render(request, 'user/login/reservation.html', context)


def book_now(request):
    # if ServerReservation.objects.filter(Q(end_time__gte=timezone.now()),
    #                                     Q(reservation_time__lte=timezone.now())).filter(user_id=request.user.id).exists()
    #     del request.session['server']
    #     redirect('/')
    if "server" in request.POST:
        request.session['server'] = request.POST.get('server')
        server = ServerManagement.objects.get(id=request.POST.get('server'))
        print(server)
        user = django.contrib.auth.models.User.objects.get(id=request.user.id)

        # make a function which will add remaining time to book now before starting reservation time
        if ServerReservation.objects.filter(
                Q(reservation_time__gt=timezone.now()),
                Q(reservation_time__lt=timezone.now() + timezone.timedelta(hours=1))).filter(server_id=server).exists():
            reserved_time = ServerReservation.objects.filter(
                Q(reservation_time__gt=timezone.now()),
                Q(reservation_time__lt=timezone.now() + timezone.timedelta(hours=1))).filter(server_id=server)
            for var in reserved_time:
                time = var.reservation_time
                bnow_2 = ServerReservation.objects.create(server_id=server, user_id=user,
                                                          reservation_time=timezone.now() + timezone.timedelta(
                                                              seconds=5),
                                                          end_time=time)
                bnow_2.save()
                break
        else:

            bnow = ServerReservation.objects.create(server_id=server, user_id=user,
                                                    reservation_time=timezone.now() + timezone.timedelta(seconds=5),
                                                    end_time=timezone.now() + timezone.timedelta(hours=1))
            bnow.save()
    elif 'use-now' in request.POST:
        request.session['srever'] = request.POST.get('use-now')

    elif 'dataUpload' in request.POST:
        try:
            if os.listdir(os.path.join(parentdir, 'media')):
                deletezip()
            uploaded_file = request.FILES['file']
            augmentationfile = request.POST.get('augmentation')
        
            modelfile = request.POST.get('model')
            
            if augmentationfile is not None:
                zipfilename = modelfile+augmentationfile+uploaded_file.name
            elif augmentationfile is None:
                zipfilename = modelfile+uploaded_file.name
            fs = FileSystemStorage()
            fs.save(zipfilename, uploaded_file)
            server = request.POST.get('dataUpload')
            SendFile(server)
            return render(request, 'user/login/dashboard.html')
        except:
             messages.error(request, "Connection is not established or the file is not selected!")
    return render(request, 'user/login/booked.html')


@login_required(login_url="login")
def dashboard(request):
    return render(request, 'user/login/dashboard.html')


@login_required(login_url="login")
def available_server(request):
    servers = ServerManagement.objects.all()
    booked_server = ServerReservation.objects.filter(Q(end_time__gte=timezone.now()),
                                                     Q(reservation_time__lte=timezone.now()))
    # free_server = avail_server | booked_server
    setelement = set()
    for f in booked_server:
        if f.server_id in servers:
            setelement.add(f.server_id)
    dt = []
    for i in servers:
        dt += [
            {
                'servername': i.server_name,
                'ram': i.ram,
                'processor': i.processor,
                'available': i.enable,
                'status': (0 if i in setelement or not i.enable else 1),
                'server_id': i.id,
            }
        ]
    return render(request, 'user/login/available_server.html', {'ServerData': dt})


def logout_user(request):
    logout(request)
    return redirect('login')


def booked_server(request):
    reservations = ServerReservation.objects.filter(user_id=request.user.id)
    booked_server = ServerReservation.objects.filter(Q(end_time__gte=timezone.now()),
                                                     Q(reservation_time__lte=timezone.now())).filter(
        user_id=request.user.id)
    setelement = []
    for f in booked_server:
        setelement.append(f)
    dt = []
    for i in reservations:
        dt += [
            {
                'servername': i.server_id.server_name,
                'ram': i.server_id.ram,
                'processor': i.server_id.processor,
                'available': i.server_id.enable,
                'status': (1 if i in setelement and i.server_id.enable else 0),
                'server_id': i.server_id.id,
            }
        ]
    return render(request, 'user/login/reserved_servers.html', {'ServerData': dt})
