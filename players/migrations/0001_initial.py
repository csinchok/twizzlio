# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Player'
        db.create_table('players_player', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('photo', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
        ))
        db.send_create_signal('players', ['Player'])

        # Adding unique constraint on 'Player', fields ['name', 'user']
        db.create_unique('players_player', ['name', 'user_id'])

        # Adding model 'BrandPlayer'
        db.create_table('players_brandplayer', (
            ('player_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['players.Player'], unique=True, primary_key=True)),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('twitter_handle', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('facebook_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('players', ['BrandPlayer'])

        # Adding model 'BrandFacebookData'
        db.create_table('players_brandfacebookdata', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['players.Player'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('likes', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('talking_about', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('posts', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('players', ['BrandFacebookData'])

        # Adding unique constraint on 'BrandFacebookData', fields ['player', 'date']
        db.create_unique('players_brandfacebookdata', ['player_id', 'date'])

        # Adding model 'FacebookData'
        db.create_table('players_facebookdata', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['players.Player'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('friends', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('players', ['FacebookData'])

        # Adding unique constraint on 'FacebookData', fields ['player', 'date']
        db.create_unique('players_facebookdata', ['player_id', 'date'])

        # Adding model 'TwitterData'
        db.create_table('players_twitterdata', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['players.Player'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('followers', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('statuses', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('players', ['TwitterData'])

        # Adding unique constraint on 'TwitterData', fields ['player', 'date']
        db.create_unique('players_twitterdata', ['player_id', 'date'])

        # Adding model 'BrandTwitterData'
        db.create_table('players_brandtwitterdata', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['players.Player'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('followers', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('statuses', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal('players', ['BrandTwitterData'])

        # Adding unique constraint on 'BrandTwitterData', fields ['player', 'date']
        db.create_unique('players_brandtwitterdata', ['player_id', 'date'])


    def backwards(self, orm):
        # Removing unique constraint on 'BrandTwitterData', fields ['player', 'date']
        db.delete_unique('players_brandtwitterdata', ['player_id', 'date'])

        # Removing unique constraint on 'TwitterData', fields ['player', 'date']
        db.delete_unique('players_twitterdata', ['player_id', 'date'])

        # Removing unique constraint on 'FacebookData', fields ['player', 'date']
        db.delete_unique('players_facebookdata', ['player_id', 'date'])

        # Removing unique constraint on 'BrandFacebookData', fields ['player', 'date']
        db.delete_unique('players_brandfacebookdata', ['player_id', 'date'])

        # Removing unique constraint on 'Player', fields ['name', 'user']
        db.delete_unique('players_player', ['name', 'user_id'])

        # Deleting model 'Player'
        db.delete_table('players_player')

        # Deleting model 'BrandPlayer'
        db.delete_table('players_brandplayer')

        # Deleting model 'BrandFacebookData'
        db.delete_table('players_brandfacebookdata')

        # Deleting model 'FacebookData'
        db.delete_table('players_facebookdata')

        # Deleting model 'TwitterData'
        db.delete_table('players_twitterdata')

        # Deleting model 'BrandTwitterData'
        db.delete_table('players_brandtwitterdata')


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
        'players.brandfacebookdata': {
            'Meta': {'unique_together': "(('player', 'date'),)", 'object_name': 'BrandFacebookData'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likes': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['players.Player']"}),
            'posts': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'talking_about': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        'players.brandplayer': {
            'Meta': {'object_name': 'BrandPlayer', '_ormbases': ['players.Player']},
            'facebook_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'player_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['players.Player']", 'unique': 'True', 'primary_key': 'True'}),
            'twitter_handle': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'players.brandtwitterdata': {
            'Meta': {'unique_together': "(('player', 'date'),)", 'object_name': 'BrandTwitterData'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'followers': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['players.Player']"}),
            'statuses': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        'players.facebookdata': {
            'Meta': {'unique_together': "(('player', 'date'),)", 'object_name': 'FacebookData'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'friends': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['players.Player']"})
        },
        'players.player': {
            'Meta': {'unique_together': "(('name', 'user'),)", 'object_name': 'Player'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'photo': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'})
        },
        'players.twitterdata': {
            'Meta': {'unique_together': "(('player', 'date'),)", 'object_name': 'TwitterData'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'followers': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['players.Player']"}),
            'statuses': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        }
    }

    complete_apps = ['players']