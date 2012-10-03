from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import json
from datetime import datetime
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render_to_response, redirect, render
from django.template import RequestContext
import random, string
import eotd.models

# Create your views here.


def campaignForm(request, campaign_id):
    campaign_owner = None
    campaign = None
    if ( campaign_id != "0" ):
        try:
            campaign = eotd.models.Campaign.objects.get(id=campaign_id)
            form = eotd.models.CampaignForm(instance=campaign)
        except:
            return HttpResponseBadRequest(_('No such campaign id. It may have been deleted.'))
        campaign_owner = campaign.owner.get()
    else:
        form = eotd.models.CampaignForm(initial = {"secret": "%s" % ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(16)) })
    return render_to_response('eotd/campaign.html', \
        {
            'campaign':campaign,
            'campaign_id':campaign_id,
            'campaign_owner':campaign_owner,
            'formObject':form
        }, \
        RequestContext(request))

def campaignSave(request, campaign_id):
    print 'trying to save campaign %s' % campaign_id 
    campaign_id = int(campaign_id) 
    campaign_owner = None 
    if request.user.is_authenticated() and request.method == 'POST': # If the form has been submitted... 
        try:
            if (campaign_id == 0): # new campaign object 
                print 'trying to make new campaign' 
                form = eotd.models.CampaignForm(request.POST) # A form bound to the POST data
                campaign = form.save()
                campaign.owner.add(request.user) 
                campaign.save() 
                print 'saved new campaign - %d' % campaign.id 
            else: 
                campaign = eotd.models.Campaign.objects.get(id=campaign_id) 
                # If the authenticated user is not the owner of this object then don't let them edit it! 
                if (request.user != campaign.owner.get()):
                    print 'Attempt by user %s to edit campaign owned by user %s' % (request.user, campaign.owner.get()) 
                    return HttpResponseForbidden() 
                if 'delete' in request.POST: 
                    campaign.delete() 
                    return HttpResponseRedirect('/eotd/campaign/')
                # update the pre-existing campaign
                form = eotd.models.CampaignForm(request.POST, instance=campaign)
                form.save()
        except ValueError:
            print form._errors
            return HttpResponseBadRequest(_('Invalid Campaign data. Please sanity check data values'))
    else:
        return HttpResponseBadRequest(_('Invalid campaign save request. Are you logged in correctly?'))

    if campaign_id == 0:
        # New Campaign, so redirect to update the id in the user's URL bar
        return redirect('/eotd/campaign/%d/' % campaign.id)
    else:
        return campaignForm(request, campaign_id)

def campaignList( request ):
    campaigns = eotd.models.Campaign.objects.order_by('name')
    return render_to_response('eotd/list.html', \
        {
            'campaigns':campaigns,
        }, \
        RequestContext(request))

def addCampaignApplicant(campaign, user):
    print 'Adding applicant %s to campaign %s' % (user, campaign)
    try:
        prior = eotd.models.CampaignApplicant.objects.get(user=user, campaign=campaign)
        prior.creationTime = datetime.now()
        prior.save()
    except ObjectDoesNotExist:
        a = eotd.models.CampaignApplicant(campaign=campaign, user=user)
        a.save()

def campaignApply( request, campaign ):
    addCampaignApplicant(campaign, request.user)
    return redirect('/eotd/campaign/%d/' % campaign.id)

def campaignJoin( request, campaign ):
    try:
        password = request.POST['password']
        print 'password is :%s' % password
        if password.upper() == campaign.secret.upper():
            campaign.players.add(request.user)
            campaign.save()
        else:
            return HttpResponseForbidden(_('Password does not match campaign secret. Contact your campaign administrator for assistance.'))
    except Exception as e:
        print 'campaignJoin exception:', e
    return redirect('/eotd/campaign/%d/' % campaign.id)

def campaignJoinHandler( request, campaign_id ):
    if request.user.is_authenticated() and request.method == 'POST':
        campaign = eotd.models.Campaign.objects.get(id=campaign_id)
        if 'join' in request.POST:
            return campaignJoin(request, campaign)
        if 'apply' in request.POST:
            return campaignApply(request, campaign)

def campaignApplicantList( request, campaign_id ):
    campaign = eotd.models.Campaign.objects.get(id=campaign_id)
    applicants = eotd.models.CampaignApplicant.objects.filter(campaign=campaign).order_by('user__username')
    return render_to_response('eotd/applicants.html', \
        {
            'applicants':applicants,
        }, \
        RequestContext(request))

