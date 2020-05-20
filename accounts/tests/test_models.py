from django.db import IntegrityError
from django.test import TestCase

from accounts.models import Company, Token, User


class UserModelTests(TestCase):

    def common_user_assertions(self, instance, email, first_name, last_name, full_name):
        self.assertEqual(instance.email, email)
        self.assertEqual(instance.first_name, first_name)
        self.assertEqual(instance.last_name, last_name)
        self.assertEqual(instance.full_name, full_name)
        self.assertEqual(instance.is_active, True)

    def token_created_assertion(self, instance):
        token = Token.objects.get(user=instance)
        self.assertIsNotNone(token)

    def setUp(self):
        self.user = User.objects.create_user(
            email="classuser@gmail.com",
            first_name="Golden",
            last_name="Retriever",
            password="WuoffWuoff"
        )

    def test_create_super_user(self):
        User.objects.create_superuser(
            email="Superuser@gmail.com",
            first_name="johnny",
            last_name="Bravo",
            password="SuPeRhAsHeD"
        )
        super_user = User.objects.get(email="superuser@gmail.com")
        self.common_user_assertions(
            super_user, "superuser@gmail.com", "johnny", "Bravo", "johnny Bravo"
        )
        self.assertEqual(super_user.is_staff, True)
        self.assertEqual(super_user.is_admin, True)
        self.assertEqual(super_user.role, 0)
        self.token_created_assertion(super_user)

    def test_create_staff_user(self):
        User.objects.create_staffuser(
            email="Staffuser@gmail.com",
            first_name="Joe",
            last_name="King",
            password="SuPeRhAsHeD2"
        )
        admin_user = User.objects.get(email="staffuser@gmail.com")
        self.common_user_assertions(
        admin_user, "staffuser@gmail.com", "Joe", "King", "Joe King"
        )
        self.assertEqual(admin_user.is_staff, True)
        self.assertEqual(admin_user.is_admin, False)
        self.assertEqual(admin_user.role, 3)
        self.token_created_assertion(admin_user)

    def create_user(self):
        base_user = User.objects.create_user(
            email="CommonUser@gmail.com",
            first_name="Ana",
            last_name="Reilly",
            password="PA314lpg"
        )
        self.common_user_assertions(
            base_user, "commonuser@gmail.com", "Ana", "Reilly", "Ana Reilly"
        )
        self.assertEqual(base_user.is_staff, False)
        self.assertEqual(base_user.is_admin, False)
        self.assertEqual(base_user.role, 1)
        self.token_created_assertion(base_user)

    def create_company_user(self):
        User.objects.create_user(
            email="CompanyUser@gmail.com",
            first_name="Obey",
            last_name="Fedex",
            password="PA314lpg",
            role=2
        )
        company_user = User.objects.get(email="companyuser@gmail.com")
        self.common_user_assertions(
            company_user, "companyuser@gmail.com", "Obey", "Fedex", "Obey Fedex"
        )
        self.assertEqual(company_user.is_staff, False)
        self.assertEqual(company_user.is_admin, False)
        self.assertEqual(company_user.role, 2)
        self.token_created_assertion(company_user)

    def test_create_user_with_missing_field(self):
        with self.assertRaisesMessage(ValueError, "Users must have a password"):
            User.objects.create_user(
                email="CommonUser@gmail.com",
                first_name="Ana",
                last_name="Reilly",
            )
        with self.assertRaisesMessage(ValueError, "Users must have an email address"):
            User.objects.create_user(
                email=None,
                first_name="Ana",
                last_name="Reilly",
                password="PA314lpg",
            )
        with self.assertRaisesMessage(ValueError, "Users must have a first name"):
            User.objects.create_user(
                email="CommonUser@gmail.com",
                first_name=None,
                last_name="Reilly",
                password="PA314lpg",
            )
        with self.assertRaisesMessage(ValueError, "Users must have a last name"):
            User.objects.create_user(
                email="CommonUser@gmail.com",
                first_name="Ana",
                last_name=None,
                password="PA314lpg",
            )

    def test_user_model_functions(self):
        self.assertEqual(str(self.user), "classuser@gmail.com")
        self.assertEqual(self.user.get_full_name(), "Golden Retriever")
        # TODO: has_perm & has_module_perms
        self.assertEqual(self.user.is_staff, False)
        self.assertEqual(self.user.is_admin, False)
        self.assertEqual(self.user.is_active, True)

    def test_most_similar_permited_user(self):
        most_similar_permited_user = User.objects.create(
            email="classuser2@gmail.com",
            first_name="Golden",
            last_name="Retriever",
            password="WuoffWuoff"
        )
        self.assertEqual(User.objects.get(email="classuser2@gmail.com"), most_similar_permited_user)
        self.assertNotEqual(User.objects.get(email="classuser2@gmail.com"), self.user)

    def test_user_has_to_be_unique(self):
        with self.assertRaises(IntegrityError):
            User.objects.create(
                email="classuser@gmail.com",
                first_name="Golden",
                last_name="Retriever",
                password="WuoffWuoff"
            )


class CompanyModelTests(TestCase):

    def setUp(self):
        self.company_user = User.objects.create_user(
            email="CompanyUser@gmail.com",
            first_name="Wabi",
            last_name="Casa",
            password="PA314lpg",
            role=2
        )

    def test_company_profile_is_created(self):
        Company.objects.create(
            user=self.company_user,
            phone=+5491162956565,
            companyName="Wabi"
        )
        company_profile = Company.objects.get(user=self.company_user)
        self.assertIsNotNone(company_profile)
        self.assertEqual(company_profile.phone, "5491162956565")
        self.assertIsNone(company_profile.instaAccount)
        self.assertEqual(company_profile.companyName, "Wabi")

    def test_company_profile_double_association(self):
        with self.assertRaises(IntegrityError):
            Company.objects.create(
                user=self.company_user,
                phone=+5491162956565,
                companyName="Wabi"
            )
            Company.objects.create(
                user=self.company_user,
                phone=+5491163256565,
                companyName="Coca"
            )
