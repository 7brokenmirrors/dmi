from django.db import models
from django.db.models import F, Q
from django.db.models.functions import Length
from typedmodels.models import TypedModel

# Example from https://github.com/craigds/django-typed-models

models.CharField.register_lookup(Length)

class TypedAnimal(TypedModel):
    """
    Abstract model
    """
    name = models.CharField(max_length=255)

    def say_something(self):
        raise NotImplementedError

    def __repr__(self):
        return u'<%s: %s>' % (self.__class__.__name__, self.name)

    class Meta:
        constraints = [models.CheckConstraint(check=Q(name__length__gt=0), name='Animal must have a name'),
                       models.CheckConstraint(check=~Q(Q(type__exact='tmodels.canine') & Q(breed__isnull=True)), name='Canines must have a breed'),
                       models.CheckConstraint(check=~Q(Q(type__exact='tmodels.feline') & Q(breed__isnull=False)), name='Cats must not have a breed'),
                       models.CheckConstraint(check=~Q(Q(type__exact='tmodels.canine') & Q(mice_eaten__gt=0)), name='Canines must not eat mice'),
           ]
        
class Canine(TypedAnimal):
    breed = models.CharField(
        max_length=200,
        null=True,
    )

    def say_something(self):
        return "woof"


class Feline(TypedAnimal):
    mice_eaten = models.IntegerField(
        default=0,
        null=True,
    )

    def say_something(self):
        return "meoww"
