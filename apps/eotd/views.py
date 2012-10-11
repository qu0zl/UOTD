from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.forms.formsets import formset_factory
import json
from django.utils import simplejson
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
    gameForm = None
    if ( campaign_id != "0" ):
        try:
            campaign = eotd.models.Campaign.objects.get(id=campaign_id)
            form = eotd.models.CampaignForm(instance=campaign)
            gameForm = eotd.models.NewGameForm(campaign=campaign)
        except:
            return HttpResponseBadRequest(_('No such campaign id. It may have been deleted.'))
        campaign_owner = campaign.owner
    else:
        form = eotd.models.CampaignForm(initial = {"secret": "%s" % ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(16)) })
    return render_to_response('eotd/campaign.html', \
        {
            'campaign':campaign,
            'campaign_id':campaign_id,
            'edit':campaign_id == "0" or (request.user.is_authenticated() and campaign.isAdmin(request.user)),
            'formObject':form,
            'gameForm':gameForm,
            'userTeams':eotd.models.Team.objects.filter(owner=request.user),
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
                campaign.owner=(request.user) 
                campaign.save() 
                print 'saved new campaign - %d' % campaign.id 
            else: 
                campaign = eotd.models.Campaign.objects.get(id=campaign_id) 
                # If the authenticated user is not the owner of this object then don't let them edit it! 
                if (request.user != campaign.owner):
                    print 'Attempt by user %s to edit campaign owned by user %s' % (request.user, campaign.owner) 
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


def campaignGame(request, campaign_id):
    try:
        if request.user.is_authenticated() and request.method == 'POST':
            campaign = eotd.models.Campaign.objects.get(id=campaign_id)
            if campaign.isAdmin(request.user):
                teams = request.POST.getlist('teams') + request.POST.getlist('teamTwo')
                date_parts=request.POST['date'].split('/')
                date="%s-%s-%s" % (date_parts[2], date_parts[0], date_parts[1])
                game = eotd.models.Game(date=date, campaign=campaign)
                game.save() # Need id before accessing M2M fields
                try:
                    for item in teams:
                        team = eotd.models.Team.objects.get(id=item)
                        gameTeam = eotd.models.GameTeam(game=game, team=team)
                        gameTeam.save()
                except Exception as e:
                    # don't leave the failed game hanging around
                    game.delete() # greg on delete clean up any GameTeam objects pointing to this.
                return redirect('/eotd/campaign/%s/' % campaign_id)
            else:
                print request.user
                return HttpResponseBadRequest(_('Not an admin of this campaign.'))
    except Exception as e:
        print 'campaignGame Exception', e
        return HttpResponseBadRequest(_('Failed to add game.'))

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
        if 'createTeam' in request.POST:
            return teamNewForCampaign(request, campaign=campaign)
        if 'addTeam' in request.POST:
            team = eotd.models.Team.objects.get(id=request.POST['addPriorTeam'])
            try:
                campaign.addTeam(team)
                return HttpResponse(_('Added team to campaign.'))
            except PermissionDenied as e:
                return HttpResponseBadRequest(_(str(e)))
    return HttpResponseBadRequest(_('Invalid campaign join attempt.'))

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

def teamPrint( request, team_id ):
    team = eotd.models.Team.objects.get(id=team_id)
    return render_to_response('eotd/team_print.html', \
        {
            'team':team,
        }, \
        RequestContext(request))

# If campaign is not None then this team is assigned to that campaign, if legal.
def teamNewForCampaign(request, campaign=None):
    try:
        coins = campaign.coins
    except:
        coins = 150 # default size
    if request.user.is_authenticated():
        form = eotd.models.NewTeamForm(initial={'coins':coins, 'campaignID':campaign.id if campaign else 0})
        return render_to_response('eotd/team_new.html', \
            {
                'formObject':form,
            }, \
            RequestContext(request))
    else:
        return HttpResponseForbidden(_('You must be logged in to create a new team.'))
        #return render_to_response('eotd/team_new.html', {}, RequestContext(request))

def teamNew(request):
    return teamNewForCampaign(request, campaign=None)

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
            'formObject':form,
            'edit': request.user.is_authenticated() and request.user == team.owner
        }, \
        RequestContext(request))

