from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
import math #used for ceil
import datetime
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
    admins = models.ManyToManyField(User, related_name='campaign_admin_table', default=None, blank=True)
    players = models.ManyToManyField(User, related_name='campaign_player_table', default=None, blank=True)
    teams = models.ManyToManyField('Team', related_name='campaign_team_table', default=None, blank=True)
    coins = models.IntegerField(default=150)
    # May teams involved in this campaign not be in any others?
    exclusive = models.BooleanField(default=False)
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

    def isAdmin(self, user):
        print 'user is: %s, owner is %s' % (user, self.owner)
        if user == self.owner or user in self.admins.all():
            return True
        else:
            return False
    # checks if the user is a player OR the owner. Owner is considered a player automatically.
    def isPlayer(self, user):
        if user in self.players.all() or user == self.owner:
            return True
        return False
    def addTeam(self, team):
        if not self.isPlayer(team.owner):
            raise PermissionDenied("Team owner is not a member of this campaign.")
        if self.coins < team.value:
            raise PermissionDenied("Team value is higher than that permitted to join this campaign.")
        if self.exclusive and team.campaign_team_table.count() > 0:
            raise PermissionDenied("This campaign does not allow a team to be in other campaigns. You must remove this team from any other campaigns in order to join.")
        self.teams.add(team)
        self.save()

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
    (-11, _("Model's Strength - 1")),
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

# need to link this to unitTemplate
# via a through model that controls if this is a normal or special access list
class SkillList(models.Model):
    def __unicode__(self):
        return self.name
    name = models.CharField(max_length=100)
    skills = models.ManyToManyField('Skill', related_name='skill_lists', default=None, blank=False)

# need to link this to unitTemplate
# via a through model
class WeaponList(models.Model):
    def __unicode__(self):
        return self.name
    name = models.CharField(max_length=100)
    weapons = models.ManyToManyField('Weapon', related_name='weapon_lists', default=None, blank=False)

class Injury(models.Model):
    MNG=1
    MINUS_STRENGTH=2
    MINUS_FORTITUDE=3
    ARRESTED=8
    CAPTURED=9
    DEAD=10
    INJURY_PENALTIES = (
        (MNG,  _('MNG')),
        (MINUS_STRENGTH,  _('-1 Strength')),
        (MINUS_FORTITUDE,  _('-1 Fortitude')),
        (ARRESTED, _('Arrested')),
        (CAPTURED, _('Captured')),
        (DEAD, _('Dead')),
    )
    def __unicode__(self):
        return self.name
    name = models.CharField(max_length=100)
    penalty = models.SmallIntegerField(choices=INJURY_PENALTIES, default=1, blank=False)

class Skill(models.Model):
    def __unicode__(self):
        return self.name
    name = models.CharField(max_length=100)
    arcanePower = models.BooleanField(default=False)

# covers weapons and non-weapon equipment.
# weapon field determines if it is or isn't a weapon
class Weapon(models.Model):
    HANDS_CHOICES = (
        (0, _('0')),
        (1, _('1')),
        (2, _('2')),
        (3, _('3')),
        (4, _('4')),
    )
    def __unicode__(self):
        return self.name

    weapon = models.BooleanField(default=True)
    name = models.CharField(max_length=100)
    # greg add notes field?
    cost = models.SmallIntegerField(default=0, blank=False)
    hands = models.SmallIntegerField(choices=HANDS_CHOICES, default=1, blank=False)
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
    EVIL=3
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

class UnitTemplateSkill(models.Model):
    skill = models.ForeignKey('Skill')
    unitTemplate = models.ForeignKey('UnitTemplate')

class UnitTemplateWeapon(models.Model):
    weapon = models.ForeignKey('Weapon')
    unitTemplate = models.ForeignKey('UnitTemplate')

class UnitTemplateSkillList(models.Model):
    # Do you need some special circumstance to be allowed use this skill-list?
    # EG a good roll on the skill table
    special = models.BooleanField(default=False)
    skillLists = models.ForeignKey('SkillList')
    unitTemplate = models.ForeignKey('UnitTemplate')

class UnitTemplateWeaponList(models.Model):
    medievalOnly = models.BooleanField(default=False)
    weaponLists = models.ForeignKey('WeaponList')
    unitTemplate = models.ForeignKey('UnitTemplate')

# If an item is held by a unit then the 'unit' field will be non-empty
# if the item is in a team's store, then the 'team' field will be non-empty
class UnitWeapon(models.Model):
    weapon = models.ForeignKey('Weapon')
    unit = models.ForeignKey('Unit', null=True)
    team = models.ForeignKey('Team', null=True)
    nameOverride = models.CharField(max_length=100, blank=True)
    # creationTime can be used to determine if a weapon was bought before or after
    # the most recent game, and thus if we get full price for selling it.
    creationTime = models.DateTimeField(auto_now_add=True, null=True)
    def __unicode__(self):
        if self.nameOverride:
            return self.nameOverride
        else:
            return unicode(self.weapon)
    def sell(self):
        try:
            team = self.unit.team
        except AttributeError as e:
            team = self.team
        if team.playedSince(self.creationTime):
                team.coins = team.coins + math.ceil(self.weapon.cost/2.0)
        else:
            team.coins = team.coins + self.weapon.cost
        team.save()
        self.delete()
