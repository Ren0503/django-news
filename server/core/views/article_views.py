from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from core.models import Category, Tag, Article, Comment
from core.serializers import ArticleSerializer, ArticleDetailSerializer

from rest_framework import status

# ----------------------------
# Guest
# ----------------------------


@api_view(['GET'])
def getArticles(request):
    query = request.query_params.get('keyword')
    if query == None:
        query = ''

    articles = Article.objects.filter(
        name__icontains=query).order_by('-createdAt')

    page = request.query_params.get('page')
    paginator = Paginator(articles, 15)

    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)
    serializer = ArticleSerializer(articles, many=True)
    return Response({'articles': serializer.data, 'page': page, 'pages': paginator.num_pages})


@api_view(['GET'])
def getTopArticles(request):
    articles = Article.objects.all().order_by('-views')[0:5]
    serializer = ArticleSerializer(articles, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getCategoryArticles(request, category):
    articles = Article.objects.filter()

@api_view(['GET'])
def getArticle(request, pk):
    try:
        article = Article.objects.get(_id=pk)
        article.views += 1
        article.save()

        serializer = ArticleDetailSerializer(article, many=False)
        return Response(serializer.data)
    except Exception as e:
        return Response({'details': f"{e}"}, status=status.HTTP_204_NO_CONTENT)

# ----------------------------
# User
# ----------------------------

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createArticleReview(request, pk):
    user = request.user
    article = Article.objects.get(_id=pk)

