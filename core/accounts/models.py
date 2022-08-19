from django.db import models
from django.contrib.auth.models import(
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin
)
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _ 

class UserManager(BaseUserManager):
    """
    custom user manager  where email is require for authentication
    """

    def create_user(self, nickname, email, password, **extra_fields):
        if not email:
            raise ValueError("user must have an email address")
        if not nickname:
            raise ValueError("Users must have a nickname ")
        user=self.model(
            email=self.normalize_email(email),
            nickname=nickname.lower()
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,email,password,nickname,**extra_fields):
        """
        create and save a SuperUser with the given email and password
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        user = self.create_user(
        email=self.normalize_email(email),
        nickname=nickname.lower(),
        password=password
        )
        return user

class User(AbstractBaseUser,PermissionsMixin):
    """
    Custom User Model for authentication management 
    """
    email=models.EmailField(max_length=255,unique=True)
    nickname = models.CharField(max_length=255)
    is_superuser=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_active =models.BooleanField(default=True)
    is_verified= models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']


    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    
    


    def __str__(self):
        return self.email

class Profile(models.Model):
    """
    Profile Class for each user
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    image = models.ImageField(blank=True, null=True)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email 


@receiver(post_save,sender=User)
def save_profile(sender, instance, created, **kwargs):
    """
    Signal for post creating a user which activates when a user being created ONLY
    """
    if created:
        Profile.objects.create(user=instance)