def teamInnerForm(request, team_id):
    print 'greg, teamInnerForm'
    team = eotd.models.Team.objects.get(id=team_id)
    return render_to_response('eotd/team_inner.html', \
        {
            'team':team,
            'edit': request.user.is_authenticated() and request.user == team.owner
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
        try:
            campaign = eotd.models.Campaign.objects.get(id=form.cleaned_data['campaignID'])
            # greg use a clas method that checks for exclusivity etc, player member of this campaign, etc
            campaign.addTeam(team)
        except KeyError:
            pass
        except Exception as e:
            print 'Exception adding this team to campaign.', e
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
                print 'Attempt by user %s to edit team owned by user %s' % (request.user, team.owner) 
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
    if request.user.is_authenticated():
        try:
            team = eotd.models.Team.objects.get(id=team_id)
            unitTemplate = eotd.models.UnitTemplate.objects.get(id=unit_id)
            if (request.user != team.owner):
                print 'Attempt by user %s to edit team owned by user %s' % (request.user, team.owner)
                return HttpResponseForbidden(_('You are not authorized to edit this team. Are you logged in correctly?') )
            try:
                coins = team.hire(unitTemplate)
            except Exception as e:
                print 'team.hire exception:', e
                return HttpResponseBadRequest(_('You are not allowed hire this model. Check cost, multiple-leaders, etc.'))
        except Exception as e:
            print 'greg, exception caught in teamHire', e
    else:
        return HttpResponseForbidden(_('You are not logged in.'))
    return HttpResponseRedirect('/eotd/team/%s/' % team_id)

        # greg work for ajax and request.method == 'POST':

def teamFire(request, team_id, unit_id):
    pass

def teamReorder(request, team_id):
    if request.is_ajax() and request.user.is_authenticated() and request.method == 'POST':
        team = eotd.models.Team.objects.get(id=team_id)
        if request.user == team.owner:
            order = request.POST.getlist('order[]')
            team.reorder(order)
            print order
            return HttpResponse()
        else:
            return HttpResponseBadRequest(_('User unauthorised.'))
    else:
        return HttpResponseBadRequest(_('Failed to update name'))


def unitName(request, unit_id):
    try:
        if request.is_ajax() and request.user.is_authenticated():
            unit = eotd.models.Unit.objects.get(id=unit_id)
            if request.user == unit.team.owner:
                print 'trying to set name to', request.POST['name']
                unit.name = request.POST['name']
                unit.save()
                return HttpResponse()
            else:
                print request.user
                print unit.owner
                return HttpResponseBadRequest(_('User unauthorised.'))
    except Exception as e:
        print 'unitName Exception', e
        return HttpResponseBadRequest(_('Failed to update name'))

# team_id is necessary when moving a store item as we don't have a unit to deduce team from
def weaponMove(request, team_id):
    try:
        if request.is_ajax() and request.user.is_authenticated():
            store=False
            if request.POST['from']=='store':
                fromUnit = None
            else:
                fromUnit = eotd.models.Unit.objects.get(id=request.POST['from'])
            if request.POST['to']=='sell':
                toUnit = None
            elif request.POST['to']=='store':
                toUnit = None
                store=True
            else:
                toUnit = eotd.models.Unit.objects.get(id=request.POST['to'])
            weaponEntry = eotd.models.UnitWeapon.objects.filter(unit=fromUnit, weapon__id=request.POST['weapon'])
            # If it's a store item then ensure it's one belonging to this team.
            if not fromUnit:
                team = eotd.models.Team.objects.get(id=team_id)
                weaponEntry = weaponEntry.filter(team=team)[0]
            else:
                team = fromUnit.team
                weaponEntry = weaponEntry.all()[0]

            if team.owner != request.user:
                raise Exception("Unauthorized attempt to edit team.")
            if (toUnit and team != toUnit.team) or (store and fromUnit.team!=team):
                raise Exception("Units are not on the same team.")
            # sale
            if not toUnit and not store:
                # greg logic to handle pawn depreciation
                team.coins = team.coins + weaponEntry.weapon.cost
                team.save()
                weaponEntry.delete()
            # store
            elif not toUnit:
                weaponEntry.team = team
                weaponEntry.unit = None
                weaponEntry.save()
            # move    
            else:
                toUnit.allowedWeapon(weaponEntry.weapon) # will raise exception if illegal
                weaponEntry.unit=toUnit
                weaponEntry.team = None
                weaponEntry.save()
        else:
            return HttpResponseBadRequest(_('User unauthorised.'))
    except Exception as e:
        return HttpResponseBadRequest(_('Failed to move weapon'))
    return HttpResponse()

# Do not put anything private in here as the user does NOT need to be authenticated.
# I consider the equipment options available to a model to be public knowledge
def unitEquipHTML(request, unit_id):
    try:
        if request.is_ajax():
            unit = eotd.models.Unit.objects.get(id=unit_id)
            return render_to_response('eotd/unit_equipment.html', \
                {
                    'unit':unit,
                }, \
                RequestContext(request))
    except Exception as e:
        print 'unitEquipHTML Exception', e
        return HttpResponseBadRequest(_('Failed to retrieve equipment options.'))

def unitBuyHTML(request, unit_id, item_id):
    try:
        if request.is_ajax() and request.user.is_authenticated():
            unit = eotd.models.Unit.objects.get(id=unit_id)
            if request.user == unit.team.owner:
                unit.addWeapon(item_id)
                unit.save()
                return render_to_response('eotd/unit_equipment.html', \
                    {
                        'unit':unit,
                        }, \
                    RequestContext(request))
            else:
                return HttpResponseBadRequest(_('User unauthorised.'))
    except PermissionDenied as e:
        return HttpResponseBadRequest(_(str(e)))
    except Exception as e:
        print 'unitBuyHtml Exception', e
        return HttpResponseBadRequest(_('Error purchasing equipment. Please retry.'))

def gameForm(request, game_id):
    try:
        game = eotd.models.Game.objects.get(id=game_id)
        teams = []
        units = []
        for item in game.gameteam_set.all():
            teams.append( eotd.models.GameFormLine( initial = {
                "team":item.team, "earnings":item.earnings, "victoryPoints":item.victoryPoints, "teamID":item.team.id}))
            inner = []
            for unit in item.gameunit_set.all():
                # greg need to modify below unit.skills.get to .all() if we move to multiple skills per game
                line = eotd.models.GameUnitLine( prefix=str(unit.id), initial = {
                    "name":unit.unit.name, "skills":unit.skills.get() if unit.skills.count()>0 else None, "injuries":unit.injuries, "summary":unit.unit.gearAsString} )
                inner.append( line)
            units.append(inner)
        # greg confirm what happens with a logged out user calling canEdit below?
        return render_to_response('eotd/game.html', \
            {
                'game':game,
                'teams':teams,
                'unitArray':units,
                'edit':game.canEdit(request.user)
                }, \
            RequestContext(request))
    except Exception as e:
        print 'gameForm exception: ', e
        return HttpResponseBadRequest(_('Error viewing game. Please retry.'))

def gameUpdate(request, game_id):
    try:
        if request.user.is_authenticated() and request.method == 'POST':
            game = eotd.models.Game.objects.get(id=game_id)

            if not game.canEdit(request.user):
                return HttpResponseBadRequest(_('You are not authorized to modify this game.'))
            team = eotd.models.Team.objects.get(id=int(request.POST['save']))
            gameTeam = eotd.models.GameTeam.objects.get(game__id=game_id, team=team)
            oldEarnings = gameTeam.earnings
            gameTeam.earnings = int(request.POST['earnings'])
            earningsDiff = gameTeam.earnings - oldEarnings
            gameTeam.victoryPoints = request.POST['victoryPoints']
            gameTeam.save()
            team.coins = team.coins+earningsDiff
            team.save()
            # Freeze the list of units used by this team in this game
            gameTeam.freezeUnits()
            return redirect('/eotd/game/%s/' % game_id)
    except Exception as e:
        print 'gameUpdate Exception', e
        return HttpResponseBadRequest(_('Failed to update game.'))


def gameUnits(request, game_id):
    try:
        if request.user.is_authenticated() and request.method == 'POST':
            game = eotd.models.Game.objects.get(id=game_id)

            if not game.canEdit(request.user):
                return HttpResponseBadRequest(_('You are not authorized to modify this game.'))
            print request.POST # greg remove
            #team = eotd.models.Team.objects.get(id=int(request.POST['update']))
            #gameTeam = eotd.models.GameTeam.objects.get(game__id=game_id, team=team)
            for item in request.POST:
                if item.endswith('-skills'):
                    prefix=item.split('-')[0]
                    gameUnit = eotd.models.GameUnit.objects.get(id=prefix)
                    gameUnit.skills = request.POST[item]
                    gameUnit.injuries = request.POST['%s-injuries' % prefix]
                    gameUnit.save()
                    #greg check this user can edit this gameUnit somehow
            return redirect('/eotd/game/%s/' % game_id)
    except Exception as e:
        print 'gameUnits Exception', e
        return HttpResponseBadRequest(_('Failed to update game.'))

def gameDelete(request, game_id):
    try:
        if request.user.is_authenticated():
            game = eotd.models.Game.objects.get(id=game_id)
            campaign = game.campaign

            if campaign.isAdmin(request.user):
                game.delete()
                return redirect('/eotd/campaign/%s/' % campaign.id)
        return HttpResponseBadRequest(_('You are not authorized to delete this game.'))
    except Exception as e:
        print 'gameDelete Exception', e
        return HttpResponseBadRequest(_('Failed to delete game.'))
