import telebot #to comunicate with telegram bot
from telebot import types #to create buttons and keyboards
import requests #to make requests to TMDB API


bot = telebot.TeleBot('8687363218:AAHbRhZerHRqb_CSuRP2MwJT2pu05AhX1oU')
TMDB_API_KEY = "f9b625f44cf94f62cb3a2f62c2a5db33" #TMDB - this is the movie database


user_languages = {}
user_states = {}
# User data storage.

def send_top_movies(message):
    user_lang = user_languages.get(message.chat.id, "EN")
    tmdb_lang = "ru-RU" if user_lang == "RU" else "en-US"
   
    all_results = []

    for page in range(1, 5):  # input how many pages you want to grt
        url = f"https://api.themoviedb.org/3/movie/top_rated?api_key={TMDB_API_KEY}&language={tmdb_lang}&page={page}" #page = 20 movies or series
        # ask database for top rated movies

        response = requests.get(url)
        data = response.json()
        results = data.get('results', [])
        all_results.extend(results)
        # translate data to the json format

        if not results:
            bot.send_message(message.chat.id, "Не удалось получить топ фильмов." if user_lang == "RU" else "Failed to retrieve top movies.")
            return
        #analyze if request give a result

        top_movies_text = "Топ фильмов:\n\n" if user_lang == "RU" else "Top Movies:\n\n"  
        for i, movie in enumerate(all_results[:80], start=1):
        #form the list                
            title = movie.get('title', 'N/A')
            release_date = movie.get('release_date', 'N/A')
            year = release_date.split('-')[0] if release_date and release_date != 'N/A' else 'N/A'
            rating = movie.get('vote_average', 'N/A')
            #input type of data to be shown in the list

            if rating != 'N/A':
                rating = round(rating, 1)
            top_movies_text += f"{i}. {title} ({year}) - ⭐ {rating}/10\n"

    bot.send_message(message.chat.id, top_movies_text)

#function to send top 80 movies based on TMDB rating

def send_top_series(message): # This function has the same algorithm as the previous one, but it is for series
    user_lang = user_languages.get(message.chat.id, "EN")
    tmdb_lang = "ru-RU" if user_lang == "RU" else "en-US"
   
    all_results = []

    for page in range(1, 5):  
        url = f"https://api.themoviedb.org/3/tv/top_rated?api_key={TMDB_API_KEY}&language={tmdb_lang}&page={page}"
        
        response = requests.get(url)
        data = response.json()
        results = data.get('results', [])
        all_results.extend(results)

        if not results:
            bot.send_message(message.chat.id, "Не удалось получить топ сериалов." if user_lang == "RU" else "Failed to retrieve top TV shows.")
            return
        top_series_text = "Топ сериалов:\n\n" if user_lang == "RU" else "Top TV Shows:\n\n"   

        for i, series in enumerate(all_results[:80], start=1):
                        
            title = series.get('name', 'N/A')
            release_date = series.get('first_air_date', 'N/A')
            year = release_date.split('-')[0] if release_date and release_date != 'N/A' else 'N/A'
            rating = series.get('vote_average', 'N/A')

            if rating != 'N/A':
                rating = round(rating, 1)
            top_series_text += f"{i}. {title} ({year}) - ⭐ {rating}/10\n"
    bot.send_message(message.chat.id, top_series_text)

#function to send top 80 series based on TMDB rating

@bot.message_handler(commands=['start'])
# Handle the /start command.
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_ru = types.KeyboardButton("Russian")
    btn_en = types.KeyboardButton("English")
    markup.add(btn_ru, btn_en)

    bot.send_message(message.chat.id, "Выбери язык интерфейса / Choose your language:", reply_markup=markup)
# Creat the buttons and ask user which language he want to use

