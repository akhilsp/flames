
from django.shortcuts import redirect
from .models import User
from django.contrib.sessions.models import Session
# All custom decorators are written here.


# Decorator for user login check
def user_login_required(f):
    def usrgo(request, *args, **kwargs):
        if 'sessionid' not in request.COOKIES:
            return redirect('/home')
        else:
            s_id = request.COOKIES['sessionid']
            s = Session.objects.get(pk=s_id)
            d = s.get_decoded()
            if 'id' in d:
                c_user = User.objects.get(pk=d['id'])
                if c_user.role == 'CO':
                    return f(request, *args, **kwargs)
                else:
                    return redirect('/home')
            else:
                return redirect('/home')
    usrgo.__doc__ = f.__doc__
    usrgo.__name__ = f.__name__
    return usrgo


# Decorator for admin login check
def admin_login_required(f):
    def adgo(request, *args, **kwargs):
        if 'sessionid' not in request.COOKIES:
            return redirect('/home')
        else:
            s_id = request.COOKIES['sessionid']
            s = Session.objects.get(pk=s_id)
            d = s.get_decoded()
            if 'id' in d:
                c_user = User.objects.get(pk=d['id'])
                if c_user.role == 'AD':
                    return f(request, *args, **kwargs)
                else:
                    return redirect('/home')
            else:
                return redirect('/home')
    adgo.__doc__ = f.__doc__
    adgo.__name__ = f.__name__
    return adgo
