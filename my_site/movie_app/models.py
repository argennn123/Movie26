from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from multiselectfield import MultiSelectField

STATUS_CHOICES = (
    ('pro', 'pro'),
    ('simple', 'simple')
)

class UserProfile(AbstractUser):
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(15),
                                                       MaxValueValidator(80)],
                                           null=True, blank=True)
    phone_number = PhoneNumberField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='simple')
    avatar = models.ImageField(upload_to='User_photo/', null=True, blank=True)
    data_register = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Category(models.Model):
    category_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.category_name


class Country(models.Model):
    country_name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.country_name


class Director(models.Model):
    director_name = models.CharField(max_length=64)
    director_bio = models.TextField()
    director_age = models.PositiveSmallIntegerField(validators=[MinValueValidator(16),
                                                       MaxValueValidator(100)],
                                           null=True, blank=True)
    director_image = models.ImageField(upload_to='director_photo/')

    def __str__(self):
        return f'{self.director_name}'


class Actor(models.Model):
    actor_name = models.CharField(max_length=64)
    actor_bio = models.TextField()
    actor_age = models.PositiveSmallIntegerField(validators=[MinValueValidator(0),
                                                       MaxValueValidator(100)],
                                           null=True, blank=True)
    actor_image = models.ImageField(upload_to='actor_photo/')

    def __str__(self):
        return self.actor_name


class Genre(models.Model):
    genre_name = models.CharField(max_length=32)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='genres')

    def __str__(self):
        return self.genre_name


class Movie(models.Model):
    movie_name = models.CharField(max_length=64)
    year = models.DateField()
    country = models.ManyToManyField(Country, related_name='movie_country')
    director = models.ManyToManyField(Director, related_name='director_movie')
    actor = models.ManyToManyField(Actor, related_name='actor_movie')
    genre = models.ManyToManyField(Genre, related_name='movie_genre')
    TYPES_CHOICES  = (
        ('360p', '360p'),
        ('480p', '480p'),
        ('720p', '720p'),
        ('1080p', '1080p'),
        ('1080p Ultra', '1080p Ultra')
    )
    types = MultiSelectField(choices=TYPES_CHOICES, default='1080p')
    movie_time = models.PositiveSmallIntegerField()
    description = models.TextField()
    movie_trailer = models.URLField()
    movie_image = models.ImageField(upload_to='movie_photo/')
    slogan = models.CharField(max_length=60, null=True, blank=True)
    status_movie = models.CharField(max_length=32, choices=STATUS_CHOICES)

    def __str__(self):
        return self.movie_name

    def get_average_rating(self):
        rating = self.rating_movie.all()
        if rating.exists():
            return round(sum([i.stars for i in rating]) / rating.count(), 2)
        return 0

    def get_count_people(self):
        return self.rating_movie.count()


class MovieLanguages(models.Model):
    language = models.CharField(max_length=32)
    video = models.FileField(upload_to='movie_video/')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_videos')

    def __str__(self):
        return self.language


class Moments(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    movie_moments = models.ImageField(upload_to='movie_moments/')


class Rating(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='rating_movie')
    stars = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 11)],
                                             null=True, blank=True)

    def __str__(self):
        return f'{self.movie.movie_name} {self.stars}'


class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_review')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.movie.movie_name} {self.text}'

    def count_like(self):
        return self.like.count()



class ReviewLike(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='like')
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)


class Favorite(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name


class FavoriteMovie(models.Model):
    favorite = models.ForeignKey(Favorite, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return self.favorite.user.first_name


class History(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)



