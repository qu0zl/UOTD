from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
import math #used for ceil
import datetime
# no longer needed - from itertools import chain

#import profiles.models

CHOICE_NO = (0, _('No'))
CHOICE_YES = (1, _('Yes'))

YES_NO_CHOICES = (
    CHOICE_NO, CHOICE_YES )

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
        return  unicode(self.name)
    def isOwner(self, user):
        return self.owner == user
    def isAdmin(self, user):
        if user == self.owner or user in self.admins.all():
            return True
        else:
            return False
    def teamsByStanding(self):
        return sorted(self.teams.all(), key=lambda a: a.value, reverse=True)
    # Delete the campaign but do not delete constituent games or it will affect team statuses
    def deleteCampaign(self, user):
        # Only the campaign owner may delete it. Not an ordinary admin.
        if not self.isOwner(user):
            return False
        self.delete()
        return True
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
        if self.exclusive:
            if team.campaign_team_table.count() > 0:
                raise PermissionDenied("This campaign does not allow a team to be in other campaigns. You must remove this team from any other campaigns in order to join.")
        elif team.campaign_team_table.filter(exclusive=True).exists():
            raise PermissionDenied("This team is already a member of a campaign that does not allow its teams to be in multiple campaigns. You must remove this team from that campaign before you can join this one.")
        self.teams.add(team)
        self.save()

class CampaignForm(forms.ModelForm):
        class Meta:
            model = Campaign
            fields = ['name', 'coins', 'secret', 'description']

SPECIALIST=1
ALLOW_SPECIALIST=2
SPECIALIST_CHOICES = (
    (0, _('---')),
    (SPECIALIST, _('Specialist')),
    (ALLOW_SPECIALIST, _('Allow Specialist'))
)

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
    (-11, _("Model Strength - 1")),
    (-2, _("Model Strength + 2")),
    (-1, _("Model Strength + 1")),
    (0, _("Model Strength")),
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
    OTHER=0
    MNG=1
    MINUS_STRENGTH=2
    MINUS_FORTITUDE=3
    MINUS_MOVEMENT=4
    MINUS_BRAVADO=5
    ARRESTED=8
    CAPTURED=9
    DEAD=10
    INJURY_PENALTIES = (
        (OTHER, _('----')),
        (MNG,  _('MNG')),
        (MINUS_STRENGTH,  _('-1 Strength')),
        (MINUS_FORTITUDE,  _('-1 Fortitude')),
        (MINUS_MOVEMENT,  _('-1 Movement')),
        (MINUS_BRAVADO, _('-1 Bravado')),
        (ARRESTED, _('Arrested')),
        (CAPTURED, _('Captured')),
        (DEAD, _('Dead')),
    )
    def __unicode__(self):
        return self.name
    name = models.CharField(max_length=100)
    # abbreviated name used for print view
    shortName = models.CharField(max_length=100, blank=True, null=True)
    # Used for team edit view. So needs to be 1 letter long or so.
    microName = models.CharField(max_length=10, blank=True, null=True)
    penalty = models.SmallIntegerField(choices=INJURY_PENALTIES, default=1, blank=False)
    @property
    def abbreviation(self):
        if self.shortName:
            return self.shortName
        return self.name
    @property
    def micro(self):
        if self.microName:
            return self.microName
        return '?'


class GameUnitInjury(models.Model):
    DOCTOR_CHOICES=(
        (0, '----'),
        (1, _('Charlatan')),
        (2, _('Local GP')),
        (3, _('Harley Street specialist')),
        (4, _('Free/Healing Hands')),
    )
    DOCTOR_COSTS={
        0:0,
        1:4,
        2:8,
        3:12,
        4:0
    }
    healed = models.BooleanField(default=False)
    doctor = models.SmallIntegerField(choices=DOCTOR_CHOICES, default=0, blank=False)
    injury = models.ForeignKey(Injury)
    gameUnit = models.ForeignKey('GameUnit')
    date = models.DateField(_("Date"),default=None, blank=True, null=True)
    def __unicode__(self):
        return u'%s: %shealed' % (self.injury.name, '' if self.healed else 'not ')
    def cost(self, doctorType=None):
        if not doctorType:
            doctorType=self.doctor
        doctorCost=GameUnitInjury.DOCTOR_COSTS[doctorType]
        # Check if we should get the 'Sons of the Empire' specialist doctor discount.
        if doctorType == 3 and self.gameUnit.unit.team.faction.name.lower()=='sons of the empire':
            doctorCost = doctorCost - 2

        return doctorCost
    @property
    def doctorString(self):
        return GameUnitInjury.DOCTOR_CHOICES[self.doctor][1]

