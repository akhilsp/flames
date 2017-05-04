from .forms import RegisterUserForm, EmailForm, NewpasswordForm
from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.template import RequestContext
from operator import itemgetter
from .decorators import *
from django.utils.decorators import method_decorator


E_mail = ''
CRITICAL = 50


def error(request):
    messages.add_message(request, CRITICAL, 'Please enter proper information.')


def login(request):
    try:
        user = authenticate(username=request.POST.get('email'), password=request.POST.get('password'))
        if user and user.role == 0:
            request.session['userid'] = user.consumer_id
            request.session['name'] = user.first_name
            request.session['id'] = user.id
            request.session.set_expiry(3000)
            return redirect('/users/home')
        elif user and user.role == 1:
            request.session['userid'] = user.username
            request.session['name'] = user.first_name
            request.session['id'] = user.id
            request.session.set_expiry(3000)
            return redirect('/admin1/home')
        else:
            return redirect("/home", messages.error(request, "The email and password you entered doesn't match."))
    except Exception as e:
        print(e)
        return redirect("/home", messages.error(request, "Can't log you in right now. Please try after some time"))


class RegPage(View):

    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = User()
            user.username = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.phone_no = form.cleaned_data['phone_no']
            user.aadhar_no = form.cleaned_data["aadhar_no"]
            user.set_password(form.cleaned_data['password'])
            user.address = form.cleaned_data['address']
            user.locality = form.cleaned_data['locality']
            user.district = form.cleaned_data['district']
            user.state = form.cleaned_data['state']
            user.pincode = form.cleaned_data['pincode']

            if not user.save():
                print("user saved")
                user.consumer_id = 'CO' + str(user.id + 100000)
                user.save()
                return redirect("/home", messages.success(request, 'Registered successfully!'))
            else:
                return redirect("/register", messages.error(request, 'Registration Failed'))

        else:
            return redirect("/register", error(request))


class HomePage(View):

    @staticmethod
    def get(request):
        if 'sessionid' in request.COOKIES:
            session_id = request.COOKIES['sessionid']
            s = Session.objects.get(pk=session_id)
            d = s.get_decoded()
            if 'id' in d:
                u = User.objects.get(pk=d['id'])
                if u.role == 1:
                    return redirect('admin1/home')
                elif u.role == 0:
                    return redirect('users/home')
            else:
                return render(request, 'login.html')
        else:
            return render(request, 'login.html')

    @staticmethod
    def post(request):
        try:
            user = authenticate(username=request.POST.get('email'), password=request.POST.get('password'))
            if user and user.role == 0:
                request.session['userid'] = user.consumer_id
                request.session['name'] = user.first_name
                request.session['id'] = user.id
                request.session.set_expiry(3000)
                return redirect('/users/home')
            elif user and user.role == 1:
                request.session['userid'] = user.username
                request.session['name'] = user.first_name
                request.session['id'] = user.id
                request.session.set_expiry(3000)
                return redirect('/admin1/home')
            else:
                return redirect("/home", messages.error(request, "The email and password you entered doesn't match."))
        except Exception as e:
            print(e)
            return redirect("/home", messages.error(request, "Can't log you in right now. Please try after some time"))


@method_decorator(user_login_required, name='get')
class UserPage(View):
    def get(self, request):
        if request.method == 'GET':
            return render(request, 'user_home.html')


def logout(request):
    try:
        del request.session['id']
        flag = 0
        return redirect('/home', messages.success(request, 'You have successfully logged out.'))

    except KeyError:
        return HttpResponse("Error. No user found.")


class ForgotPassword(View):
    def get(self, request):
        return render(request, 'enter_email.html')

    def post(self, request):
        global E_mail
        form = EmailForm(request.POST)
        E_mail = form.data["email"]
        user = User.objects.get(email=E_mail)
        if user is not None:
            send_mail(
                'Bharatgas Password Reset',
                'Hi',
                'vjithin34@gmail.com',
                [E_mail],
                html_message='<p>'
                             'Please use the link to reset your password :'
                             '<a href="http://127.0.0.1:8000/password/changing">Reset your password.</a><br>'
                             'If you did not request this password change please feel free to ignore it.</p>',
                )
            messages.success(request, 'A Verification link is sent to your Email Address')
            return redirect('/email')
        else:
            messages.warning(request, 'We could not find an account with this email address')
            return redirect('/email')


