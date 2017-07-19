from django.contrib.auth import authenticate

def log(request):
    user = request.user
    if user.is_authenticated():
        ctx = {
            'log_note': 'Log out, {}'.format(user.username),
            'log_link': 'logout',
            'user': user
        }
    else:
        ctx = {
            'log_note': 'Log in, Stranger',
            'log_link': 'login',
            'user': user
        }
    return ctx


