import csv
from pandas import options
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_imdb():
    print("Starting IMDb scraping for 2024 movies...")
    options = Options()
   # options.add_argument("--headless")
    
    # Essential: Add a real browser User-Agent
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# Add these to make the window look less like a bot
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options)
    url = "https://www.imdb.com/search/title/?title_type=feature&release_date=2024-01-01,2024-12-31"
    print(f"Accessing URL: {url}")
    movie_data = []
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 35)
        containers = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item")))

        for container in containers:
            try:
                print("Processing a movie container...", container.get_attribute("outerHTML")[:200])  # Print the first 200 characters of the container for debugging
                name = container.find_element(By.CSS_SELECTOR, "h3.ipc-title__text").text.split('. ', 1)[-1]
                try:
                    print("Found storyline for the movie.")
                    plot = container.find_element(By.CSS_SELECTOR, "div.ipc-html-content-inner-div").text
                    print(f"Plot: {plot[:100]}...")  # Print the first 100 characters of the plot for debugging
                except:
                    print("No storyline found for this movie.")
                    plot = "No storyline available"
                movie_data.append([name, plot])
            except:
                continue

        with open('data/imdb_2024_movies.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Movie Name", "Storyline"])
            writer.writerows(movie_data)
        print("Scraping complete. Data saved to data/imdb_2024_movies.csv")

    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_imdb()