def campaignApplicantHandler( request, applicant_id, what ):
    if request.user.is_authenticated():
        try:
            applicant = eotd.models.CampaignApplicant.objects.get(id=applicant_id)
            campaign = applicant.campaign
            if campaign.is_admin(request.user):
                if what == 'approve':
                    campaign.players.add(applicant.user)
                    campaign.save()
                    applicant.delete()
                    return HttpResponseRedirect('/eotd/campaign/%s/' % campaign.id)
                elif what == 'deny':
                    applicant.delete()
                return HttpResponseRedirect('/eotd/campaign/%s/' % campaign.id)
            else:
                return HttpResponseForbidden(_('Attempt to modify campaign that does not belong to your account.'))
        except ObjectDoesNotExist:
            return HttpResponseForbidden(_('Failed in player application handling. Please try again via main campaign page.'))
    return HttpResponseForbidden(_('You are not authorized to modify this campaign. Are you correctly logged in?'))
    
# greg re-write or delete the below.
# i'm probably changing my approach to this
def campaignTeamHandler( request, campaign_id, what ):
    if request.user.is_authenticated():
        campaign = eotd.models.Campaign.objects.get(id=campaign_id)
        if campaign.is_player(request.user):
            if what == 'newTeam':
                pass
            elif what == 'addTeam':
                pass
    return HttpResponseForbidden(_('You are not authorized to add a team to this campaign. Are you correctly logged in and a member of this campaign?'))

def teamList( request ):
    teams = eotd.models.Team.objects.order_by('name')
    return render_to_response('eotd/team_list.html', \
        {
            'teams':teams,
        }, \
        RequestContext(request))

def teamNew(request):
    if request.user.is_authenticated():
        form = eotd.models.NewTeamForm()
        return render_to_response('eotd/team_new.html', \
            {
                'formObject':form,
            }, \
            RequestContext(request))
    else:
        return HttpResponseForbidden(_('You must be logged in to create a new team.'))
        #return render_to_response('eotd/team_new.html', {}, RequestContext(request))


def teamForm(request, team_id):
    team_owner = None
    team = None
    try:
        team = eotd.models.Team.objects.get(id=team_id)
        form = eotd.models.TeamForm(instance=team)
    except:
        return HttpResponseBadRequest(_('No such team id. It may have been deleted.'))
    team_owner = team.owner
    return render_to_response('eotd/team_edit.html', \
        {
            'team':team,
            'team_id':team_id,
            'team_owner':team_owner,
            'formObject':form
        }, \
        RequestContext(request))

# Save a new team - ie just the name, faction, coins and description.
def newTeamSave(request):
    if request.user.is_authenticated() and request.method == 'POST': # If the form has been submitted... 
        print 'trying to make new team' 
        form = eotd.models.NewTeamForm(request.POST) # A form bound to the POST data
        team = form.save() # save below after setting owner
        team.owner=request.user 
        team.save() 
        print 'saved new team - %d' % team.id 
        # New Team, so redirect to update the id in the user's URL bar
        return redirect('/eotd/team/%d/' % team.id)

# Save function for editing a pre-existing team.
def teamSave(request, team_id):
    print 'trying to save team %s' % team_id 
    team_id = int(team_id) 
    if request.user.is_authenticated() and request.method == 'POST': # If the form has been submitted... 
        try:
            team = eotd.models.Team.objects.get(id=team_id) 
            # If the authenticated user is not the owner of this object then don't let them edit it! 
            if (request.user != team.owner):
                print 'Attempt by user %s to edit team owned by user %s' % (request.user, team.owner.get()) 
                return HttpResponseForbidden(_('You are not authorized to edit this team. Are you logged in correctly?') )
            if 'delete' in request.POST: 
                team.delete() 
                return HttpResponseRedirect('/eotd/team/')
            # update the pre-existing team
            form = eotd.models.TeamForm(request.POST, instance=team)
            form.save()
        except ValueError:
            print form._errors
            return HttpResponseBadRequest(_('Invalid Team data. Please sanity check data values'))
    else:
        return HttpResponseBadRequest(_('Invalid team save request. Are you logged in correctly?'))

    return teamForm(request, team_id)

def teamHire(request, team_id, unit_id):
    if request.user.is_authenticated() and request.method == 'POST':
        try:
            team = eotd.models.Team.objects.get(id=team_id)
            unitTemplate = eotd.models.UnitTemplate(id=unit_id)
            if (request.user != team.owner):
                print 'Attempt by user %s to edit team owned by user %s' % (request.user, team.owner.get())
                return HttpResponseForbidden(_('You are not authorized to edit this team. Are you logged in correctly?') )
            if not team.hire(unitTemplate):
                return HttpResponseBadRequest(_('You are not allowed hire this model. Check cost, multiple-leaders, etc.'))
        except Exception as e:
            print 'greg, exception caught in teamHire', e
    return HttpResponseRedirect('/eotd/team/%s/' % team_id)

        # greg work for ajax and request.method == 'POST':

def teamFire(request, team_id, unit_id):
    pass

