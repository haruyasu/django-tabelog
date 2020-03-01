from .models import Pref, Category


def common(request):
    """テンプレートに毎回渡すデータ"""
    context = {
        'pref_list': Pref.objects.all().order_by('pref'),
        'category_list': Category.objects.all().order_by('category_l'),
    }

    return context
