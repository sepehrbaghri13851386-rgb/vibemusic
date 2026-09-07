from loginsogin_app.models import CustomUser


def user_context(request):
    user_id = request.session.get('user_id')
    auth_user = CustomUser.objects.filter(id=user_id).first() if user_id else None
    return {'auth_user': auth_user}
