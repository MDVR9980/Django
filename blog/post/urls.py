from django.urls import path
from . import views

app_name = 'post'
urlpatterns = [
    # path('detail/<slug:slug>', views.post_detail, name='post_detail'),
    # path('list', views.posts_list, name="posts_list"),
    path('list', views.ArticleListView.as_view(), name="posts_list"),    
    # path('list', views.ArticleList.as_view(), name="posts_list"),    
    path('category/<int:pk>', views.category_detail , name="category_detail"),
    path('search/', views.search, name="search_articles"),
    # path('contactus/', views.contactus, name='contact_us'),
    # path('contactus/', views.ContactUsView.as_view(), name='contact_us'),
    path('contactus/', views.MessageView.as_view(), name='contact_us'),
    path('testbase/', views.TestBaseView.as_view(), name='test_base'),
    path('users', views.UserList.as_view(), name="user_list"),    
    path('red', views.HomePageRedirect.as_view(), name="redirect"),
    path('detail/<slug:slug>', views.ArticleDetailView.as_view(), name='post_detail'),
    path('messages/', views.MessageListView.as_view(), name="message_list"),
    path('message/edit/<int:pk>', views.MessageUpdateView.as_view(), name="message_edit"),
    path('message/delete/<int:pk>', views.MessageDeleteView.as_view(), name="message_delete"),
    path('archive/', views.ArchiveIndexArticleView.as_view(), name="archive"),
    path('archive/<int:year>', views.YearArchiveArticleView.as_view(), name="archive_year"),
]