class Skill(models.Model):
    STRENGTH=1
    FORTITUDE=2
    MARKSMANSHIP=3
    MOVEMENT=4
    ATTACKS=5
    WOUNDS=6
    BRAVADO=7
    ARCANE=8
    COMBAT=9
    STAT_MODS = (
        (STRENGTH, _('Strength')),
        (FORTITUDE, _('Fortitude')),
        (MARKSMANSHIP, _('Marksmanship')),
        (MOVEMENT, _('Movement')),
        (ATTACKS, _('Attacks')),
        (WOUNDS, _('Wounds')),
        (BRAVADO, _('Bravado')),
        (ARCANE, _('Arcane')),
        (COMBAT, _('Combat')),
    )
    class Meta:
        ordering=['name']
    def __unicode__(self):
        return self.name
    name = models.CharField(max_length=100)
    arcanePower = models.BooleanField(default=False)
    statMod = models.SmallIntegerField(choices=STAT_MODS, default=None, blank=True, verbose_name="Unit stat modified", null=True)
    statModAmount = models.SmallIntegerField(choices=tuple((x,x) for x in range(-1, 2)), default=0, blank=True, verbose_name="Unit stat modification amount")

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
    def strengthString(self):
        for x,y in WEAPON_STRENGTH_CHOICES:
            if x == self.strength:
                return unicode(y)
        return ''

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
    @property
    def availableUnitTemplates(self):
        # exclude UnitTemplates which have notForPurchase set to True
        return UnitTemplate.objects.filter(faction=self,notForPurchase=False)

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
        team = self.getTeam
        if not self.isNew:
                team.coins = team.coins + (self.weapon.cost/2)
        else:
            team.coins = team.coins + self.weapon.cost
        team.save()
        self.delete()
    @property
    def getTeam(self):
        try:
            return self.unit.team
        except AttributeError as e:
            return self.team
    @property
    def isNew(self):
        return not self.getTeam.playedSince(self.creationTime)
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
    # If this unit type should not be available for purchase. May be used for units that come free with others.
    notForPurchase = models.BooleanField(default=False)
    # If this unit type is a Gentleman & Jackanape special character
    gent = models.BooleanField(default=False)
    # If this model is a Gentleman & Jackanape then this is the reduced retention cost.
    gentRetentionCost = models.SmallIntegerField(default=0, blank=False)

    # Used to point to another UnitTemplate that should come free with this template.
    comesWith = models.ManyToManyField('UnitTemplate', default=None, blank=True)

    specialType = models.SmallIntegerField(choices=SPECIALIST_CHOICES,default=0,blank=False)
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
    @property
    def recentlyRetired(self):
        if self.retiredTime and not self.team.playedSince(self.retiredTime):
            return True
        return False
    def handsWorth(self):
        hands = 0
        # greg also check equipment...
        for item in self.unitWeapons.all():
            hands = hands + item.hands
        return hands
    def allowedWeapon(self, weapon, isPurchase=True):
        # check cost first but only if this is a purchase
        if isPurchase and weapon.cost > self.team.coins:
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

    def unitSpecificWeaponLists(self):
        '''Return weaponLists from the unitTemplate but filter out any illegal choices based on medieval, CCW etc'''
        rv = []
        try:
            UnitTemplateWeaponList
            for utwl in UnitTemplateWeaponList.objects.filter(unitTemplate=self.baseUnit):
                item = dict()
                item['name']=utwl.weaponLists.name
                item['id']=utwl.weaponLists.id
                weapons = utwl.weaponLists.weapons.all()
                if utwl.medievalOnly:
                    weapons = weapons.filter(medieval=True)
                item['weapons']=weapons
                rv.append(item)
        except Exception as e:
            print 'unitSpecificWeaponLists exception', e
        return rv

    def heal(self, injury_id, doctor):
        injury = GameUnitInjury.objects.get(id=injury_id, gameUnit__unit=self, healed=False)
        cost = injury.cost(doctor)
        if cost > self.team.coins:
            return False
        injury.healed = True
        injury.doctor = doctor
        injury.date = datetime.datetime.today()
        self.team.adjustCoins(cost * -1)
        injury.save()
    # Used to un-retire Gentlemen & Jackanapes without any injuries
    def restoreVitality(self):
        try:
            GameUnitInjury.objects.get(gameUnit__unit=self).delete()
        except GameUnitInjury.DoesNotExist:
            pass
        self.retiredTime=None
        self.save()

    def clearMNG(self):
        for gameunit in self.gameunit_set.filter(gameunitinjury__healed=False, gameunitinjury__injury__penalty=Injury.MNG):
            gameunitinjury = gameunit.gameunitinjury_set.get()
            gameunitinjury.healed=True
            gameunitinjury.save()

    def addWeapon(self, weapon_id):
        weapon = Weapon.objects.get(id=weapon_id)
        self.allowedWeapon(weapon)
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

        # Add cost of any bought skills
        cost = cost + (self.gameunit_set.exclude(skills=None).count() * 10)

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
        return self.moddedStat(self.baseUnit.combat+self.faction.combatMod, None, Skill.COMBAT)
    @property
    def marksmanship(self):
        return self.moddedStat(self.baseUnit.marksmanship+self.faction.marksmanshipMod, None, Skill.MARKSMANSHIP)
    def moddedStat(self, baseStat, injuryType=None, statType=None):
        modded = baseStat - self.injuryCount(injuryType) + self.statModCount(statType)
        if modded < baseStat:
            return "%s*" % modded
        elif modded > baseStat:
            return "%s^" % modded
        return modded
    @property
    def strength(self):
        return self.moddedStat(self.baseUnit.strength, Injury.MINUS_STRENGTH, Skill.STRENGTH)
    @property
    def fortitude(self):
        return self.moddedStat(self.baseUnit.fortitude, Injury.MINUS_FORTITUDE, Skill.FORTITUDE)
    @property
    def attacks(self):
        # need to handle teeth and claws and multiple weapons in general.
        return self.moddedStat(self.baseUnit.attacks, None, Skill.ATTACKS)
    @property
    def wounds(self):
        return self.moddedStat(self.baseUnit.wounds, None, Skill.WOUNDS)
    @property
    def bravado(self):
        return self.moddedStat(self.baseUnit.bravado+self.faction.bravadoMod, Injury.MINUS_BRAVADO, Skill.BRAVADO)
    @property
    def arcane(self):
        return self.moddedStat(self.baseUnit.arcane+self.faction.arcaneMod, None, Skill.ARCANE) 
    @property
    def weapons(self):
        # Don't be clever and use the below to save a DB call.
        # By adding two querysets with '|' the queries are combined before
        # the DB call is made, and we end up getting many duplicate entries.
        # return self.baseUnit.weapons.all() | self.unitWeapons.all()
        return list(self.baseWeapons) + list(self.unitWeapons.all())
    @property
    def skills(self):
        # All skills from the base template or purchased
        return self.baseUnit.skills.all() | Skill.objects.filter(game_unit_for_skill__unit=self)
    @property
    def baseWeapons(self):
        return self.baseUnit.weapons.all()
    @property
    def boughtWeapons(self):
        return UnitWeapon.objects.filter(unit=self)
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
    @property
    def injuries(self):
        return self.gameunit_set.filter(gameunitinjury__healed=False).order_by('gameunitinjury__injury')
    @property
    def injuriesExMNG(self):
        return self.injuries.exclude(gameunitinjury__injury__penalty=Injury.MNG)
    @property
    def injuriesAsString(self):
        rv =""
        first = True

        for item in self.injuries:
            if not first:
                rv = "%s, %s" % (rv, item.injuries.get().abbreviation)
            else:
                rv = rv + item.injuries.get().abbreviation
                first = False
        return rv
    # Is the unit missing the next game - MNG, captured, etc
    @property
    def isMNG(self):
        return self.injuryCount(Injury.MNG) > 0
    def statModCount(self, statType):
        if not statType:
            return 0
        try:
            # Working on assumption that all stat mods are only +1, so will return count rather than slower process of dereferencing
            # and summing the mods
            return self.gameunit_set.filter(skills__statMod=statType).count()
        except ObjectDoesNotExist:
            return 0
    def injuryCount(self, injuryType):
        if not injuryType:
            return 0
        try:
            return self.gameunit_set.filter(gameunitinjury__healed=False, gameunitinjury__injury__penalty=injuryType).count()
        except ObjectDoesNotExist:
            return 0
    @property
    def isDead(self):
        return self.injuryCount(Injury.DEAD) > 0
    @property
    def isRetired(self):
        return self.retiredTime != None
    def fire(self):
        if not self.baseUnit.gent:
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
# Manager for Team object. Used to exclude retired teams by default
class TeamManager(models.Manager):
    def get_query_set(self):
        return super(TeamManager, self).get_query_set().exclude(retired=True)

