from .models import CustomUser


def auth_user_context(request):
    """
    این تابع کاربر لاگین‌شده (بر اساس session) رو به context همه‌ی
    تمپلیت‌ها اضافه می‌کنه، تا تو base.html بتونیم بدون نیاز به اینکه
    هر ویو دستی context بفرسته، وضعیت لاگین/نام/عکس کاربر رو نشون بدیم.
    """
    user_id = request.session.get('user_id')
    auth_user = None
    if user_id:
        auth_user = CustomUser.objects.filter(id=user_id).first()
    return {'auth_user': auth_user}