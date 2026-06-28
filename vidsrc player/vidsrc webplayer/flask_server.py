from flask import Flask, request, render_template_string
from tmdb_api import search, get_tv_details, get_imdb_id, get_popular  # or paste function above

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VidBRZ</title>
    <style>

        
    body {
        font-family: Arial;
        background: #111;
        color: white;
        margin: 0;
        padding: 10px;
    }

    .search {
        padding: 12px;
        width: 100%;
        max-width: 400px;
        margin-bottom: 10px;
    }

    form {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
    }

    button {
        padding: 12px;
    }

    .card {
        display: flex;
        flex-direction: row;
        gap: 10px;
        margin: 10px 0;
        background: #222;
        padding: 10px;
        border-radius: 8px;
    }

    img {
        width: 120px;
        border-radius: 6px;
    }

    .card div {
        flex: 1;
    }

    /* 📱 MOBILE RESPONSIVE */
    @media (max-width: 600px) {
        .card {
            flex-direction: column;
            align-items: center;
            text-align: center;
        }

        img {
            width: 60%;
        }

        .search {
            width: 100%;
        }
    }
        .card a {
        color: white;
        text-decoration: none;
        }

        .card a:visited {
            color: white;
        }

        .card a:hover {
            color: #ddd;
            text-decoration: underline;
        }
        .home-link {
        color: white;
        text-decoration: none;
    }

    .home-link:visited {
        color: white;
    }

    .home-link:hover {
        color: #ddd;
        text-decoration: underline;
    }
</style>

</head>
<body>

<h1><a class="home-link" href="/">VidBRZ</a><color=#ppp></h1>

<form method="GET">
    <input class="search" name="q" placeholder="Search movies..." />
    <button type="submit">Search</button>
</form>


{% if not request.args.get('q') %}
    <h2>🔥 Trending</h2>
{% endif %}


{% for m in movies %}
<div class="card">
    {% if m.media_type == "tv" %}
    <a href="/tv/{{ m.tmdb_id }}">View Seasons</a>
    {% else %}
    <a href="{{ m.vidsrc_url }}" target="_blank">Watch Movie</a>
    {% endif %}

    <img src="{{ m.poster }}">
    <div>
        <h2>{{ m.title }}</h2>
        <p>{{ m.release_date }}</p>
        <p>{{ m.overview }}</p>
    </div>
</div>
{% endfor %}

</body>
</html>
"""

TV_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ show.name }}</title>
    <style>
        body { font-family: Arial; background:#111; color:white; padding:20px; }
        .season { background:#222; padding:10px; margin:10px 0; border-radius:8px; }
        a { color: #4da3ff; }
    </style>
</head>
<body>

<h1>{{ show.name }}</h1>
<p>{{ show.overview }}</p>

<h2>Seasons</h2>

{% for season in show.seasons %}
    {% if season.season_number > 0 %}
    <div class="season">
        <h3>Season {{ season.season_number }}</h3>
        <p>Episodes: {{ season.episode_count }}</p>

        {% for ep in range(1, season.episode_count + 1) %}
            <p>
                Episode {{ ep }} -
                <a target="_blank"
                   href="https://vidsrc-embed.ru/embed/tv/{{show_id}}/{{ season.season_number }}-{{ ep }}">
                   Watch
                </a>
            </p>
        {% endfor %}
    </div>
    {% endif %}
{% endfor %}

</body>
</html>
"""



@app.route("/")
def home():
    query = request.args.get("q")

    movies = []

    popular = get_popular()

    if query:
        movies = search(query)
    else:
        movies = popular

    return render_template_string(HTML, movies=movies)


@app.route("/tv/<int:tv_id>")
def tv_page(tv_id):
    show = get_tv_details(tv_id)
    show_id = get_imdb_id(tv_id)
    return render_template_string(TV_HTML, show=show, show_id=show_id)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)



