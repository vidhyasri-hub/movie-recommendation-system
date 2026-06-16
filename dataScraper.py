import csv
from pandas import options
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def scrape_imdb_more():
    print("Starting IMDb scraping for 2024 movies...")
    options = Options()
    
    # Essential: Add a real browser User-Agent
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options)

    url = (
        "https://www.imdb.com/search/title/"
        "?title_type=feature"
        "&release_date=2024-01-01,2024-12-31"
    )

    driver.get(url)

    wait = WebDriverWait(driver, 20)

    try:

        while True:

            try:

                # Wait until button visible
                load_more = wait.until(
                    EC.element_to_be_clickable(
                        (
                            By.XPATH,
                            "//button[contains(.,'Load more')]"
                        )
                    )
                )

                driver.execute_script(
                    "arguments[0].scrollIntoView();",
                    load_more
                )

                time.sleep(2)

                load_more.click()

                print("Loaded more movies")

                time.sleep(4)

            except TimeoutException:

                print("No more Load More button")
                break

        # AFTER ALL MOVIES ARE LOADED

        containers = driver.find_elements(
            By.CSS_SELECTOR,
            "li.ipc-metadata-list-summary-item"
        )

        movie_data = []

        for movie in containers:

            try:

                name = (
                    movie
                    .find_element(
                        By.CSS_SELECTOR,
                        "h3.ipc-title__text"
                    )
                    .text
                    .split(". ", 1)[-1]
                )

                try:

                    plot = movie.find_element(
                        By.CSS_SELECTOR,
                        "div.ipc-html-content-inner-div"
                    ).text

                except:

                    plot = (
                        "No storyline available"
                    )

                movie_data.append(
                    [name, plot]
                )

            except Exception:
                continue

        with open(
            "data/imdb_2024_movies.csv",
            "w",
            newline="",
            encoding="utf-8"
        ) as f:

            writer = csv.writer(f)

            writer.writerow(
                [
                    "Movie Name",
                    "Storyline"
                ]
            )

            writer.writerows(movie_data)

        print(
            f"Saved {len(movie_data)} movies"
        )

    finally:

        driver.quit()


if __name__ == "__main__":
    scrape_imdb_more()