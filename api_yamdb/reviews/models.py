from django.db import models



CHOICES = [i for i in range(1,11)]


class Title():


class Review(models.Model):
    #author...
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField()
    score = models.IntegerField(choices=CHOICES)
    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True
    )

    def __str__(self) -> str:
        return self.text


class Comment(models.Model):
    #author...
    review_id = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации комментария',
        auto_now_add=True
    )

    def __str__(self) -> str:
        return self.text