class Team(models.Model):
    name = models.CharField(max_length=100)
    faction = models.ForeignKey(Faction, default=None, blank=False)
    owner = models.ForeignKey(User, null=True, default=None, blank=True)
    coins = models.IntegerField(default=0)
    influence = models.IntegerField(default=0)
    description = models.TextField(max_length=800, blank=True)
    store = models.ManyToManyField('Weapon', default=None, through='UnitWeapon', blank=True)
    # Cannot delete a team that has played games
    # So instead will mark it as retired and then no longer display it.
    retired = models.BooleanField(default=False, blank=True)
    freezeTime = models.DateTimeField(null=True, blank=True)
    objects = TeamManager() # Exclude retired teams by default.
    all_objects = models.Manager() # The standard manager. Include all teams.

    def __unicode__(self):
        return self.name
    @property
    def availableUnitTemplates(self):
        # Same as the faction version of this except it excludes any Gentlemen & Jackanapes that 
        # are already part of the team
        return self.faction.availableUnitTemplates.filter(~models.Q(unit__team=self,gent=True)).order_by('-gent')
    # Does this Team have a leader model
    def hasLeader(self):
        return self.activeUnits.filter(models.Q(baseUnit__leader=True) | models.Q(unitLeaderOverride=True)).count() > 0
    @property
    def hasPlayedGames(self):
        return GameTeam.objects.filter(team=self).exists()
    # If this team has played games then we will only flag them as retired rather than actually delete them
    def deleteOrRetire(self):
        if self.hasPlayedGames:
            self.retired = True
            self.save()
        else:
            self.units.all().delete()
            self.delete()
    def canHire(self, unitTemplate):
        # Can we afford it
        if unitTemplate.cost > self.coins:
            raise PermissionDenied(_("Unable to afford this unit."))
        # Not allowed two leaders
        if unitTemplate.leader and self.hasLeader():
            raise PermissionDenied(_("Only one leader model allowed."))
        # Only allowed have 1/3rd (rounding-up) of models be heroes
        if unitTemplate.hero:
            heroCount = self.activeUnits.filter(baseUnit__hero=True).count()
            plebCount = self.activeUnits.filter(baseUnit__hero=False).count()
            maxHeroCount = math.ceil(plebCount/2.0)
            if maxHeroCount == 0:
                maxHeroCount = 1
            if heroCount+1 > maxHeroCount:
                raise PermissionDenied(_("Would exceed 1/3rd heroes faction composition limit."))
        # Cannot have more specialists than it has specialist-allowing models
        if unitTemplate.specialType == SPECIALIST:
            specAllowCount = self.activeUnits.filter(baseUnit__specialType=ALLOW_SPECIALIST).count()
            specCount = self.activeUnits.filter(baseUnit__specialType=SPECIALIST).count()
            if specCount+1 > specAllowCount:
                raise PermissionDenied(_("Cannot have more specialists than specialist-allowing models."))
        # Not allowed exceed maximum number of certain models
        if unitTemplate.maxCount > 0:
            if self.units.filter(baseUnit=unitTemplate).count() >= unitTemplate.maxCount:
                raise PermissionDenied(_("Would exceed maximum number of this unit type allowed."))
        return True
    def hire(self, unitTemplate, free=False):
        # will raise exception carrying message explaining the problem.
        if not free and not self.canHire(unitTemplate):
            raise PermissionDenied('Unable to hire this unit.')
        unit = Unit(faction=self.faction, baseUnit=unitTemplate, team=self, unitOrder=self.units.count()+1)
        unit.save()
        if not free:
            self.adjustCoins(unitTemplate.cost * -1)
        for minion in unitTemplate.comesWith.all():
            minion = Unit(faction=self.faction, baseUnit=unitTemplate.comesWith.all()[0], team=self, unitOrder=self.units.count()+1)
            minion.save()
        return self.coins
    def releaseGent(self, id, gameUnit):
        try:
            unitTemplate = UnitTemplate.objects.get(id=id)
            for unit in self.activeUnits.filter(baseUnit__id=id, baseUnit__gent=True):
                print 'Deleting G&J from team'
                unit.fire()
            for minion in unitTemplate.comesWith.all():
                for unit in self.activeUnits.filter(baseUnit__id=minion.id, baseUnit__gent=True):
                    print 'Deleting G&J minion from team'
                    unit.fire()

            # Refund money if they were previously retained
            if gameUnit.retain == gameUnit.RETAINED:
                print 'increasing team coins by', unitTemplate.gentRetentionCost
                self.adjustCoins(unitTemplate.gentRetentionCost)

            gameUnit.retain = gameUnit.RELEASED
            gameUnit.save()

        except Exception as e:
            print 'releaseGent exception %s: %s' % (id, e)
    def retainGent(self, id, gameUnit):
        try:
            unitTemplate = UnitTemplate.objects.get(id=id)
            if self.activeUnits.filter(baseUnit__id=id).count() == 0:
                print 'adding G&J to team as missing during retention'
                # Bring back the G&J
                self.allInactiveUnits.filter(baseUnit__id=id)[0].restoreVitality()

            for minion in unitTemplate.comesWith.all():
                if self.activeUnits.filter(baseUnit__id=minion.id).count() == 0:
                    print 'Adding G&J minion as missing during retention'
                    self.allInactiveUnits.filter(baseUnit__id=minion.id)[0].restoreVitality()

            if gameUnit.retain != gameUnit.RETAINED:
                print 'reducing team coins by', unitTemplate.gentRetentionCost
                self.adjustCoins(unitTemplate.gentRetentionCost * -1)
                gameUnit.retain = gameUnit.RETAINED
                gameUnit.save()
        except Exception as e:
            print 'retainGent exception %s: %s' % (id, e)
    def reorder(self, order):
        try:
            for i, item in enumerate(order,1):
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
    def storeValue(self):
        value = 0
        for entry in UnitWeapon.objects.filter(team=self, unit=None):
            value = value+entry.weapon.cost
        return value
    @property
    def value(self):
        cost = self.coins + self.faction.cost
        for unit in self.activeUnitsNoMNG:
            cost = cost + unit.cost
        return cost + self.storeValue + (self.influence * 5)
    def adjustCoins(self, amount):
        self.coins = self.coins + amount
        self.save()
    @property
    def activeUnits(self):
        # exclude retired and dead models
        return Unit.objects.filter(team=self).exclude(~models.Q(retiredTime=None)).filter(~models.Q(gameunit__injuries__penalty=Injury.DEAD, gameunit__gameunitinjury__healed=False))
    # return the list of alive/non-retired units, excluding any that are miss next game
    @property
    def activeUnitsNoMNG(self):
        return self.activeUnits.filter(~models.Q(gameunit__injuries__penalty=Injury.MNG, gameunit__gameunitinjury__healed=False))
    def clearMNG(self):
        for item in self.activeUnits.filter(models.Q(gameunit__injuries__penalty=Injury.MNG, gameunit__gameunitinjury__healed=False)):
            item.clearMNG()
    @property
    def inactiveUnits(self):
        return (self.retiredUnits | self.deadUnits).distinct()
    @property
    def allInactiveUnits(self): # DOES include Gentlemen & Jackanapes
        return (self.allRetiredUnits | self.deadUnits).distinct()
    @property
    def retiredUnits(self): # does not include Gentlemen & Jackanapes
        return Unit.objects.filter(team=self).exclude(retiredTime=None).exclude(baseUnit__gent=True)
    @property
    def allRetiredUnits(self): # DOES include Gentlemen & Jackanapes
        return Unit.objects.filter(team=self).exclude(retiredTime=None)
    @property
    def deadUnits(self):
        return Unit.objects.filter(team=self).filter(models.Q(gameunit__injuries__penalty=Injury.DEAD, gameunit__gameunitinjury__healed=False))
    # List of weapons carried by active units
    @property
    def activeWeapons(self):
        weapons = set()
        for unit in self.activeUnits:
            for weapon in unit.weapons:
                if weapon.weapon:
                    weapons.add(weapon)
        return weapons

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
    def deleteGame(self):
        for gameTeam in self.gameteam_set.all():
            gameTeam.gameunit_set.all().delete()
            # Remove their winnings
            gameTeam.team.adjustCoins(gameTeam.earnings * -1)
            gameTeam.delete()
        self.delete()
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
    influenceSpent = models.SmallIntegerField(default=0, blank=False)
    influenceBought = models.SmallIntegerField(default=0, blank=False)
    freezeTime = models.DateTimeField(null=True, blank=True)
    # units involved in this game
    units = models.ManyToManyField('Unit', related_name='game_for_unit', default=None, blank=True, through='GameUnit')
    # copies the units currently in the team into the 'units' field.
    # This is only performed the first time this method is called so that any later changes to team roster
    # will not then be reflected into this game if the game is updated.
    def freezeUnits(self):
        if self.units.count()>0:
            return
        for item in self.team.activeUnitsNoMNG.all():
            gameUnit = GameUnit(gameTeam=self, unit=item)
            gameUnit.save()
        self.freezeTime = datetime.datetime.now()
        # remove any MNG status
        self.team.clearMNG()
        self.save()
        # Update the team object's most recent game timestamp
        self.team.updateFreezeTime(self.freezeTime)

    def __unicode__(self):
        return u"Team: %s, VP: %s, Winnings: %s" % (self.team, self.victoryPoints, self.earnings)

