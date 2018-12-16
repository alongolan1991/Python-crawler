from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
import re
import sys

# Connect to mongodb
import connectdb


# Open the file that includes the links from imdb
with open('links.txt', 'r') as file:
    lines = file.read().splitlines()
    for j in lines:
        # Getting html page that includes 50 items
        html = urlopen('https://imdb.com/' + j)
        print('https://imdb.com/' + j)
        soup = BeautifulSoup(html.read())
        record = soup.find_all(
            "div",  {"class": ["lister-item", "mode-advanced"]})
        # recor
        for k in record:
            # my_index is the uniqe index for movie
            my_index = k.find(
                "span", {"class": ["lister-item-index", "unbold text-primary"]}).text
            Movie_index = str(my_index.split(".")[0])
            Movie_index = Movie_index.replace(",", '')
            Movie_index = int(Movie_index)
            print(Movie_index)
            # link_to_movie is direct link to movie record
            link_to_movie = k.find("a")['href']
            link_to_movie = "https://imdb.com" + str(link_to_movie)
            # print("Movie link: " + link_to_movie)
            movie_record = urlopen(link_to_movie)
            parsed_movie_record = BeautifulSoup(movie_record.read())
            # split the date from the name of the movie
            movie_name = parsed_movie_record.find(
                "div", {"class": "title_wrapper"}).find('h1').text
            pasred_movie_name = movie_name.split("(")[0]
            pasred_movie_name = pasred_movie_name.replace("\xa0", '')
            # print("Movie name: " + pasred_movie_name)
            # getting the year of the movie
            try:
                release_date = movie_name.split("(")[1]
                release_date = release_date.split(")")[0]
            except AttributeError:
                release_date = "None"
                pass
            except IndexError:
                release_date = "None"
                pass

            # print("Release date: " + release_date)
            # bring the movie rating
            try:
                movie_rating = parsed_movie_record.find(
                    "span", {"itemprop": "ratingValue"}).text
                # print("Movie rating: " + str(movie_rating))
            except AttributeError:
                movie_rating = "None"
                # print("Movie rating: None")
                pass
            # bring the run time
            try:
                Real_run_time = "None"
                movie_detail = parsed_movie_record.find(
                    "div", {"id": "titleDetails"})
                Run_time = movie_detail.find("time").text
                Real_run_time = Run_time.split(" ")[0]
                # print("Run Time: " + Real_run_time)
            except AttributeError:
                # print("Run Time: None")
                pass
            # bring the budget
            budget = "None"
            try:
                ways_to_budget = movie_detail.find_all(
                    "div", {"class": "txt-block"})
                for way in ways_to_budget:
                    if(way.find("h4").text == "Budget:"):
                        m = way.text
                        m = re.findall(r'\d', m)
                        budget = ''.join(m)
                        break
            except AttributeError:
                pass
            # print("Budget: " + budget)
            # bring the movie ganers
            ganer_list = []
            movie_story_line = parsed_movie_record.find(
                "div", {"id": "titleStoryLine"})
            try:
                ganer = movie_story_line.select("div.see-more.inline.canwrap")
                for gan in ganer:
                    if(gan.find("h4").text == "Genres:"):
                        all_links_ganers = gan.find_all("a")
                        for gane in all_links_ganers:
                            ganer_list.append(gane.text.split(" ")[1])
            except AttributeError:
                pass
            # sys.stdout.write("Ganers: ")
            # print(*ganer_list, sep=", ")
            # bring the story line
            Real_story_line = "None"
            try:
                my_story_line = movie_story_line.find(
                    'div', {'class': ['inline', 'canwrap']}).find('span', {"class": None}).text
                Real_story_line = my_story_line.lstrip()
            except AttributeError:
                pass
            # print("Story line: " + Real_story_line)
            # bring the case list
            cast_list = []
            try:
                cast_table = parsed_movie_record.find(
                    "table", {"class": "cast_list"})
                cast = cast_table.find_all("td", {"class": None})
                for ca in cast:
                    temp = ca.find("a").text.split(" ", 1)[1]
                    cast_list.append(temp.split("\n")[0])

                # sys.stdout.write("Cast: ")
                # print(*cast_list, sep=", ")
            except AttributeError:
                pass
            # bring the movie director and writter
            Director = "None"
            Writer = "None"
            credit = parsed_movie_record.find_all(
                "div", {"class": "credit_summary_item"})
            for cred in credit:
                if(cred.find("h4").text == "Director:" or cred.find("h4").text == "Directors:"):
                    Director = cred.find("a").text
                if(cred.find("h4").text == "Writers:" or cred.find("h4").text == "Writer:"):
                    Writer = cred.find("a").text

            # print("Director: " + Director)
            # print("Writter: " + Writer)
            Item = {
                "movie_id": Movie_index, #Number
                "link": link_to_movie,
                "name": pasred_movie_name,
                "release_date": release_date,
                "rating": movie_rating,
                "runtime": Real_run_time,
                "budget": budget,
                "genres": ganer_list,
                "cast": cast_list, #Array
                "writer": Writer,
                "director": Director,
                "story_line": Real_story_line,
                "sex": False, #Boolean
                "violence": False #Boolean
            }

            # print("Json----" * 100)
            # print(Item)
            connectdb.pushRECORD(Item)
            # print("-" * 100)
print("Finished mother fucker !")

            
