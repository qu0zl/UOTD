from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template


urlpatterns = patterns("",
    url(r"^$", direct_to_template, {"template": "eotd/eotd.html"}, name="eotd"),
    url(r"^terms/$", direct_to_template, {"template": "eotd/terms.html"}, name="terms"),
    url(r"^privacy/$", direct_to_template, {"template": "eotd/privacy.html"}, name="privacy"),
    url(r"^dmca/$", direct_to_template, {"template": "eotd/dmca.html"}, name="dmca"),
    url(r"^what_next/$", direct_to_template, {"template": "eotd/what_next.html"}, name="what_next"),
    (r'^campaign/$', 'eotd.views.campaignList'),
    (r'^campaign/(\d+)/$', 'eotd.views.campaignForm'),
    (r'^campaign/(\d+)/save/$', 'eotd.views.campaignSave'),
    (r'^campaign/(\d+)/join/$', 'eotd.views.campaignJoinHandler'),
    (r'^campaign/(\d+)/applicant/$', 'eotd.views.campaignApplicantList'),
    (r'^campaign/applicant/(\d+)/(\w+)/$', 'eotd.views.campaignApplicantHandler'),
    # greg still need the below line?
    (r'^campaign/(\d+)/team/(\w+)/$', 'eotd.views.campaignTeamHandler'),
    (r'^team/$', 'eotd.views.teamList'),
    (r'^team/0/save/$', 'eotd.views.newTeamSave'),
    (r'^team/(\d+)/save/$', 'eotd.views.teamSave'),
    (r'^team/0/$', 'eotd.views.teamNew'),
    (r'^team/(\d+)/$', 'eotd.views.teamForm'),
    (r'^team/(\d+)/hire/(\d+)/$', 'eotd.views.teamHire'),
    (r'^team/(\d+)/fire/(\d+)/$', 'eotd.views.teamFire'),
    (r'^team/(\d+)/reorder/$', 'eotd.views.teamReorder'),
    (r'^unit/(\d+)/rename/$', 'eotd.views.unitName'),
)
