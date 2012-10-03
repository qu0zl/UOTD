from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

#import profiles.models

# Create your models here.

#class BaseType(models.Model):
#    name = models.CharField(max_length=100)
#    cost = models.IntegerField(default=0)

#class Unit(models.Model):
#    name = models.CharField(max_length=100)
#    baseType = models.ManyToManyField(BaseType, default=None, blank=False)

class CampaignApplicant(models.Model):
    user = models.ForeignKey(User)
    campaign = models.ForeignKey('Campaign')
    creationTime = models.DateTimeField(auto_now_add=True, null=True)
    def __unicode__(self):
        return u"Campaign: %s, User: %s, Date: %s" % (self.campaign, self.user, self.creationTime)

class Campaign(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, null=True, default=None, blank=False, editable=False, related_name="campaigns")
    description = models.TextField(max_length=800, blank=True)
    # owner will always have admin rights and cannot be removed, so admin table can be empty
    admins = models.ManyToManyField(User, related_name='Campaign Admin Table', default=None, blank=True)
    players = models.ManyToManyField(User, related_name='Campaign Player Table', default=None, blank=True)
    teams = models.ManyToManyField('Team', related_name='Campaign Team Table', default=None, blank=True)
    coins = models.IntegerField(default=150)
    # secret key for campaign. Used to allow player to add themselves to the campaign.
    secret = models.CharField(max_length=40)
    applicants = models.ManyToManyField(User, default=None, through='CampaignApplicant', blank=True)
    #players can add teams to campaign?

    # Campaign options
    #greg things like can...
    # players can add old team or only start new one?
    # campaign private? ie can others look at it
    def __unicode__(self):
        return u"%s:%s" % (self.id, self.name)

    def is_admin(self, user):
        print 'user is: %s, owner is %s' % (user, self.owner.get())
        if user == self.owner.get() or user in self.admins.all():
            return True
        else:
            return False

class CampaignForm(forms.ModelForm):
        class Meta:
            model = Campaign
            fields = ['name', 'coins', 'secret', 'description']

# Used for unit and weapon stats
STAT_CHOICES = (
    (1,  _('1')),
    (2,  _('2')),
    (3,  _('3')),
    (4,  _('4')),
    (5,  _('5')),
    (6,  _('6')),
    (7,  _('7')),
    (8,  _('8')),
    (9,  _('9')),
    (10,  _('10')),
    (11,  _('11')),
    (12,  _('12')),
)

class Weapon(models.Model):
    HANDS_CHOICES = (
        (1, _('1')),
        (2, _('2')),
        (3, _('3')),
        (4, _('4')),
    )
    def __unicode__(self):
        return self.name
    name = models.CharField(max_length=100)
    # greg add notes field?
    cost = models.SmallIntegerField(default=0, blank=False)
    hands = models.SmallIntegerField(choices=HANDS_CHOICES, default=0, blank=False)
    ccw = models.BooleanField(default=False)
    medieval = models.BooleanField(default=False)
    # -1 for shortRange means template
    shortRange = models.SmallIntegerField(default=0, blank=True)
    mediumRange = models.SmallIntegerField(default=0, blank=True)
    longRange = models.SmallIntegerField(default=0, blank=True)
    strength = models.SmallIntegerField(choices=STAT_CHOICES, default=5)

#class UnitWeapon(models.Model):
#    weapon = models.ForeignKey('Weapons')
#    unit = models.ForeignKey('BaseUnit')
#    nameOverride = models.CharField(max_length=100, blank=True)
#    # Is it a main-weapon or an anti-infantry weapon?
#    mountType = models.SmallIntegerField(choices=MOUNT_TYPE_CHOICES, default=0, blank=False)
#    def __unicode__(self):
#        if self.nameOverride:
#            return self.nameOverride
#        else:
#            return unicode(self.weapon)

