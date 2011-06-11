# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Lecture'
        db.create_table('main_lecture', (
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Category'])),
            ('annotation', self.gf('django.db.models.fields.TextField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('main', ['Lecture'])

        # Adding model 'Category'
        db.create_table('main_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('main', ['Category'])

        # Adding model 'Test'
        db.create_table('main_test', (
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Category'])),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('difficulty', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('time', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('main', ['Test'])

        # Adding model 'Question'
        db.create_table('main_question', (
            ('test', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Test'])),
            ('question', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('extra', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
        ))
        db.send_create_signal('main', ['Question'])

        # Adding model 'Answer'
        db.create_table('main_answer', (
            ('answer', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Question'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('correct', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
        ))
        db.send_create_signal('main', ['Answer'])

        # Adding model 'TestPass'
        db.create_table('main_testpass', (
            ('random_answer_choices', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('complite', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('mode', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('start', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('result', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('test', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Test'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['account.User'])),
        ))
        db.send_create_signal('main', ['TestPass'])

        # Adding model 'AnswerChoice'
        db.create_table('main_answerchoice', (
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Question'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('test_pass', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.TestPass'])),
        ))
        db.send_create_signal('main', ['AnswerChoice'])

        # Adding model 'AnswerResult'
        db.create_table('main_answerresult', (
            ('answer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Answer'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='answers', to=orm['main.AnswerChoice'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('main', ['AnswerResult'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Lecture'
        db.delete_table('main_lecture')

        # Deleting model 'Category'
        db.delete_table('main_category')

        # Deleting model 'Test'
        db.delete_table('main_test')

        # Deleting model 'Question'
        db.delete_table('main_question')

        # Deleting model 'Answer'
        db.delete_table('main_answer')

        # Deleting model 'TestPass'
        db.delete_table('main_testpass')

        # Deleting model 'AnswerChoice'
        db.delete_table('main_answerchoice')

        # Deleting model 'AnswerResult'
        db.delete_table('main_answerresult')
    
    
    models = {
        'account.user': {
            'Meta': {'object_name': 'User', '_ormbases': ['auth.User']},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['account.UserGroup']", 'null': 'True', 'blank': 'True'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'account.usergroup': {
            'Meta': {'object_name': 'UserGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
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
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'main.answer': {
            'Meta': {'object_name': 'Answer'},
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'correct': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Question']"})
        },
        'main.answerchoice': {
            'Meta': {'object_name': 'AnswerChoice'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Question']"}),
            'test_pass': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.TestPass']"})
        },
        'main.answerresult': {
            'Meta': {'object_name': 'AnswerResult'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Answer']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'to': "orm['main.AnswerChoice']"})
        },
        'main.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'main.lecture': {
            'Meta': {'object_name': 'Lecture'},
            'annotation': ('django.db.models.fields.TextField', [], {}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Category']"}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'main.question': {
            'Meta': {'object_name': 'Question'},
            'extra': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'test': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Test']"})
        },
        'main.test': {
            'Meta': {'object_name': 'Test'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Category']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'difficulty': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'time': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'main.testpass': {
            'Meta': {'object_name': 'TestPass'},
            'complite': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mode': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'random_answer_choices': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'result': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'test': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Test']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['account.User']"})
        }
    }
    
    complete_apps = ['main']
