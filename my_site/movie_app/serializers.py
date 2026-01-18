from rest_framework import serializers
from .models import (
    UserProfile, Category, Country, Director, Actor, Genre,
    Movie, MovieLanguages, Moments, Rating, Review,
    ReviewLike, Favorite, FavoriteMovie, History
)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'age', 'phone_number')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'avatar']


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name']


class GenreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'genre_name']

class GenreNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['genre_name']


class CategoryDetailSerializer(serializers.ModelSerializer):
    genres = GenreListSerializer(read_only=True, many=True)
    class Meta:
        model = Category
        fields = ['category_name', 'genres']


class CountryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'country_name']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['country_name']


class MovieListSerializer(serializers.ModelSerializer):
    country = CountrySerializer(many=True)
    year = serializers.DateField(format('%Y'))
    genre = GenreNameSerializer(many=True)

    class Meta:
        model = Movie
        fields = ['id', 'movie_image', 'movie_name', 'year',
                  'country', 'genre', 'status_movie']


class DirectorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['id', 'director_name']


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ['director_name']


class DirectorDetailSerializer(serializers.ModelSerializer):
    director_movie = MovieListSerializer(read_only=True, many=True)
    class Meta:
        model = Director
        fields = ['director_name', 'director_movie']


class ActorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['id', 'actor_name']


class ActorDetailSerializer(serializers.ModelSerializer):
    actor_movie = MovieListSerializer(read_only=True, many=True)
    class Meta:
        model = Actor
        fields = ['actor_name', 'actor_movie']


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ['actor_name']


class CountryDetailSerializer(serializers.ModelSerializer):
    movie_country = MovieListSerializer(read_only=True, many=True)
    class Meta:
        model = Country
        fields = ['country_name', 'movie_country']


class GenreDetailSerializer(serializers.ModelSerializer):
    movie_genre = MovieListSerializer(read_only=True, many=True)
    class Meta:
        model = Genre
        fields = ['genre_name', 'movie_genre']


class MovieLanguagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieLanguages
        fields = ['language', 'video']


class ReviewSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()
    create_date = serializers.DateTimeField(format='%d-%m-%Y %H:%M')
    count_like = serializers.SerializerMethodField()
    class Meta:
        model = Review
        fields = ['user', 'text', 'create_date', 'parent', 'count_like']

    def count_like(self, obj):
        return obj.count_like()


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class MovieDetailSerializer(serializers.ModelSerializer):
    country = CountrySerializer(many=True)
    director = DirectorSerializer(many=True)
    genre = GenreNameSerializer(many=True)
    actor = ActorSerializer(many=True)
    movie_videos = MovieLanguagesSerializer(many=True, read_only=True)
    movie_review = ReviewSerializer(read_only = True, many=True)
    average_rating = serializers.SerializerMethodField()
    count_people = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['movie_name', 'movie_image', 'year', 'country', 'director', 'genre', 'types', 'movie_time', 'actor',
                  'movie_trailer', 'description', 'slogan', 'status_movie', 'movie_videos', 'average_rating', 'count_people', 'movie_review']

    def get_average_rating(self, obj):
        return obj.get_average_rating()

    def get_count_people(self, obj):
        return obj.get_count_people()


class MomentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moments
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'


class ReviewLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewLike
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'


class FavoriteMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteMovie
        fields = '__all__'


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'
