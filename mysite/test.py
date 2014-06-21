# -*- encoding:utf-8 -*-
# import os
# BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

# print BASE_DIR
# print TEMPLATE_DIRS
from django.test import TestCase
from django.test.client import Client

#fixtures 사용하기
#데이터베이스가 새로 만들어질때 데이터를 자동으로 입력해준다.
# python manaage.py dumpdata > test_data.json

class ViewTest(TestCase):
    #fixtures=['test_data.json']
    def setUp(self):
        self.client=Client()
        
    def test_register_page(self):
        data={
            'username':'test_user',
            'email':'test_user@example.com',
            'password1':'pass123',
            'password2':'pass123'
        }
        response=self.client.post('/bookmarks/register/',data)
        self.assertEqual(response.status_code,302)
        
    def test_bookmark_save(self):
        response=self.client.login('/bookmark/save/','your_username','your_password')
        self.assertTrue(response)
        
        data = {
            'url':'http://www.example.com',
            'title':'test url',
            'tags':'test-tag'
        }
        
        response=self.client.post('/bookmarks/save/',data)
        self.assertEqual(response.stats_code,302)
        
        response=self.client.get('/bookmarks/user/your_name/')
        self.assertTrue('http://www.example.com' in response.content)
        self.assertTrue('test url' in response.content)
        self.assertTrue('test-tag' in response.content)
        