# Describes a unit or team-member model. These are the unmodified statistics that will
# act as a template on which instances of units in a campaign will be based.

class UnitTemplate(models.Model):
    def __unicode__(self):
        return self.name
    faction = models.ManyToManyField(Faction, related_name='unit_templates', default=None, blank=False)
    name = models.CharField(max_length=100)
    weaponLists = models.ManyToManyField(WeaponList, related_name='unit_template_weaponlists', default=None, blank=False, through='UnitTemplateWeaponList')
    skillLists = models.ManyToManyField(SkillList, related_name='unit_template_skilllists', default=None, blank=False, through='UnitTemplateSkillList')
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
    skills = models.ManyToManyField('Skill', default=None, through='UnitTemplateSkill', blank=True)

# modified from a 
class Unit(models.Model):
    class Meta:
        ordering = ['unitOrder']
    def __unicode__(self):
        return self.name
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
    creationTime = models.DateTimeField(auto_now_add=True, null=True)
    retiredTime = models.DateTimeField(null=True, blank=True)

    @property
    def isNew(self):
        return not self.team.playedSince(self.creationTime)
    def handsWorth(self):
        hands = 0
        # greg also check equipment...
        for item in self.unitWeapons.all():
            hands = hands + item.hands
        return hands
    def allowedWeapon(self, weapon):
        # check cost first
        if weapon.cost > self.team.coins:
            raise PermissionDenied("Cannot afford this item.")
        if weapon.hands + self.handsWorth() > 4:
            raise PermissionDenied("Cannot carry this many hands worth of equipment.")
        #greg once you implement injuries check here to see if they can use 2 handed weapons...

        # check if on one of our allowed weaponlists
        for aList in self.baseUnit.weaponLists.all():
            if weapon in aList.weapons.all():
                # check for limitations on mediveal weapons
                if weapon.medieval or not self.baseUnit.unittemplateweaponlist_set.get(unitTemplate=self.baseUnit, weaponLists=aList).medievalOnly:
                    return
                if not weapon.medieval and self.baseUnit.unittemplateweaponlist_set.get(unitTemplate=self.baseUnit, weaponLists=aList).medievalOnly:
                    raise PermissionDenied("May only use medieval weapons.")
        raise PermissionDenied("Illegal weapon choice")

    def addWeapon(self, weapon_id):
        weapon = Weapon.objects.get(id=weapon_id)
        print 'allowedWeaponed says',self.allowedWeapon(weapon)
        newWeapon = UnitWeapon(weapon=weapon, unit=self)
        newWeapon.save()
        self.team.coins = self.team.coins - weapon.cost
        self.team.save()
        return True

    @property
    def cost(self):
        cost = self.baseUnit.cost
        for item in self.unitWeapons.all():
            cost = cost +item.cost
        print cost
        return cost
    @property
    def medieval(self):
        for aList in self.baseUnit.unittemplateweaponlist_set.all():
            if aList.medievalOnly:
                return True
        return False   
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
    def weapons(self):
        return self.baseUnit.weapons.all() | self.unitWeapons.all()
    @property
    def skills(self):
        return self.baseUnit.skills.all()
    @property
    def baseWeapons(self):
        return self.baseUnit.weapons.all()
    @property
    def boughtWeapons(self):
        return self.unitWeapons.all()
    @property
    def gearAsString(self):
        rv =""
        for item in self.skills:
            if len(rv) > 0:
                rv = "%s, %s" % (rv, item)
            else:
                rv = rv + item.name
        for item in self.weapons:
            if len(rv) > 0:
                rv = "%s, %s" % (rv, item)
            else:
                rv = rv + item.name
        return rv
    # Is the unit missing the next game - MNG, captured, etc
    @property
    def isMNG(self):
        # greg filter based on freezeTime
        try:
            mostRecentGame = self.gameunit_set.filter(gameTeam__freezeTime=self.team.freezeTime).get()
            try:
                if mostRecentGame.injuries.penalty == Injury.MNG:
                    return True
            except AttributeError:
                pass
        except ObjectDoesNotExist:
            pass
        return False
    @property
    def isRetired(self):
        return self.retiredTime != None
    def fire(self):
        # Move all carried items to team store
        for item in self.unitweapon_set.all():
            item.unit = None
            item.team = self.team
            item.save()
        if self.isNew:
            self.team.adjustCoins(self.baseUnit.cost)
            self.delete()
        else: # Mark as retired
            self.retiredTime=datetime.datetime.now()
            self.save()

