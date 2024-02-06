from fastapi import FastAPI, HTTPException
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

app = FastAPI()
firefox_options = Options()
firefox_options.add_argument('--headless')
driver = webdriver.Firefox(options=firefox_options)

def clean_url(url):
    if url.startswith("https://"):
        url = url[len("https://"):]
    if url.startswith("www."):
        url = url[len("www."):]
    if url.endswith("/"):
        url = url[:-1]
    return url

def capture_screenshot(url):
    url="https://www.javatpoint.com/"
    try:
        driver.get(url)
        image_path = clean_url(url)
        driver.save_screenshot(f"{image_path}.png")
        absolute_path = os.path.abspath(image_path)
        print(f"The absolute path of the image is: {absolute_path}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to capture screenshot: {str(e)}")

@app.get("/screenshot/{url}")
async def get_screenshot(url: str):
    try:
        capture_screenshot(url)
        return {"message": f"Screenshot captured for {url}"}
    finally:
        driver.quit()

@app.get("/")
async def home():
    return {"message":"yes"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

    '''uvicorn your_filename:app --reload'''
