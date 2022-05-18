import unittest
from app.models import User


class TestUser(unittest.TestCase):
    '''
    Test Class to test the behaviour of the User class
    '''
    def setUp(self):
        self.user_Esa_Gavin = User(username = 'Esa Gavin', password_hash = 'cyberpunk2077', email = 'gavinkariuki@gmail.com',
        image_file = 'https://image.tmdb.org/t/p/w500/cough', blog = 'wake up samurai, we have a python to burn')

        def tearDown(self):
            User.Clear_user()

        def test_check_instance_variables(self):
            self.assertEquals(self.new_Esa_Gavin.id, 1)
            self.assertEquals(self.new_Esa_Gavin.username, 'Esa Gavin')
            self.assertEquals(self.new_Esa_Gavin.password, 'cyberpunk2077')
            self.assertEquals(self.new_Esa_Gavin.email, 'gavinkariuki@gmail.com')
            self.assertEquals(self.new_Esa_Gavin.bio, 'Lord of Cinders')
            self.assertEquals(self.new_Esa_Gavin.profile_pic_path, 'https://image.tmdb.org/t/p/w500/cough')
            self.assertEquals(self.new_Esa_Gavin.pitch, 'wake up samurai, we have a python to burn')

        def test_password_setter(self):
            self.assertTrue(self.news_user.pass_secure is not None)

        def test_no_access_password(self):
            with self.assertRaises(AttributeError):
                self.new_user.password

        def test_password_verification(self):
            self.assertTrue(self.new_user.verify_password('cyberpunk2077'))
