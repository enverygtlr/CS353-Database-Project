from flask import redirect, request


def redirect_last(default='/'):
    if request.referrer is None:
        return redirect(default)
    return redirect(request.referrer)