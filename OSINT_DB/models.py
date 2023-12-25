from django.db import models


# Create your models here.
class Events(models.Model):
    name = models.CharField(verbose_name="Events Name", max_length=4096)
    date = models.DateField(verbose_name="Events happened date", auto_now=True)
    score = models.FloatField(verbose_name="Events heat value")


class Objects(models.Model):
    name = models.CharField(verbose_name="Objects name", max_length=4096)
    role = models.IntegerField(verbose_name="The classes of object")
    gender = models.IntegerField(verbose_name="gender of object")

    def to_dict(self):
        return {"name":self.name,"role":self.role,"gender":self.gender}

    def __str__(self):
        return self.name + "," + str(self.role) + "," + str(self.gender)




class Keywords(models.Model):
    keyword = models.CharField(verbose_name="keywords", max_length=4096)
    date = models.DateField(verbose_name="The first time of it", auto_now=True)


class Events_to_Keywords(models.Model):
    events_id = models.ForeignKey(to="Events", verbose_name="Event ID", on_delete=models.CASCADE)
    keyword_id = models.ForeignKey(to="Keywords", verbose_name="Keyword ID", on_delete=models.CASCADE)


class Objects_to_Keywords(models.Model):
    object_id = models.ForeignKey(to="Objects", verbose_name="Object ID", on_delete=models.CASCADE)
    keyword_id = models.ForeignKey(to="Keywords", verbose_name="Keyword ID", on_delete=models.CASCADE)


class Objects_to_Objects(models.Model):
    object1_id = models.IntegerField()
    object2_id = models.IntegerField()


class Events_to_Objects(models.Model):
    events_id = models.ForeignKey(to="Events", on_delete=models.CASCADE)
    object_id = models.ForeignKey(to="Objects", on_delete=models.CASCADE)
