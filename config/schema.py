from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from graphene_django.debug import DjangoDebug
import graphene
from boards.schema import CreateAskArticle, CreateFreeArticle, CreateFreeArticleComment, EditFreeArticle, FreeArticleQuery, NoticeArticleQuery
from services.models import RelatedCompanyPartner
from services.schema import CreateDevelopmentRequest, CreatePartnerRequest, DevelopmentQuery, LanderPartnerQuery, RelatedCompanyPartnerQuery

UserModel = get_user_model()


class Query(RelatedCompanyPartnerQuery, FreeArticleQuery, NoticeArticleQuery, LanderPartnerQuery, DevelopmentQuery, graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name="_debug")


class Mutations(graphene.ObjectType):
    create_development_request = CreateDevelopmentRequest.Field()
    create_partner_request = CreatePartnerRequest.Field()
    create_free_article = CreateFreeArticle.Field()
    create_free_article_comment = CreateFreeArticleComment.Field()
    edit_free_article = EditFreeArticle.Field()
    create_ask_article = CreateAskArticle.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)
