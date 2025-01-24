from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User



class Category(models.Model):
    name = models.CharField(max_length=100)  # Category name
    description = models.TextField(blank=True, null=True)  # Optional description

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)  # New field null ture blank true means its optional
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)  # Link post to category
    
    # models.ForeignKey:
    # This creates a many-to-one relationship. It means that many instances of this model (e.g., Post or Article) 
    # can be associated with one instance of the related model (User).
    
    # CASCADE means: If a User is deleted, all related Post or Article instances will also be deleted.
    # This is useful to maintain referential integrity.

    def __str__(self):
        return self.title
    
#     The __str__ method is a special method in Python that returns a human-readable or "pretty" string representation of an object.

# In the context of Django models, it is used to specify what should be displayed when you
# print an instance of the model or view it in the Django admin interface or other tools.

# When an instance of the Post model is converted to a string (e.g., in the admin interface or the shell), 
# it will display the value of its title field