class Team(models.Model):
    name = models.CharField(max_length=100)
    faction = models.ForeignKey(Faction, default=None, blank=False)
    owner = models.ForeignKey(User, null=True, default=None, blank=True)
    coins = models.IntegerField(default=0)
    description = models.TextField(max_length=800, blank=True)
    store = models.ManyToManyField('Weapon', default=None, through='UnitWeapon', blank=True)
    freezeTime = models.DateTimeField(null=True, blank=True)
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
        self.adjustCoins(unitTemplate.cost * -1)
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
    # Return true if we have played a game since the passed time
    # Used to compare purchase times of equipment/injuries to the current freezeTime value
    def playedSince(self, time):
        if not self.freezeTime or time > self.freezeTime:
            return False
        return True
    # Update the currently tracked most recent game played time-stamp
    def updateFreezeTime(self, time):
        if not self.freezeTime or time > self.freezeTime:
            self.freezeTime = time
            self.save()
    @property
    def value(self):
        cost = self.coins
        for unit in self.units.all():
            cost = cost + unit.cost
        print 'greg modify team value to include stored equipment'
        return cost
    def adjustCoins(self, amount):
        self.coins = self.coins + amount
        self.save()
    @property
    def activeUnits(self):
        return Unit.objects.filter(team=self).exclude(~models.Q(retiredTime=None))
    @property
    def retiredUnits(self):
        return Unit.objects.filter(team=self).exclude(retiredTime=None)

class NewTeamForm(forms.ModelForm):
    campaignID = forms.IntegerField(label="", widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Team
        fields = ['name', 'coins', 'faction', 'description']

class TeamForm(forms.ModelForm):
        class Meta:
            model = Team
            fields = ['name', 'description']

class Game(models.Model):
    # Need to be able to support more than 2 teams
    teams = models.ManyToManyField('Team', related_name='game_for_team', default=None, blank=True, through='GameTeam')
    date = models.DateField(_("Date"),default=datetime.date.today)
    campaign = models.ForeignKey('Campaign', related_name='games', null=True, default=None)
    def canEdit(self, user):
        if user:
            for team in self.teams.all():
                if user == team.owner:
                    return True
            if user == self.campaign.owner:
                return True
        return False

class NewGameForm(forms.ModelForm):
    teamTwo = forms.ModelMultipleChoiceField(queryset=Team.objects.all())
    def __init__(self, campaign, *args, **kwargs):
        super(NewGameForm, self).__init__(*args, **kwargs)
        self.fields['teams'].queryset = campaign.teams.all()
        self.fields['teamTwo'].queryset = campaign.teams.all()

    class Meta:
        model = Game
        widgets = {
            'date': forms.DateInput(format='%m/%d/%Y'),
        }

# tracks a single teams involvement in a game. What players did they have at the time, what points did they score etc.
class GameTeam(models.Model):
    game = models.ForeignKey('Game', related_name="gameteam_set")
    team = models.ForeignKey('Team')
    victoryPoints = models.SmallIntegerField(default=0, blank=False)
    earnings = models.SmallIntegerField(default=0, blank=False)
    freezeTime = models.DateTimeField(null=True, blank=True)
    # units involved in this game
    units = models.ManyToManyField('Unit', related_name='game_for_unit', default=None, blank=True, through='GameUnit')
    # copies the units currently in the team into the 'units' field.
    # This is only performed the first time this method is called so that any later changes to team roster
    # will not then be reflected into this game if the game is updated.
    def freezeUnits(self):
        if self.units.count()>0:
            return
        for item in self.team.units.all():
            gameUnit = GameUnit(gameTeam=self, unit=item)
            gameUnit.save()
        self.freezeTime = datetime.datetime.now()
        self.save()
        # Update the team object's most recent game timestamp
        self.team.updateFreezeTime(self.freezeTime)

    def __unicode__(self):
        return u"Team: %s, VP: %s, Winnings: %s" % (self.team, self.victoryPoints, self.earnings)

# tracks a single units involvement in a game. Did they get any injuries, any new skills, etc?
class GameUnit(models.Model):
    gameTeam = models.ForeignKey(GameTeam)
    unit = models.ForeignKey('Unit')
    skills = models.ForeignKey('Skill', related_name='game_unit_for_skill', default=None, blank=True, null=True)
    injuries = models.ForeignKey('Injury', related_name='game_unit_for_injury', default=None, blank=True, null=True)
    def __unicode__(self):
        return u"%s" % self.unit.name

class GameUnitLine(forms.Form):
    # greg the below does not work for me, it produces
    # gameForm exception:  Caught TypeError while rendering: 'ManyRelatedManager' object is not iterable
    # I need ModelMultipleChoiceField to be able to add multiple skills to a model in a single game
    # However, I'm leaving this for now. I'm beginning to wonder if this is a django regression.
    #skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all(), widget=forms.CheckboxSelectMultiple())
    skills = forms.ModelChoiceField(Skill.objects.all())
    injuries = forms.ModelChoiceField(Injury.objects.all())
    name = forms.CharField()
    summary = forms.CharField()

class GameFormLine(forms.ModelForm):
    team = forms.CharField()
    teamID = forms.IntegerField(widget=forms.widgets.HiddenInput())

    class Meta:
        model = GameTeam
        fields = ['team','victoryPoints','earnings']

#class GameFormLine(forms.Form):
#    team = forms.CharField()
#    victoryPoints = forms.IntegerField()
#    earnings = forms.IntegerField()
#    teamID = forms.IntegerField(widget=forms.widgets.HiddenInput())
