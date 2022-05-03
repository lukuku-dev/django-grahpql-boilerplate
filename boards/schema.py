import graphene
from graphene import Field

from .models import AskArticle, NoticeArticle, FreeArticle, FreeArticleComment
from graphene_django import DjangoObjectType

from graphene_django_pagination import DjangoPaginationConnectionField
from pydash import py_


class NoticeArticleType(DjangoObjectType):
    class Meta:
        model = NoticeArticle
        filter_fields = {"id": ["icontains"]}


class NoticeArticleQuery(object):
    all_notice_article = DjangoPaginationConnectionField(NoticeArticleType)
    notice_article_by_id = graphene.Field(
        NoticeArticleType, id=graphene.String(required=True))

    def resolve_all_notice_article(self, info, **kwargs):
        return NoticeArticle.objects.filter(is_active=True)

    def resolve_notice_article_by_id(self, info, id, **kwargs):
        try:
            notice_article = NoticeArticle.objects.get(id=id, is_active=True)
            notice_article.view_count += 1
            notice_article.save()
            return notice_article
        except NoticeArticle.DoesNotExist:
            return None


class FreeArticleCommentType(DjangoObjectType):
    class Meta:
        exclude = ['password']
        model = FreeArticleComment


class FreeArticleType(DjangoObjectType):
    all_comment = Field(FreeArticleCommentType)

    class Meta:
        model = FreeArticle
        filter_fields = {"id": ["icontains"]}

    def resolve_all_comment(self, info):
        return self.freearticlecomment_set.filter(is_active=True)


class FreeArticleQuery(object):
    all_free_article = DjangoPaginationConnectionField(FreeArticleType)
    free_article_by_id = graphene.Field(
        FreeArticleType, id=graphene.String(required=True))

    def resolve_all_free_article(self, info, **kwargs):
        return FreeArticle.objects.filter(is_active=True)

    def resolve_free_article_by_id(self, info, id, **kwargs):
        try:
            article = FreeArticle.objects.get(id=id, is_active=True)
            article.view_count += 1
            article.save()
            return article
        except FreeArticle.DoesNotExist:
            return None


class CreateFreeArticle(graphene.Mutation):
    class Arguments:
        writer = graphene.String(required=True)
        title = graphene.String(required=True)
        content = graphene.String(required=True)
        password = graphene.String(required=True)

    ok = graphene.Boolean()
    id = graphene.ID()

    def mutate(root, info, **kwargs):
        free_article = FreeArticle.objects.create(**kwargs)
        return CreateFreeArticle(ok=True, id=free_article.id)


class CreateAskArticle(graphene.Mutation):
    class Arguments:
        company_name = graphene.String(required=True)
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        content = graphene.String(required=True)

    ok = graphene.Boolean()
    id = graphene.ID()

    def mutate(root, info, **kwargs):
        ask_article = AskArticle.objects.create(**kwargs)
        return CreateFreeArticle(ok=True, id=ask_article.id)


class CreateFreeArticleComment(graphene.Mutation):
    class Arguments:
        free_article = graphene.Int(required=True)
        free_article_comment = graphene.Int()
        name = graphene.String(required=True)
        content = graphene.String(required=True)

    ok = graphene.Boolean()
    id = graphene.ID()

    def mutate(root, info, free_article, free_article_comment, **kwargs):
        free_article = FreeArticle.objects.get(id=free_article)
        free_article_comment = None
        if free_article_comment:
            free_article_comment = FreeArticleComment.objects.get(
                id=free_article_comment)

        free_article_comment = FreeArticleComment.objects.create(
            free_article=free_article, free_article_comment=free_article_comment, **kwargs)
        return CreateFreeArticleComment(ok=True, id=free_article_comment.id)


class EditFreeArticle(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        password = graphene.String(required=True)

        is_active = graphene.Boolean()
        writer = graphene.String()
        title = graphene.String()
        content = graphene.String()

    ok = graphene.Boolean()
    id = graphene.ID()

    def mutate(root, info, id, password, **kwargs):
        free_article = FreeArticle.objects.get(
            id=id, password=password, is_active=True)
        for k, v in kwargs.items():
            if v:
                setattr(free_article, k, v)
        free_article.save()
        return EditFreeArticle(ok=True, id=free_article.id)
