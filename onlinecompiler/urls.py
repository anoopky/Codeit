from django.conf.urls import url
import onlinecompiler.views as v
from django.contrib.admin.views.decorators import staff_member_required

urlpatterns = [
    url(r'compileTest', v.compile_debug, name='compileTest'),
    url(r'compile', v.compile_test_cases, name='compile'),
    url(r'add', staff_member_required(v.add_question, login_url="/login"), name='add_question'),
    url(r'result', v.result, name='result'),
    url(r'^$', v.dashboard, name='dashboard'),
    url(r'login', v.login_user, name='login'),
    url(r'logout', v.logout_user, name='logout'),
    url(r'^question/(?P<idn>\d+)/$', v.question, name='questions'),
]