class Faction(models.Model):
    GOOD=1
    NEUTRAL=2
    EVIL=2
    ALIGNMENT_CHOICES = (
        (GOOD,  _('Good')),
        (NEUTRAL,  _('Neutral')),
        (EVIL,  _('Evil')),
    )
    def __unicode__(self):
        return self.name
    name = models.CharField(max_length=100)
    alignment = models.SmallIntegerField(choices=ALIGNMENT_CHOICES, default=2, blank=False)
    # Do you have to pay a premium to choose this faction? EG the specialised Gentlemen's Clubs
    cost = models.SmallIntegerField(default=0, blank=False)

# Describes a unit or team-member model. These are the unmodified statistics that will
# act as a template on which instances of units in a campaign will be based.

class UnitTemplate(models.Model):
    def __unicode__(self):
        return self.name
    faction = models.ManyToManyField(Faction, related_name='unit_templates', default=None, blank=False)
    name = models.CharField(max_length=100)
    supernatural = models.BooleanField(default=False)
    # If maxCount > 0 then that is the maximum number of that unitType in a faction
    maxCount = models.SmallIntegerField(default=0, blank=False)
    # Use SmallInt rather than Boolean for hero and leader in case a third option is later added to the game
    hero = models.BooleanField(default=False)
    leader = models.BooleanField(default=False)
    animal = models.BooleanField(default=False)
    cost = models.SmallIntegerField(default=100, blank=False)
    movement = models.SmallIntegerField(choices=STAT_CHOICES, default=4, blank=False)
    combat = models.SmallIntegerField(choices=STAT_CHOICES, default=3, blank=False)
    marksmanship = models.SmallIntegerField(choices=STAT_CHOICES, default=3, blank=False)
    strength = models.SmallIntegerField(choices=STAT_CHOICES, default=3, blank=False)
    fortitude = models.SmallIntegerField(choices=STAT_CHOICES, default=3, blank=False)
    attacks = models.SmallIntegerField(choices=STAT_CHOICES, default=1, blank=False)
    wounds = models.SmallIntegerField(choices=STAT_CHOICES, default=1, blank=False)
    bravado = models.SmallIntegerField(choices=STAT_CHOICES, default=4, blank=False)
    arcane = models.SmallIntegerField(choices=STAT_CHOICES, default=3, blank=False)
#
    #weapons somehow

# modified from a 
class Unit(models.Model):
    # greg change this to point to a unittemplate and base all calculations on that
    # that way any changes to the base class will be propagated to all derived units
    # i think that would be better
    # greg change this to ForeignKey assuming you find no problems with that
    baseUnit = models.ForeignKey(UnitTemplate, default=None, blank=False)

    @property
    def leader(self):
        # greg extend to support a local over-ride flag for units that get promoted to leadership
        return self.baseUnit.leader
    # greg put team and owner in here too
    #def __init__(self, *args, **kwargs):
    #    super(Unit, self).__init__(*args, **kwargs)

class Team(models.Model):
    name = models.CharField(max_length=100)
    faction = models.ForeignKey(Faction, default=None, blank=False)
    owner = models.ForeignKey(User, null=True, default=None, blank=True)
    coins = models.IntegerField(default=0)
    description = models.TextField(max_length=800, blank=True)
    units = models.ManyToManyField(Unit, default=None, blank=True)
    def __unicode__(self):
        return self.name
    # Does this Team have a leader model
    def hasLeader(self):
        for item in self.units.all():
            if item.leader:
                return True
        return False
    def canHire(self, unitTemplate):
        # Can we afford it
        if unitTemplate.cost > self.coins:
            return False
        # Not allowed two leaders
        if unitTemplate.leader and self.hasLeader:
            return False
        # Not allowed exceed maximum number of certain models
        if unitTemplate.maxCount > 0:
            if team.count(unitTemplate) >= unitTemplate.maxCount:
                return False
        return True
    def hire(self, unitTemplate):
        if not self.canHire:
            return False
        unit = eotd.models.Unit(baseUnit=unitTemplate)
        unit.save()
        self.units.add(unit)
        return True



class NewTeamForm(forms.ModelForm):
        class Meta:
            model = Team
            fields = ['name', 'coins', 'faction', 'description']

class TeamForm(forms.ModelForm):
        class Meta:
            model = Team
            fields = ['name', 'description']

