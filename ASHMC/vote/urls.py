from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required


from .views import MeasureListing, MeasureDetail, MeasureResultList

urlpatterns = patterns('vote.views',
       url('^$', login_required(MeasureListing.as_view()), name='vote_main'),
       url('^measures/$', login_required(MeasureListing.as_view()), name='measure_list'),
       url('^measure/(?P<pk>\d+)/$', login_required(MeasureDetail.as_view()), name='measure_detail'),
       url('^results/$', login_required(MeasureResultList.as_view()), name='vote_measure_results'),
)
