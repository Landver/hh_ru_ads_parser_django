import graphene

import ads.schema


class Query(ads.schema.Query, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)