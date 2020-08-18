from django.test import TestCase
from .models import Profile,Projects,Rates
from django.contrib.auth.models import User

# Create your tests here.
class ProfileTestClass(TestCase):
    '''
    Creating testclass for user profiles
    '''
    def setUp(self):
        
        self.kiragu = User(username='kiragu', password='12345')
        self.kiragu = Profile( profile_photo='default.png',bio='Finding inspiration from fellow developers', website='www.me.me', phone_number='0747676733')

    def test_instance(self):
        self.assertTrue(isinstance(self.kiragu,Profile))

    def test_save(self):
        self.kiragu.save_profile()
        profiles = Profile.objects.all()
        self.assertTrue(len(profiles)>0)
 

class PostsTestClass(TestCase):
    '''
    Creating test class for user posts
    '''
    def setUp(self):
        self.kiragu = Profile(first_name='Duncan',last_name='kiragu',username='DunK',email='dunkiragu@gmail.com')
        self.kiragu.save()

        self.new_tag=tag(tag='testing')
        self.new_tag.save_tag()

        self.new_post =Posts(caption="testing testing 1,2",profile=self.kiragu)
        self.new_post.save_posts()

        self.new_post.tag.add(self.new_tag)

    def tearDown(self):
        Profile.objects.all().delete()
        tag.objects.all().delete()
        Posts.objects.all().delete()    

    def test_posts(self):
        posts = Posts.posts()
        self.assertTrue(len(posts)>0)


class RatesTestClass(TestCase):
    '''
    Creating test class for user ratings 
    '''
    def setUp(self):
        self.user = User(username='Bazenga',email='bigmanbazu@gmail.com',password='qwerty')
        
        self.rate = Rates(design=10,usability=10,content=10,user=self.user,project=10)
        self.rate.save()
        
        self.assertTrue(isinstance(self.rate,Rate))  