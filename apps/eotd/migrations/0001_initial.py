# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CampaignApplicant'
        db.create_table('eotd_campaignapplicant', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('campaign', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eotd.Campaign'])),
            ('creationTime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
        ))
        db.send_create_signal('eotd', ['CampaignApplicant'])

        # Adding model 'Campaign'
        db.create_table('eotd_campaign', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='campaigns', null=True, to=orm['auth.User'])),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=800, blank=True)),
            ('coins', self.gf('django.db.models.fields.IntegerField')(default=150)),
            ('exclusive', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('secret', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal('eotd', ['Campaign'])

        # Adding M2M table for field admins on 'Campaign'
        db.create_table('eotd_campaign_admins', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('campaign', models.ForeignKey(orm['eotd.campaign'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('eotd_campaign_admins', ['campaign_id', 'user_id'])

        # Adding M2M table for field players on 'Campaign'
        db.create_table('eotd_campaign_players', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('campaign', models.ForeignKey(orm['eotd.campaign'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('eotd_campaign_players', ['campaign_id', 'user_id'])

        # Adding M2M table for field teams on 'Campaign'
        db.create_table('eotd_campaign_teams', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('campaign', models.ForeignKey(orm['eotd.campaign'], null=False)),
            ('team', models.ForeignKey(orm['eotd.team'], null=False))
        ))
        db.create_unique('eotd_campaign_teams', ['campaign_id', 'team_id'])

        # Adding model 'SkillList'
        db.create_table('eotd_skilllist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('eotd', ['SkillList'])

        # Adding M2M table for field skills on 'SkillList'
        db.create_table('eotd_skilllist_skills', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('skilllist', models.ForeignKey(orm['eotd.skilllist'], null=False)),
            ('skill', models.ForeignKey(orm['eotd.skill'], null=False))
        ))
        db.create_unique('eotd_skilllist_skills', ['skilllist_id', 'skill_id'])

        # Adding model 'WeaponList'
        db.create_table('eotd_weaponlist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('eotd', ['WeaponList'])

        # Adding M2M table for field weapons on 'WeaponList'
        db.create_table('eotd_weaponlist_weapons', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('weaponlist', models.ForeignKey(orm['eotd.weaponlist'], null=False)),
            ('weapon', models.ForeignKey(orm['eotd.weapon'], null=False))
        ))
        db.create_unique('eotd_weaponlist_weapons', ['weaponlist_id', 'weapon_id'])

        # Adding model 'Injury'
        db.create_table('eotd_injury', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('penalty', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
        ))
        db.send_create_signal('eotd', ['Injury'])

        # Adding model 'Skill'
        db.create_table('eotd_skill', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('arcanePower', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('eotd', ['Skill'])

        # Adding model 'Weapon'
        db.create_table('eotd_weapon', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('weapon', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('cost', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('hands', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('ccw', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('medieval', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('shortRange', self.gf('django.db.models.fields.SmallIntegerField')(default=0, blank=True)),
            ('mediumRange', self.gf('django.db.models.fields.SmallIntegerField')(default=0, blank=True)),
            ('longRange', self.gf('django.db.models.fields.SmallIntegerField')(default=0, blank=True)),
            ('strength', self.gf('django.db.models.fields.SmallIntegerField')(default=5)),
        ))
        db.send_create_signal('eotd', ['Weapon'])

        # Adding model 'Faction'
        db.create_table('eotd_faction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('alignment', self.gf('django.db.models.fields.SmallIntegerField')(default=2)),
            ('cost', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('combatMod', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('marksmanshipMod', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('bravadoMod', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('arcaneMod', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
        ))
        db.send_create_signal('eotd', ['Faction'])

        # Adding model 'UnitTemplateSkill'
        db.create_table('eotd_unittemplateskill', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('skill', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eotd.Skill'])),
            ('unitTemplate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eotd.UnitTemplate'])),
        ))
        db.send_create_signal('eotd', ['UnitTemplateSkill'])

        # Adding model 'UnitTemplateWeapon'
        db.create_table('eotd_unittemplateweapon', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('weapon', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eotd.Weapon'])),
            ('unitTemplate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eotd.UnitTemplate'])),
        ))
        db.send_create_signal('eotd', ['UnitTemplateWeapon'])

        # Adding model 'UnitTemplateSkillList'
        db.create_table('eotd_unittemplateskilllist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('special', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('skillLists', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eotd.SkillList'])),
            ('unitTemplate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eotd.UnitTemplate'])),
        ))
        db.send_create_signal('eotd', ['UnitTemplateSkillList'])

        # Adding model 'UnitTemplateWeaponList'
        db.create_table('eotd_unittemplateweaponlist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('medievalOnly', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('weaponLists', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eotd.WeaponList'])),
            ('unitTemplate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eotd.UnitTemplate'])),
        ))
        db.send_create_signal('eotd', ['UnitTemplateWeaponList'])

        # Adding model 'UnitWeapon'
        db.create_table('eotd_unitweapon', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('weapon', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eotd.Weapon'])),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eotd.Unit'], null=True)),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eotd.Team'], null=True)),
            ('nameOverride', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('creationTime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
        ))
        db.send_create_signal('eotd', ['UnitWeapon'])

        # Adding model 'UnitTemplate'
        db.create_table('eotd_unittemplate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('supernatural', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('maxCount', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('hero', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('leader', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('animal', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cost', self.gf('django.db.models.fields.SmallIntegerField')(default=100)),
            ('movement', self.gf('django.db.models.fields.SmallIntegerField')(default=4)),
            ('combat', self.gf('django.db.models.fields.SmallIntegerField')(default=3)),
            ('marksmanship', self.gf('django.db.models.fields.SmallIntegerField')(default=3)),
            ('strength', self.gf('django.db.models.fields.SmallIntegerField')(default=3)),
            ('fortitude', self.gf('django.db.models.fields.SmallIntegerField')(default=3)),
            ('attacks', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('wounds', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('bravado', self.gf('django.db.models.fields.SmallIntegerField')(default=4)),
            ('arcane', self.gf('django.db.models.fields.SmallIntegerField')(default=3)),
        ))
        db.send_create_signal('eotd', ['UnitTemplate'])

        # Adding M2M table for field faction on 'UnitTemplate'
        db.create_table('eotd_unittemplate_faction', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('unittemplate', models.ForeignKey(orm['eotd.unittemplate'], null=False)),
            ('faction', models.ForeignKey(orm['eotd.faction'], null=False))
        ))
        db.create_unique('eotd_unittemplate_faction', ['unittemplate_id', 'faction_id'])

        # Adding model 'Unit'
        db.create_table('eotd_unit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('baseUnit', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['eotd.UnitTemplate'])),
            ('unitName', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('unitLeaderOverride', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('faction', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='faction_units', to=orm['eotd.Faction'])),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='units', to=orm['eotd.Team'])),
            ('unitOrder', self.gf('django.db.models.fields.SmallIntegerField')(default=999)),
        ))
        db.send_create_signal('eotd', ['Unit'])

        # Adding model 'Team'
        db.create_table('eotd_team', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('faction', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['eotd.Faction'])),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['auth.User'], null=True, blank=True)),
            ('coins', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=800, blank=True)),
        ))
        db.send_create_signal('eotd', ['Team'])

        # Adding model 'Game'
        db.create_table('eotd_game', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(default=datetime.date.today)),
            ('campaign', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='games', null=True, to=orm['eotd.Campaign'])),
        ))
        db.send_create_signal('eotd', ['Game'])

        # Adding model 'GameTeam'
        db.create_table('eotd_gameteam', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('game', self.gf('django.db.models.fields.related.ForeignKey')(related_name='gameteam_set', to=orm['eotd.Game'])),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eotd.Team'])),
            ('victoryPoints', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('earnings', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
        ))
        db.send_create_signal('eotd', ['GameTeam'])

        # Adding model 'GameUnit'
        db.create_table('eotd_gameunit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('gameTeam', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eotd.GameTeam'])),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['eotd.Unit'])),
            ('skills', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='game_unit_for_skill', null=True, blank=True, to=orm['eotd.Skill'])),
            ('injuries', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='game_unit_for_injury', null=True, blank=True, to=orm['eotd.Injury'])),
        ))
        db.send_create_signal('eotd', ['GameUnit'])


    def backwards(self, orm):
        # Deleting model 'CampaignApplicant'
        db.delete_table('eotd_campaignapplicant')

        # Deleting model 'Campaign'
        db.delete_table('eotd_campaign')

        # Removing M2M table for field admins on 'Campaign'
        db.delete_table('eotd_campaign_admins')

        # Removing M2M table for field players on 'Campaign'
        db.delete_table('eotd_campaign_players')

        # Removing M2M table for field teams on 'Campaign'
        db.delete_table('eotd_campaign_teams')

        # Deleting model 'SkillList'
        db.delete_table('eotd_skilllist')

        # Removing M2M table for field skills on 'SkillList'
        db.delete_table('eotd_skilllist_skills')

        # Deleting model 'WeaponList'
        db.delete_table('eotd_weaponlist')

        # Removing M2M table for field weapons on 'WeaponList'
        db.delete_table('eotd_weaponlist_weapons')

        # Deleting model 'Injury'
        db.delete_table('eotd_injury')

        # Deleting model 'Skill'
        db.delete_table('eotd_skill')

        # Deleting model 'Weapon'
        db.delete_table('eotd_weapon')

        # Deleting model 'Faction'
        db.delete_table('eotd_faction')

        # Deleting model 'UnitTemplateSkill'
        db.delete_table('eotd_unittemplateskill')

        # Deleting model 'UnitTemplateWeapon'
        db.delete_table('eotd_unittemplateweapon')

        # Deleting model 'UnitTemplateSkillList'
        db.delete_table('eotd_unittemplateskilllist')

        # Deleting model 'UnitTemplateWeaponList'
        db.delete_table('eotd_unittemplateweaponlist')

        # Deleting model 'UnitWeapon'
        db.delete_table('eotd_unitweapon')

        # Deleting model 'UnitTemplate'
        db.delete_table('eotd_unittemplate')

        # Removing M2M table for field faction on 'UnitTemplate'
        db.delete_table('eotd_unittemplate_faction')

        # Deleting model 'Unit'
        db.delete_table('eotd_unit')

        # Deleting model 'Team'
        db.delete_table('eotd_team')

        # Deleting model 'Game'
        db.delete_table('eotd_game')

        # Deleting model 'GameTeam'
        db.delete_table('eotd_gameteam')

        # Deleting model 'GameUnit'
        db.delete_table('eotd_gameunit')


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
            'game': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'gameteam_set'", 'to': "orm['eotd.Game']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eotd.Team']"}),
            'units': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'game_for_unit'", 'default': 'None', 'to': "orm['eotd.Unit']", 'through': "orm['eotd.GameUnit']", 'blank': 'True', 'symmetrical': 'False'}),
            'victoryPoints': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'})
        },
        'eotd.gameunit': {
            'Meta': {'object_name': 'GameUnit'},
            'gameTeam': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eotd.GameTeam']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'injuries': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'game_unit_for_injury'", 'null': 'True', 'blank': 'True', 'to': "orm['eotd.Injury']"}),
            'skills': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'game_unit_for_skill'", 'null': 'True', 'blank': 'True', 'to': "orm['eotd.Skill']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['eotd.Unit']"})
        },
        'eotd.injury': {
            'Meta': {'object_name': 'Injury'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'penalty': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        'eotd.skill': {
            'Meta': {'object_name': 'Skill'},
            'arcanePower': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'store': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['eotd.Weapon']", 'symmetrical': 'False', 'through': "orm['eotd.UnitWeapon']", 'blank': 'True'})
        },
        'eotd.unit': {
            'Meta': {'ordering': "['unitOrder']", 'object_name': 'Unit'},
            'baseUnit': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['eotd.UnitTemplate']"}),
            'faction': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'faction_units'", 'to': "orm['eotd.Faction']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'cost': ('django.db.models.fields.SmallIntegerField', [], {'default': '100'}),
            'faction': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'related_name': "'unit_templates'", 'symmetrical': 'False', 'to': "orm['eotd.Faction']"}),
            'fortitude': ('django.db.models.fields.SmallIntegerField', [], {'default': '3'}),
            'hero': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leader': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'marksmanship': ('django.db.models.fields.SmallIntegerField', [], {'default': '3'}),
            'maxCount': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'movement': ('django.db.models.fields.SmallIntegerField', [], {'default': '4'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'skillLists': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'related_name': "'unit_template_skilllists'", 'symmetrical': 'False', 'through': "orm['eotd.UnitTemplateSkillList']", 'to': "orm['eotd.SkillList']"}),
            'skills': ('django.db.models.fields.related.ManyToManyField', [], {'default': 'None', 'to': "orm['eotd.Skill']", 'symmetrical': 'False', 'through': "orm['eotd.UnitTemplateSkill']", 'blank': 'True'}),
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