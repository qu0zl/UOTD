from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
# no longer needed - from itertools import chain

#import profiles.models

# Create your models here.

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

WEAPON_STRENGTH_CHOICES = (
    (-2, _("Model's Strength + 2")),
    (-1, _("Model's Strength + 1")),
    (0, _("Model's Strength")),
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
    strength = models.SmallIntegerField(choices=WEAPON_STRENGTH_CHOICES, default=5)

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
    combatMod = models.SmallIntegerField(default=0, blank=False)
    marksmanshipMod = models.SmallIntegerField(default=0, blank=False)
    bravadoMod = models.SmallIntegerField(default=0, blank=False)
    arcaneMod = models.SmallIntegerField(default=0, blank=False)

class UnitTemplateWeapon(models.Model):
    weapon = models.ForeignKey('Weapon')
    unitTemplate = models.ForeignKey('UnitTemplate')

class UnitWeapon(models.Model):
    weapon = models.ForeignKey('Weapon')
    unit = models.ForeignKey('Unit')
    nameOverride = models.CharField(max_length=100, blank=True)
    def __unicode__(self):
        if self.nameOverride:
            return self.nameOverride
        else:
            return unicode(self.weapon)

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
    weapons = models.ManyToManyField('Weapon', default=None, through='UnitTemplateWeapon', blank=True)
#
    #weapons somehow

# modified from a 
class Unit(models.Model):
    class Meta:
        ordering = ['unitOrder']
    # base unit template on which this unit is modified.
    # All statistics are calculated as differences from this template unit
    baseUnit = models.ForeignKey(UnitTemplate, default=None, blank=False)
    unitName = models.CharField(max_length=100)
    # Has this model been promoted to being a leader
    unitLeaderOverride = models.BooleanField(default=False)
    # Set this unit's faction at creation time, as we may be a unit that belongs to multiple factions and
    # could have faction specific modifiers.
    faction = models.ForeignKey(Faction, related_name='faction_units', default=None, blank=False)
    unitWeapons = models.ManyToManyField('Weapon', default=None, through='UnitWeapon', blank=True)
    team = models.ForeignKey('Team', related_name='units', default=None, blank=False)
    # used for unit ordering in a team
    unitOrder = models.SmallIntegerField(default=999, blank=False)

    @property
    def leader(self):
        return self.unitLeaderOverride or self.baseUnit.leader
    @leader.setter
    def leader(self, value):
        self.unitLeaderOverride = True
    @property
    def name(self):
        return self.unitName if self.unitName else self.baseUnit.name
    @name.setter
    def name(self, value):
        self.unitName = value
    @property
    def movement(self):
        return self.baseUnit.movement
    @property
    def combat(self):
        return self.baseUnit.combat+self.faction.combatMod
    @property
    def marksmanship(self):
        return self.baseUnit.marksmanship + self.faction.marksmanshipMod
    @property
    def strength(self):
        return self.baseUnit.strength
    @property
    def fortitude(self):
        return self.baseUnit.fortitude
    @property
    def attacks(self):
        return self.baseUnit.attacks
    @property
    def wounds(self):
        return self.baseUnit.wounds
    @property
    def bravado(self):
        return self.baseUnit.bravado + self.faction.bravadoMod
    @property
    def arcane(self):
        return self.baseUnit.arcane + self.faction.arcaneMod
    @property
    def cost(self):
        return self.baseUnit.cost
    @property
    def weapons(self):
        return self.baseUnit.weapons.all() | self.unitWeapons.all()
            # or can do it via chain
            #weapon_list = sorted(
            #    chain(self.baseUnit.weapons.all(), self.unitWeapons.all()),
            #    key=lambda instance: instance.date_created)
            #return weapon_list

    # greg put team and owner in here too
    #def __init__(self, *args, **kwargs):
    #    super(Unit, self).__init__(*args, **kwargs)

class Team(models.Model):
    name = models.CharField(max_length=100)
    faction = models.ForeignKey(Faction, default=None, blank=False)
    owner = models.ForeignKey(User, null=True, default=None, blank=True)
    coins = models.IntegerField(default=0)
    description = models.TextField(max_length=800, blank=True)
    #units = models.ManyToManyField(Unit, default=None, blank=True)
    def __unicode__(self):
        return self.name
    # Does this Team have a leader model
    def hasLeader(self):
        for item in self.units.all():
            if item.leader:
                import pdb;pdb.set_trace()
                return True
        return False
    def canHire(self, unitTemplate):
        # Can we afford it
        if unitTemplate.cost > self.coins:
            return False
        # Not allowed two leaders
        if unitTemplate.leader and self.hasLeader():
            return False
        # Not allowed exceed maximum number of certain models
        if unitTemplate.maxCount > 0:
            if team.count(unitTemplate) >= unitTemplate.maxCount:
                return False
        return True
    def hire(self, unitTemplate):
        if not self.canHire(unitTemplate):
            raise Exception('Unable to hire this unit.')
        unit = Unit(faction=self.faction, baseUnit=unitTemplate, team=self, unitOrder=self.units.count()+1)
        print 'unit unitOrder is', unit.unitOrder
        unit.save()
        self.coins = self.coins - unitTemplate.cost
        self.save()
        return self.coins
    def reorder(self, order):
        try:
            for i, item in enumerate(order,1):
                print i, item
                unit = self.units.get(id=item)
                unit.unitOrder=i
                unit.save()
        except Exception as e:
            print 'greg big catch all. Remove.', e

class NewTeamForm(forms.ModelForm):
        class Meta:
            model = Team
            fields = ['name', 'coins', 'faction', 'description']

class TeamForm(forms.ModelForm):
        class Meta:
            model = Team
            fields = ['name', 'description']

