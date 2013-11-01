# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'GameUnit.retain'
        db.add_column('eotd_gameunit', 'retain',
                      self.gf('django.db.models.fields.SmallIntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'GameUnit.retain'
        db.delete_column('eotd_gameunit', 'retain')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'eotd.campaign': {
            'Meta': {'object_name': 'Campaign'},
            'admins': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'related_name': "'campaign_admin_table'", 'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'applicants': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['auth.User']", 'symmetrical': 'False', 'through': "orm['eotd.CampaignApplicant']", 'blank': 'True'}),
            'coins': ('django.db.models.fields.IntegerField', [], {'default': '150'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '800', 'blank': 'True'}),
            'exclusive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'campaigns'", 'null': 'True', 'to': "orm['auth.User']"}),
            'players': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'related_name': "'campaign_player_table'", 'blank': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'secret': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'teams': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'related_name': "'campaign_team_table'", 'blank': 'True', 'symmetrical': 'False', 'to': "orm['eotd.Team']"})
        },
        'eotd.campaignapplicant': {
            'Meta': {'object_name': 'CampaignApplicant'},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eotd.Campaign']"}),
            'creationTime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'eotd.faction': {
            'Meta': {'object_name': 'Faction'},
            'alignment': ('django.db.models.fields.SmallIntegerField', [], {'default': '2'}),
            'arcaneMod': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'bravadoMod': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'combatMod': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'cost': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'marksmanshipMod': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'eotd.game': {
            'Meta': {'object_name': 'Game'},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'games'", 'null': 'True', 'to': "orm['eotd.Campaign']"}),
            'date': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'teams': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'game_for_team'", 'default': 'None', 'to': "orm['eotd.Team']", 'through': "orm['eotd.GameTeam']", 'blank': 'True', 'symmetrical': 'False'})
        },
        'eotd.gameteam': {
            'Meta': {'object_name': 'GameTeam'},
            'earnings': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'freezeTime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'game': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gameteam_set'", 'to': "orm['eotd.Game']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'influenceBought': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'influenceSpent': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eotd.Team']"}),
            'units': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'game_for_unit'", 'default': 'None', 'to': "orm['eotd.Unit']", 'through': "orm['eotd.GameUnit']", 'blank': 'True', 'symmetrical': 'False'}),
            'victoryPoints': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'})
        },
        'eotd.gameunit': {
            'Meta': {'ordering': "['unit__unitOrder']", 'object_name': 'GameUnit'},
            'gameTeam': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eotd.GameTeam']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'injuries': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['eotd.Injury']", 'symmetrical': 'False', 'through': "orm['eotd.GameUnitInjury']", 'blank': 'True'}),
            'retain': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'skills': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'game_unit_for_skill'", 'null': 'True', 'blank': 'True', 'to': "orm['eotd.Skill']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eotd.Unit']"})
        },
        'eotd.gameunitinjury': {
            'Meta': {'object_name': 'GameUnitInjury'},
            'date': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'doctor': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'gameUnit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eotd.GameUnit']"}),
            'healed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'injury': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eotd.Injury']"})
        },
        'eotd.injury': {
            'Meta': {'object_name': 'Injury'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'microName': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'penalty': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'shortName': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'eotd.skill': {
            'Meta': {'ordering': "['name']", 'object_name': 'Skill'},
            'arcanePower': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'statMod': ('django.db.models.fields.SmallIntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'statModAmount': ('django.db.models.fields.SmallIntegerField', [], {'default': '0', 'blank': 'True'})
        },
        'eotd.skilllist': {
            'Meta': {'object_name': 'SkillList'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'skills': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'related_name': "'skill_lists'", 'symmetrical': 'False', 'to': "orm['eotd.Skill']"})
        },
        'eotd.team': {
            'Meta': {'object_name': 'Team'},
            'coins': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '800', 'blank': 'True'}),
            'faction': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['eotd.Faction']"}),
            'freezeTime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'influence': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'retired': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'store': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['eotd.Weapon']", 'symmetrical': 'False', 'through': "orm['eotd.UnitWeapon']", 'blank': 'True'})
        },
        'eotd.unit': {
            'Meta': {'ordering': "['unitOrder']", 'object_name': 'Unit'},
            'baseUnit': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['eotd.UnitTemplate']"}),
            'creationTime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'faction': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'faction_units'", 'to': "orm['eotd.Faction']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'retiredTime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'units'", 'to': "orm['eotd.Team']"}),
            'unitLeaderOverride': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'unitName': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'unitOrder': ('django.db.models.fields.SmallIntegerField', [], {'default': '999'}),
            'unitWeapons': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['eotd.Weapon']", 'symmetrical': 'False', 'through': "orm['eotd.UnitWeapon']", 'blank': 'True'})
        },
        'eotd.unittemplate': {
            'Meta': {'object_name': 'UnitTemplate'},
            'animal': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'arcane': ('django.db.models.fields.SmallIntegerField', [], {'default': '3'}),
            'attacks': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'bravado': ('django.db.models.fields.SmallIntegerField', [], {'default': '4'}),
            'combat': ('django.db.models.fields.SmallIntegerField', [], {'default': '3'}),
            'comesWith': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['eotd.UnitTemplate']", 'symmetrical': 'False', 'blank': 'True'}),
            'cost': ('django.db.models.fields.SmallIntegerField', [], {'default': '100'}),
            'faction': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'related_name': "'unit_templates'", 'symmetrical': 'False', 'to': "orm['eotd.Faction']"}),
            'fortitude': ('django.db.models.fields.SmallIntegerField', [], {'default': '3'}),
            'gent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'gentRetentionCost': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'hero': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leader': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'marksmanship': ('django.db.models.fields.SmallIntegerField', [], {'default': '3'}),
            'maxCount': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'movement': ('django.db.models.fields.SmallIntegerField', [], {'default': '4'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'notForPurchase': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'skillLists': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'related_name': "'unit_template_skilllists'", 'symmetrical': 'False', 'through': "orm['eotd.UnitTemplateSkillList']", 'to': "orm['eotd.SkillList']"}),
            'skills': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['eotd.Skill']", 'symmetrical': 'False', 'through': "orm['eotd.UnitTemplateSkill']", 'blank': 'True'}),
            'specialType': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'strength': ('django.db.models.fields.SmallIntegerField', [], {'default': '3'}),
            'supernatural': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'weaponLists': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'related_name': "'unit_template_weaponlists'", 'symmetrical': 'False', 'through': "orm['eotd.UnitTemplateWeaponList']", 'to': "orm['eotd.WeaponList']"}),
            'weapons': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['eotd.Weapon']", 'symmetrical': 'False', 'through': "orm['eotd.UnitTemplateWeapon']", 'blank': 'True'}),
            'wounds': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        'eotd.unittemplateskill': {
            'Meta': {'object_name': 'UnitTemplateSkill'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'skill': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eotd.Skill']"}),
            'unitTemplate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eotd.UnitTemplate']"})
        },
        'eotd.unittemplateskilllist': {
            'Meta': {'object_name': 'UnitTemplateSkillList'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'skillLists': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eotd.SkillList']"}),
            'special': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'unitTemplate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eotd.UnitTemplate']"})
        },
        'eotd.unittemplateweapon': {
            'Meta': {'object_name': 'UnitTemplateWeapon'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'unitTemplate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eotd.UnitTemplate']"}),
            'weapon': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eotd.Weapon']"})
        },
        'eotd.unittemplateweaponlist': {
            'Meta': {'object_name': 'UnitTemplateWeaponList'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medievalOnly': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'unitTemplate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eotd.UnitTemplate']"}),
            'weaponLists': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eotd.WeaponList']"})
        },
        'eotd.unitweapon': {
            'Meta': {'object_name': 'UnitWeapon'},
            'creationTime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nameOverride': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eotd.Team']", 'null': 'True'}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eotd.Unit']", 'null': 'True'}),
            'weapon': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eotd.Weapon']"})
        },
        'eotd.weapon': {
            'Meta': {'object_name': 'Weapon'},
            'ccw': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cost': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'hands': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'longRange': ('django.db.models.fields.SmallIntegerField', [], {'default': '0', 'blank': 'True'}),
            'medieval': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mediumRange': ('django.db.models.fields.SmallIntegerField', [], {'default': '0', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'shortRange': ('django.db.models.fields.SmallIntegerField', [], {'default': '0', 'blank': 'True'}),
            'strength': ('django.db.models.fields.SmallIntegerField', [], {'default': '5'}),
            'weapon': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'eotd.weaponlist': {
            'Meta': {'object_name': 'WeaponList'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'weapons': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'related_name': "'weapon_lists'", 'symmetrical': 'False', 'to': "orm['eotd.Weapon']"})
        }
    }

    complete_apps = ['eotd']