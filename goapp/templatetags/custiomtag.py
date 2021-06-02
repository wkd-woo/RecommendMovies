from django import template
register = template.Library()

# 템플릿에서 list[index]을 사용자 커스텀으로 값을 가져올 수 있도록함
@register.filter
def index(indexable, i):
    return indexable[i]