# tracks a single units involvement in a game. Did they get any injuries, any new skills, etc?
class GameUnit(models.Model):
    UNSET=0
    RETAINED=1
    RELEASED=2
    RETAIN_CHOICES = ( (UNSET,'Unset'), (RETAINED,'Retained'), (RELEASED,'Released') )

    class Meta:
        ordering = ['unit__unitOrder']
    gameTeam = models.ForeignKey(GameTeam)
    unit = models.ForeignKey('Unit')
    skills = models.ForeignKey('Skill', related_name='game_unit_for_skill', default=None, blank=True, null=True)
    injuries = models.ManyToManyField('Injury', through="GameUnitInjury", default=None, blank=True)
    # If this model is a G&J, then did we retain them.
    retain = models.SmallIntegerField(choices=RETAIN_CHOICES, default=0, blank=False)
    def __unicode__(self):
        return u"%s" % self.unit.name

class GameUnitLine(forms.Form):
    # greg the below does not work for me, it produces
    # gameForm exception:  Caught TypeError while rendering: 'ManyRelatedManager' object is not iterable
    # I need ModelMultipleChoiceField to be able to add multiple skills to a model in a single game
    # However, I'm leaving this for now. I'm beginning to wonder if this is a django regression.
    #skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all(), widget=forms.CheckboxSelectMultiple())
    # Skill choices need to be limited based on the unit being displayed
    skills = forms.ModelChoiceField(Skill.objects.all())
    injuries = forms.ModelChoiceField(Injury.objects.all())
    name = forms.CharField()
    summary = forms.CharField()

class GameGentLine(forms.Form):
    name = forms.CharField()
    rent = forms.IntegerField()
    retain = forms.ChoiceField(choices=YES_NO_CHOICES, required=True, label=_("Retain?"))

class GameFormLine(forms.ModelForm):
    team = forms.CharField()
    teamID = forms.IntegerField(widget=forms.widgets.HiddenInput())

    class Meta:
        model = GameTeam
        fields = ['team','victoryPoints','earnings', 'influenceSpent', 'influenceBought']