@bot.message_handler(func=lambda message: message.text in ["Russian", "English"])
def set_language(message):
    if message.text == "Russian":
        user_languages[message.chat.id] = "RU"     

        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_movie = types.KeyboardButton("Найти фильм")
        btn_show = types.KeyboardButton("Найти сериал")
        btn_top1 = types.KeyboardButton("Топ фильмов")
        btn_top2 = types.KeyboardButton("Топ сериалов")
    
        markup1.add(btn_movie, btn_show)
        markup1.add(btn_top1, btn_top2)

        bot.send_message(message.chat.id, "Хорошо, выбери действие:", reply_markup=markup1)

    elif message.text == "English":
        user_languages[message.chat.id] = "EN"
                
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_movie = types.KeyboardButton("Find a Movie")
        btn_show = types.KeyboardButton("Find a TV Show")
        btn_top1 = types.KeyboardButton("Top Movies")
        btn_top2 = types.KeyboardButton("Top TV Shows")
    
        markup1.add(btn_movie, btn_show)
        markup1.add(btn_top1, btn_top2)

        bot.send_message(message.chat.id, "Choose an option:", reply_markup=markup1)
#So after user choose the language we creat the buttons and ask user which action he want to do based on the language he choose

@bot.message_handler(func=lambda message: message.text in ["Find a Movie", "Find a TV Show", "Top Movies", "Top TV Shows", "Найти фильм", "Найти сериал", "Топ фильмов", "Топ сериалов"])
def option(message):
    if message.text == "Find a Movie" or message.text == "Найти фильм":
        user_states[message.chat.id] = "FIND_MOVIE"
        if user_languages.get(message.chat.id) == "RU":
            bot.send_message(message.chat.id, "Пожалуйста, введите название фильма:")
        else:
            bot.send_message(message.chat.id, "Please enter the movie name:")

    elif message.text == "Find a TV Show" or message.text == "Найти сериал":
        user_states[message.chat.id] = "FIND_TV_SHOW"
        if user_languages.get(message.chat.id) == "RU":
            bot.send_message(message.chat.id, "Пожалуйста, введите название сериала:")
        else:
            bot.send_message(message.chat.id, "Please enter the TV show name:")

    elif message.text == "Top Movies" or message.text == "Топ фильмов":
        user_states[message.chat.id] = "TOP_MOVIES"
        if user_languages.get(message.chat.id) == "RU":
            bot.send_message(message.chat.id, send_top_movies(message))
        else:
            bot.send_message(message.chat.id, send_top_movies(message))
    
    elif message.text == "Top TV Shows" or message.text == "Топ сериалов":
        user_states[message.chat.id] = "TOP_TV_SHOWS"
        if user_languages.get(message.chat.id) == "RU":
            bot.send_message(message.chat.id, send_top_series(message))
        else:
            bot.send_message(message.chat.id, send_top_series(message))
