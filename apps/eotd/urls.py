from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns("",
    url(r"^$", direct_to_template, {"template": "eotd/eotd.html"}, name="eotd"),
    url(r"^terms/$", direct_to_template, {"template": "eotd/terms.html"}, name="terms"),
    url(r"^privacy/$", direct_to_template, {"template": "eotd/privacy.html"}, name="privacy"),
    url(r"^dmca/$", direct_to_template, {"template": "eotd/dmca.html"}, name="dmca"),
    url(r"^what_next/$", direct_to_template, {"template": "eotd/what_next.html"}, name="what_next"),
    url(r"^help/unit/$", direct_to_template, {"template": "eotd/campaign_help.html"}, name="campaign_help"),
    url(r"^help/FAQ/$", direct_to_template, {"template": "eotd/FAQ.html"}, name="FAQ"),
    (r'^campaign/$', 'eotd.views.campaignList'),
    (r'^campaign/(\d+)/$', 'eotd.views.campaignForm'),
    (r'^campaign/(\d+)/save/$', 'eotd.views.campaignSave'),
    (r'^campaign/(\d+)/join/$', 'eotd.views.campaignJoinHandler'),
    (r'^campaign/(\d+)/applicant/$', 'eotd.views.campaignApplicantList'),
    (r'^campaign/(\d+)/game/$', 'eotd.views.campaignGame'),
    (r'^campaign/applicant/(\d+)/(\w+)/$', 'eotd.views.campaignApplicantHandler'),
    # greg still need the below line?
    (r'^campaign/(\d+)/team/(\w+)/$', 'eotd.views.campaignTeamHandler'),
    (r'^campaign/(?P<campaign_id>\d+)/(?P<user_id>\d+)/(?P<command>\w+)/$', 'eotd.views.campaignMangeAdmin'),
    (r'^team/$', 'eotd.views.teamList'),
    (r'^team/list/(\d+)/$', 'eotd.views.teamList'),
    (r'^team/0/save/$', 'eotd.views.newTeamSave'),
    (r'^team/(\d+)/save/$', 'eotd.views.teamSave'),
    (r'^team/0/$', 'eotd.views.teamNew'),
    (r'^team/(\d+)/$', 'eotd.views.teamForm'),
    (r'^team/(\d+)/inner/$', 'eotd.views.teamInnerForm'),
    (r'^team/(\d+)/csv/$', 'eotd.views.teamCSV'),
    (r'^team/(\d+)/print/$', 'eotd.views.teamPrint'),
    (r'^team/(\d+)/hire/(\d+)/$', 'eotd.views.teamHire'),
    (r'^team/(\d+)/reorder/$', 'eotd.views.teamReorder'),
    (r'^team/(\d+)/delete/$', 'eotd.views.teamDelete'),
    (r'^team/(\d+)/delete/confirm/$', 'eotd.views.teamDelete', {"confirm": True}),
    (r'^unit/(\d+)/rename/$', 'eotd.views.unitName'),
    (r'^unit/(\d+)/equip/$', 'eotd.views.unitEquipHTML'),
    (r'^unit/(\d+)/injuries/$', 'eotd.views.unitInjuryHTML'),
    (r'^unit/(\d+)/buy/(\d+)/$', 'eotd.views.unitBuyHTML'),
    (r'^unit/(\d+)/injuries/(\d+)/$', 'eotd.views.unitHealHTML'),
    (r'^unit/(\d+)/fire/$', 'eotd.views.unitFireHTML'),
    (r'^unit/(\d+)/unretire/$', 'eotd.views.unitUnFireHTML'),
    (r'^game/(\d+)/$', 'eotd.views.gameForm'),
    (r'^game/(\d+)/update/$', 'eotd.views.gameUpdate'),
    (r'^game/(\d+)/delete/$', 'eotd.views.gameDelete'),
    (r'^game/(\d+)/units/$', 'eotd.views.gameUnits'),
    (r'^stats/recent/$', 'eotd.views.statsRecent'),
    (r'^weapon/(?P<team_id>\d+)/move/$', 'eotd.views.weaponMove'),
)
