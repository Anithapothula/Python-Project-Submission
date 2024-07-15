import pandas as pd
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import time

def get_driver():
    options = Options()
    options.headless = True
    service = Service(executable_path='C:\\Users\\appothul\\Desktop\\appothul\\Python\\capestone\\chromedriver.exe')  
    try:
        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except WebDriverException as e:
        print(f"Error initializing the WebDriver: {e}")
        return None

def fetch_movie_data(genre):
    driver = get_driver()
    if driver is None:
        print("Failed to initialize the WebDriver.")
        return None

    url = f"https://www.imdb.com/search/title/?genres={genre}"  
    driver.get(url)
    time.sleep(5)  

    movies = []
    try:
        movie_elements = driver.find_elements(By.CSS_SELECTOR, 'h3.ipc-title__text')
        for element in movie_elements:
            try:
                title = element.text.strip()  
                if title:  
                    movies.append(title)
            except NoSuchElementException as e:
                print(f"Error finding movie title: {e}")
    except NoSuchElementException as e:
        print(f"Error finding movie elements: {e}")
    finally:
        driver.quit()

    return movies

def save_to_csv(movies, genre):
    df = pd.DataFrame({'title': movies})
    df.to_csv(f'{genre}_movies.csv', index=False)

def suggest_random_movie(movies):
    if not movies:
        return None
    return random.choice(movies)

def main():
    genre = input("Enter the interested genre of movies: ").strip().lower()
    movies = fetch_movie_data(genre)
    if movies:
        save_to_csv(movies, genre)
        suggestion = suggest_random_movie(movies)
        if suggestion:
            print(f"Recommended movie: {suggestion}")
        else:
            print("No valid movie titles found.")
    else:
        print("No data fetched.")

if __name__ == "__main__":
    main()
