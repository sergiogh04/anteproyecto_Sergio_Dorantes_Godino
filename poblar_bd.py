from django.contrib.auth.models import User
from anime.models import Genre, Anime
from datetime import date

# Crear superusuario
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'adminpassword')
    print("✅ Superusuario creado: admin / adminpassword")
else:
    print("🔐 El superusuario 'admin' ya existe.")

# Crear géneros
genres = ['Acción', 'Aventura', 'Comedia', 'Drama', 'Fantasía', 'Ciencia Ficción', 'Romance', 'Terror', 'Slice of Life']
genre_objs = []
for name in genres:
    genre, created = Genre.objects.get_or_create(name=name)
    genre_objs.append(genre)
    print(f"{'✅' if created else '📁'} Género: {name}")

# Lista de animes
anime_data = [
    {"title": "Naruto", "format": "TV", "status": "finished", "episodes": 220, "year": date(2002, 10, 3), "is_trending": True, "is_seasonal": False},
    {"title": "Attack on Titan", "format": "TV", "status": "finished", "episodes": 87, "year": date(2013, 4, 6), "is_trending": True, "is_seasonal": False},
    {"title": "Jujutsu Kaisen", "format": "TV", "status": "airing", "episodes": 24, "year": date(2020, 10, 3), "is_trending": True, "is_seasonal": True},
    {"title": "Your Name", "format": "Movie", "status": "finished", "episodes": 1, "year": date(2016, 8, 26), "is_trending": False, "is_seasonal": False},
    {"title": "Vivy: Fluorite Eye’s Song", "format": "TV", "status": "finished", "episodes": 13, "year": date(2021, 4, 3), "is_trending": False, "is_seasonal": True},
    {"title": "Steins;Gate", "format": "TV", "status": "finished", "episodes": 24, "year": date(2011, 4, 6), "is_trending": True, "is_seasonal": False},
    {"title": "Demon Slayer", "format": "TV", "status": "airing", "episodes": 26, "year": date(2019, 4, 6), "is_trending": True, "is_seasonal": True},
    {"title": "Chainsaw Man", "format": "TV", "status": "airing", "episodes": 12, "year": date(2022, 10, 12), "is_trending": False, "is_seasonal": True},
    {"title": "Made in Abyss", "format": "TV", "status": "finished", "episodes": 13, "year": date(2017, 7, 7), "is_trending": False, "is_seasonal": False},
    {"title": "Death Note", "format": "TV", "status": "finished", "episodes": 37, "year": date(2006, 10, 3), "is_trending": True, "is_seasonal": False},
    {"title": "A Silent Voice", "format": "Movie", "status": "finished", "episodes": 1, "year": date(2016, 9, 17), "is_trending": False, "is_seasonal": False},
    {"title": "Mob Psycho 100", "format": "TV", "status": "finished", "episodes": 12, "year": date(2016, 7, 11), "is_trending": False, "is_seasonal": True},
    {"title": "Tokyo Revengers", "format": "TV", "status": "airing", "episodes": 24, "year": date(2021, 4, 11), "is_trending": True, "is_seasonal": True},
    {"title": "One Piece", "format": "TV", "status": "airing", "episodes": 1000, "year": date(1999, 10, 20), "is_trending": True, "is_seasonal": False},
]

# Añadir animes a la base de datos
for data in anime_data:
    anime, created = Anime.objects.get_or_create(
        title=data["title"],
        defaults={
            "description": f"Descripción de {data['title']}",
            "format": data["format"],
            "status": data["status"],
            "episodes": data["episodes"],
            "year": data["year"],
            "is_trending": data["is_trending"],
            "is_seasonal": data["is_seasonal"],
            "image": "https://via.placeholder.com/150"
        }
    )
    if created:
        anime.genres.set(genre_objs[:3])  # Asigna 3 primeros géneros
        anime.save()
        print(f"✅ Anime creado: {anime.title}")
    else:
        print(f"📁 Anime ya existente: {anime.title}")
