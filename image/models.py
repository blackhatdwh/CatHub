from django.db import models

# Create your models here.

class Image(models.Model):
    name = models.CharField(max_length=30)
    gif_file = models.FileField(upload_to='IMG_FILE')
    still_file = models.FileField(upload_to='IMG_FILE')
    pub_date = models.DateTimeField()
    oo_num = models.IntegerField(default=0)
    xx_num = models.IntegerField(default=0)
    comment_num = models.IntegerField(default=0)
    def __str__(self):
        return self.name

class Comment(models.Model):
    image_id = models.ForeignKey(Image, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    content = models.CharField(max_length=300)
    pub_date = models.DateTimeField()
    oo_num = models.IntegerField(default=0)
    xx_num = models.IntegerField(default=0)
    reply_to = models.ForeignKey("Comment", on_delete=models.CASCADE, blank=True, null=True)

class Comment_Vote(models.Model):
    comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE)
    ip_addr = models.CharField(max_length=15)
    attitude = models.BooleanField()
    class Meta:
        unique_together = (('comment_id', 'ip_addr'),)
