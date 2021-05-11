import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import Ad


# Добавление возможности graphql запрашивать отфильтрованные данные
class AdNode(DjangoObjectType):
    class Meta:
        model = Ad
        filter_fields = {'title': ['exact', 'icontains', 'istartswith'],
                         'company_name': ['exact', 'icontains'],
                         'id': ['exact'],
                         }
        interfaces = (graphene.relay.Node, )


# Добавление возможности graphql запрашивать любые частичные данные данные
class AdType(DjangoObjectType):
    class Meta:
        model = Ad
        fields = ('id', 'title')
    say_hello = graphene.String(default_value='Hello bae')


# Реализация возможности получать наборы данных по желаемому запросу
class Query(graphene.ObjectType):
    ad = graphene.relay.Node.Field(AdNode)
    all_ads = DjangoFilterConnectionField(AdNode)

    ad_by_id = graphene.Field(AdType, id=graphene.String(required=True))

    # Метод добавляющий возможность graphql получить данные об объявлении по его id
    def resolve_ad_by_id(self, info, id):
        try:
            return Ad.objects.get(id=id)
        except Ad.DoesNotExist:
            return None