#in this function we check which button user pressed and based on that we switch the state of the user between searching movirs and series beacaus it has different urls or if you choose one of tops it call one of the functions send_top_movies or send_top_series 

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    state = user_states.get(message.chat.id)

    if state == "FIND_MOVIE":
        text = message.text.lower()
    
        user_lang = user_languages.get(message.chat.id, "EN")
    
        tmdb_lang = "ru-RU" if user_lang == "RU" else "en-US"

        wait_text = "Секунду, ищу фильм..." if user_lang == "RU" else "Please wait, it can take few seconds..."
        bot.send_message(message.chat.id, wait_text)
        # Here we get the name of the movie from user and add it to the url alongside with users language
        
        url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={text}&language={tmdb_lang}"
       

        response = requests.get(url)
        data = response.json()       
        results = data.get('results', [])
        #Here we also process the response from TMDB and get the results in json format

        if not results:
            not_found = "Фильм не найден." if user_lang == "RU" else "No movies found."
            bot.send_message(message.chat.id, not_found)
            return
        #analyze the result
        movie = results[0]
        
        genres_dict_ru = {                                                  
            28: "Боевик", 12: "Приключения", 16: "Мультфильм", 35: "Комедия",
            80: "Криминал", 99: "Документальный", 18: "Драма", 10751: "Семейный",
            14: "Фэнтези", 36: "История", 27: "Ужасы", 10402: "Музыка",
            9648: "Детектив", 10749: "Мелодрама", 878: "Фантастика", 10770: "Телефильм",
            53: "Триллер", 10752: "Военный", 37: "Вестерн"
        }
        
        genres_dict_en = {
            28: "Action", 12: "Adventure", 16: "Animation", 35: "Comedy",
            80: "Crime", 99: "Documentary", 18: "Drama", 10751: "Family",
            14: "Fantasy", 36: "History", 27: "Horror", 10402: "Music",
            9648: "Mystery", 10749: "Romance", 878: "Science Fiction", 10770: "TV Movie",
            53: "Thriller", 10752: "War", 37: "Western"
        }

    
        if user_lang == "RU":
            genre_ids = movie.get('genre_ids', [])
            genre_names = [genres_dict_ru.get(genre_id, 'Unknown') for genre_id in genre_ids]
            genre_text = ', '.join(genre_names) if genre_names else 'N/A'
        else:
            genre_ids = movie.get('genre_ids', [])
            genre_names = [genres_dict_en.get(genre_id, 'Unknown') for genre_id in genre_ids]
            genre_text = ', '.join(genre_names) if genre_names else 'N/A'
        #in this two blocks we translate genre IDs from TMDB into readable genre names

        title = movie.get('title', 'N/A')
        release_date = movie.get('release_date', 'N/A')
        year = release_date.split('-')[0] if release_date and release_date != 'N/A' else 'N/A'
        plot = movie.get('overview', 'N/A')
        rating = movie.get('vote_average', 'N/A')
        poster_path = movie.get('poster_path', 'N/A')
        id = movie.get('id')
        #There we unpacked the data from the json response and get the title, year, plot, rating, poster path and id of the movie

        artists_url = f"https://api.themoviedb.org/3/movie/{id}/credits?api_key={TMDB_API_KEY}&language={tmdb_lang}"
        artists_response = requests.get(artists_url)
        zhopa = artists_response.json()
        
        sanya_pidor = zhopa.get('cast', [])
        gondonio = zhopa.get('crew', [])

        cast  = [person.get('name', 'N/A') for person in sanya_pidor] if sanya_pidor else 'N/A'
        huila = [person.get('name', 'N/A') for person in gondonio if person.get('job') == 'Director'] if gondonio else 'N/A'
        #there we make another request to TMDB to get the cast of the movie by using the id of the movie and unpack 

        search_title = title.replace(' ', '+')
        
        if rating != 'N/A':
            rating = round(rating, 1) # Round the rating to one decimal place 7.67 -> 7.7  ыыыыы сикс севен

        if user_lang == "RU":
            response_text = f"\nНазвание: {title}\n\nГод: {year}\n\nЖанр: {genre_text}\n\nРежисер: {', '.join(huila[:2])}\n\nАктеры: {', '.join(cast[:5])}\n\nОписание: {plot}\n\n⭐ Рейтинг TMDb: {rating}/10 \n\n🍿[Смотреть сериал в HD](https://www.google.com/search?q={search_title}+{year}+смотреть+онлайн+бесплатно+hd)\n\n [Смотреть Трейлер](https://www.youtube.com/results?search_query={search_title}+{year}+трейлер) "
            bot.send_photo(message.chat.id , f"https://image.tmdb.org/t/p/w500{poster_path}") 
        else:
            response_text = f"\nTitle: {title}\n\nYear: {year}\n\nGenre: {genre_text}\n\nDirector: {', '.join(huila[:2])}\n\nCast: {', '.join(cast[:5])}\n\nPlot: {plot}\n\n⭐ Rating TMDb: {rating}/10 \n\n🍿  [Watch in  HD](https://www.google.com/search?q={search_title}+{year}+смотреть+онлайн+бесплатно+hd)\n\n [Watch Trailer](https://www.youtube.com/results?search_query={search_title}+{year}+трейлер)"
            bot.send_photo(message.chat.id , f"https://image.tmdb.org/t/p/w500{poster_path}")
            #This few lines to correct the message and add poster to movie before send also I added a link immediately to the ready player but the fuckig google blocked it so user should find player by himself, additonally i add a link to trailer
     
        bot.send_message(message.chat.id, response_text, parse_mode='Markdown', disable_web_page_preview=True)
    

    elif state == "FIND_TV_SHOW": # In this part we do the same as in the previous block but for series
        text = message.text.lower()
    
        user_lang = user_languages.get(message.chat.id, "EN")
    
        tmdb_lang = "ru-RU" if user_lang == "RU" else "en-US"

        wait_text = "Секунду, ищу сериал..." if user_lang == "RU" else "Please wait, it can take few seconds..."
        bot.send_message(message.chat.id, wait_text)
        
        url = f"https://api.themoviedb.org/3/search/tv?api_key={TMDB_API_KEY}&query={text}&language={tmdb_lang}"
       

        response = requests.get(url)
        data = response.json()

        results = data.get('results', [])

        if not results:
            not_found = "Сериал не найден." if user_lang == "RU" else "No TV shows found."
            bot.send_message(message.chat.id, not_found)
            return

        show = results[0]
        
        genres_dict_ru = {
            10759: "Боевик и приключения", 16: "Мультфильм", 35: "Комедия",
            80: "Криминал", 99: "Документальный", 18: "Драма", 10751: "Семейный",
            10762: "Детский", 9648: "Детектив", 10763: "Новости", 10764: "Реальное ТВ",
            10765: "Фантастика и фэнтези", 10766: "Мелодрама", 10767: "Ток-шоу"
        }
        
        genres_dict_en = {
            10759: "Action & Adventure", 16: "Animation", 35: "Comedy",
            80: "Crime", 99: "Documentary", 18: "Drama", 10751: "Family",
            10762: "Kids", 9648: "Mystery", 10763: "News", 10764: "Reality",
            10765: "Sci-Fi & Fantasy", 10766: "Soap", 10767: "Talk"
        }

        if user_lang == "RU":
                genre_ids = show.get('genre_ids', [])
                genre_names = [genres_dict_ru.get(genre_id, 'Unknown') for genre_id in genre_ids]
                genre_text = ', '.join(genre_names) if genre_names else 'N/A'
        else:
                genre_ids = show.get('genre_ids', [])
                genre_names = [genres_dict_en.get(genre_id, 'Unknown') for genre_id in genre_ids]
                genre_text = ', '.join(genre_names) if genre_names else 'N/A'

        title = show.get('name', 'N/A')
        release_date = show.get('first_air_date', 'N/A')
        year = release_date.split('-')[0] if release_date and release_date != 'N/A' else 'N/A'
        plot = show.get('overview', 'N/A')
        rating = show.get('vote_average', 'N/A')
        poster_path = show.get('poster_path', 'N/A')
        id = show.get('id')

        artists_url = f"https://api.themoviedb.org/3/tv/{id}/credits?api_key={TMDB_API_KEY}&language={tmdb_lang}"
        artists_response = requests.get(artists_url)
        zhopa = artists_response.json()

        sanya_pidor = zhopa.get('cast', [])
        gondonio = zhopa.get('crew', [])

        cast  = [person.get('name', 'N/A') for person in sanya_pidor] if sanya_pidor else 'N/A'
        huila = [person.get('name', 'N/A') for person in gondonio if person.get('job') == 'Director'] if gondonio else 'N/A'

        search_title = title.replace(' ', '+')
            
        if rating != 'N/A':
            rating = round(rating, 1)

        if user_lang == "RU":
            response_text = f"\nНазвание: {title}\n\nГод: {year}\n\nЖанр: {genre_text}\n\nРежисер: {', '.join(huila[:2])}\n\nАктеры: {', '.join(cast[:5])}\n\nОписание: {plot}\n\n⭐ Рейтинг TMDb: {rating}/10 \n\n🍿 [Смотреть сериал в HD](https://www.google.com/search?q={search_title}+{year}+смотреть+онлайн+бесплатно+hd)\n\n [Смотреть Трейлер](https://www.youtube.com/results?search_query={search_title}+{year}+трейлер)"
            bot.send_photo(message.chat.id , f"https://image.tmdb.org/t/p/w500{poster_path}")    
        else:
            response_text = f"\nTitle: {title}\n\nYear: {year}\n\nGenre: {genre_text}\n\nDirector: {', '.join(huila[:2])}\n\nCast: {', '.join(cast[:5])}\n\nPlot: {plot}\n\n⭐ Rating TMDb: {rating}/10 \n\n🍿 [Watch in  HD](https://www.google.com/search?q={search_title}+{year}+смотреть+онлайн+бесплатно+hd)\n\n [Watch Trailer](https://www.youtube.com/results?search_query={search_title}+{year}+трейлер)"
            bot.send_photo(message.chat.id , f"https://image.tmdb.org/t/p/w500{poster_path}")
        
        bot.send_message(message.chat.id, response_text, parse_mode='Markdown', disable_web_page_preview=True)


bot.polling(none_stop=True)               