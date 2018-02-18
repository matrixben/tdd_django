from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       # 如下url只在lists应用下调用，故转移到lists文件夹下
                       url(r'^(\d+)/$', 'lists.views.view_list', name='view_list'),
                       url(r'^(\d+)/add_item$', 'lists.views.add_item', name='add_item'),
                       url(r'^new$', 'lists.views.new_list', name='new_list'),
                       )