class PasswordChange(ForgotPassword):

    def get(self, request):
        return render(request, 'password_changing.html')

    def post(self, request):
        global E_mail
        user1 = User.objects.get(email=E_mail)
        form = NewpasswordForm(request.POST)
        user1.set_password(form.data['password'])
        try:
            user1.save()
            messages.success(request, 'PASSWORD SUCCESSFULLY CHANGED')
            return redirect('/home')

        except:
            messages.success(request, 'PASSWORD CHANGING FAILED')
            return redirect('/password/changing')


@method_decorator(admin_login_required, name='get')
class AdminPage(View):
    def get(self, request):
        if request.method == 'GET':
            return render(request, 'admin1_home.html')


@method_decorator(admin_login_required, name='get')
class Consumer(View):

    def get(self, request):
        consumers = User.objects.filter(role='CO', is_delete=False).order_by('first_name')
        return render(request, 'admin1_consumers.html', {'consumers': consumers})

    def post(self, request):
        m_id = request.POST['id']
        print(m_id)
        consumer = User.objects.get(pk=m_id)
        consumer.is_delete = True
        consumer.save()
        return redirect('/admin1/consumers', messages.success(request, 'user successfully deleted'))


@method_decorator(admin_login_required, name='get')
class Order(View):

    def get(self, request):
        context = RequestContext(request)
        consumers = User.objects.filter(role='CO', is_delete=False).order_by('first_name')
        order_consumer1 = []
        for consumer in consumers:
            orders = consumer.rel_name.all().order_by('request_date')
            for order in orders:
                order = {
                    'order_id': order.id, 'type': order.type, 'date': order.request_date, 'consumer': consumer.email, 'consumer_no': consumer.consumer_id, 'status': order.status,
                }
                order_consumer1.append(order)
        order_consumer2 = sorted(order_consumer1, key=itemgetter('order_id'))
        order_consumer = sorted(order_consumer2, key=itemgetter('status'))
        print(order_consumer)
        return render(request, 'admin1_requests.html', {'order_consumer': order_consumer}, context)

    def post(self, request):
        orders = UserRequests.objects.all().order_by('request_date')
        n_id = orders.user_id
        return redirect('admin1/requests')
        rqt_id = request.POST['id']
        print(rqt_id)
        usr_ord = UserRequests.objects.get(pk=rqt_id)
        usr_ord.status = request.POST['status_update']
        usr_ord.expected_date = request.POST['expected_date']
        usr_ord.save()
        return redirect('/admin1/requests')


@method_decorator(user_login_required, name='get')
class Refil(View):

    def get(self, request):
        if request.method == 'GET':
            session_id = request.COOKIES['sessionid']
            s = Session.objects.get(pk=session_id)
            print(s.get_decoded())
            uid = s.get_decoded()
            try:
                requests = UserRequests.objects.filter(user_id=uid['id'])
                return render(request, 'refil.html', {'requests': requests})
            except:
                return redirect("/home", messages.success(request, 'Please login'))

    def post(self, request):
        if request.method == 'POST':
            session_id = request.COOKIES['sessionid']
            s = Session.objects.get(pk=session_id)
            print(s.get_decoded())
            uid = s.get_decoded()
            print("refil ok")
            try:
                u = UserRequests()
                u.type = 'RFL'
                u.user = User.objects.get(pk=uid['id'])
                u.save()
                requests = UserRequests.objects.filter(user_id=uid['id'])
                return render(request, 'refil_success.html', {'requests': requests}, messages.success(request, 'You have booked successfully'))
            except:
                return redirect("/home", messages.success(request, 'Please login'))



def Refil_new(request):
    return HttpResponse("refil.")

@method_decorator(user_login_required, name='get')
def refil_new(request):
        return HttpResponse("refil.")



