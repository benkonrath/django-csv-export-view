from django.db import models


class FieldTest(models.Model):
    date = models.DateField()
    datetime = models.DateTimeField()
    choice = models.CharField(max_length=1, choices=(("R", "Red"), ("G", "Green")), default="R")
    empty_choice = models.CharField(max_length=1, choices=(("Y", "Yellow"), ("B", "Black")), blank=True)
    integer_choice = models.IntegerField(choices=((0, "Zero"), (1, "One")), default=0)

    @property
    def my_property(self):
        return "Foo"


# Many-to-one relationships
class Manufacturer(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Car(models.Model):
    name = models.CharField(max_length=50)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# Many-to-many relationships
class Topping(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=1)

    def __str__(self):
        return self.name


class Pizza(models.Model):
    name = models.CharField(max_length=50)
    toppings = models.ManyToManyField(Topping)

    def __str__(self):
        return self.name


# One-to-one relationships
class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)

    def __str__(self):
        return self.name


class Restaurant(models.Model):
    place = models.OneToOneField(Place, on_delete=models.CASCADE, primary_key=True)
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)

    def __str__(self):
        return self.place
