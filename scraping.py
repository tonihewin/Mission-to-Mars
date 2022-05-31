{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "006d68b8",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "[WDM] - ====== WebDriver manager ======\n",
      "[WDM] - Current google-chrome version is 101.0.4951\n",
      "[WDM] - Get LATEST chromedriver version for 101.0.4951 google-chrome\n",
      "[WDM] - Driver [C:\\Users\\tlhch\\.wdm\\drivers\\chromedriver\\win32\\101.0.4951.41\\chromedriver.exe] found in cache\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "{'news_title': 'NASA Wins Two Emmy Awards for Interactive Mission Coverage', 'news_paragraph': \"NASA-JPL's coverage of the Mars InSight landing earns one of the two wins, making this the NASA center's second Emmy.\", 'featured_image': 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/image/featured/mars1.jpg', 'facts': '<table border=\"1\" class=\"dataframe table table-striped\">\\n  <thead>\\n    <tr style=\"text-align: right;\">\\n      <th></th>\\n      <th>Mars</th>\\n      <th>Earth</th>\\n    </tr>\\n    <tr>\\n      <th>Description</th>\\n      <th></th>\\n      <th></th>\\n    </tr>\\n  </thead>\\n  <tbody>\\n    <tr>\\n      <th>Mars - Earth Comparison</th>\\n      <td>Mars</td>\\n      <td>Earth</td>\\n    </tr>\\n    <tr>\\n      <th>Diameter:</th>\\n      <td>6,779 km</td>\\n      <td>12,742 km</td>\\n    </tr>\\n    <tr>\\n      <th>Mass:</th>\\n      <td>6.39 × 10^23 kg</td>\\n      <td>5.97 × 10^24 kg</td>\\n    </tr>\\n    <tr>\\n      <th>Moons:</th>\\n      <td>2</td>\\n      <td>1</td>\\n    </tr>\\n    <tr>\\n      <th>Distance from Sun:</th>\\n      <td>227,943,824 km</td>\\n      <td>149,598,262 km</td>\\n    </tr>\\n    <tr>\\n      <th>Length of Year:</th>\\n      <td>687 Earth days</td>\\n      <td>365.24 days</td>\\n    </tr>\\n    <tr>\\n      <th>Temperature:</th>\\n      <td>-87 to -5 °C</td>\\n      <td>-88 to 58°C</td>\\n    </tr>\\n  </tbody>\\n</table>', 'last_modified': datetime.datetime(2022, 5, 31, 2, 55, 15, 125574)}\n"
     ]
    }
   ],
   "source": [
    "# Import Splinter, BeautifulSoup, and Pandas\n",
    "from splinter import Browser\n",
    "from bs4 import BeautifulSoup as soup\n",
    "import pandas as pd\n",
    "import datetime as dt\n",
    "from webdriver_manager.chrome import ChromeDriverManager\n",
    "\n",
    "\n",
    "def scrape_all():\n",
    "    # Initiate headless driver for deployment\n",
    "    executable_path = {'executable_path': ChromeDriverManager().install()}\n",
    "    browser = Browser('chrome', **executable_path, headless=True)\n",
    "\n",
    "    news_title, news_paragraph = mars_news(browser)\n",
    "\n",
    "    # Run all scraping functions and store results in a dictionary\n",
    "    data = {\n",
    "        \"news_title\": news_title,\n",
    "        \"news_paragraph\": news_paragraph,\n",
    "        \"featured_image\": featured_image(browser),\n",
    "        \"facts\": mars_facts(),\n",
    "        \"last_modified\": dt.datetime.now()\n",
    "    }\n",
    "\n",
    "    # Stop webdriver and return data\n",
    "    browser.quit()\n",
    "    return data\n",
    "\n",
    "\n",
    "def mars_news(browser):\n",
    "\n",
    "    # Scrape Mars News\n",
    "    # Visit the mars nasa news site\n",
    "    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'\n",
    "    browser.visit(url)\n",
    "\n",
    "    # Optional delay for loading the page\n",
    "    browser.is_element_present_by_css('div.list_text', wait_time=1)\n",
    "\n",
    "    # Convert the browser html to a soup object and then quit the browser\n",
    "    html = browser.html\n",
    "    news_soup = soup(html, 'html.parser')\n",
    "\n",
    "    # Add try/except for error handling\n",
    "    try:\n",
    "        slide_elem = news_soup.select_one('div.list_text')\n",
    "        # Use the parent element to find the first 'a' tag and save it as 'news_title'\n",
    "        news_title = slide_elem.find('div', class_='content_title').get_text()\n",
    "        # Use the parent element to find the paragraph text\n",
    "        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()\n",
    "\n",
    "    except AttributeError:\n",
    "        return None, None\n",
    "\n",
    "    return news_title, news_p\n",
    "\n",
    "\n",
    "def featured_image(browser):\n",
    "    # Visit URL\n",
    "    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'\n",
    "    browser.visit(url)\n",
    "\n",
    "    # Find and click the full image button\n",
    "    full_image_elem = browser.find_by_tag('button')[1]\n",
    "    full_image_elem.click()\n",
    "\n",
    "    # Parse the resulting html with soup\n",
    "    html = browser.html\n",
    "    img_soup = soup(html, 'html.parser')\n",
    "\n",
    "    # Add try/except for error handling\n",
    "    try:\n",
    "        # Find the relative image url\n",
    "        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')\n",
    "\n",
    "    except AttributeError:\n",
    "        return None\n",
    "\n",
    "    # Use the base url to create an absolute url\n",
    "    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'\n",
    "\n",
    "    return img_url\n",
    "\n",
    "def mars_facts():\n",
    "    # Add try/except for error handling\n",
    "    try:\n",
    "        # Use 'read_html' to scrape the facts table into a dataframe\n",
    "        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]\n",
    "\n",
    "    except BaseException:\n",
    "        return None\n",
    "\n",
    "    # Assign columns and set index of dataframe\n",
    "    df.columns=['Description', 'Mars', 'Earth']\n",
    "    df.set_index('Description', inplace=True)\n",
    "\n",
    "    # Convert dataframe into HTML format, add bootstrap\n",
    "    return df.to_html(classes=\"table table-striped\")\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "\n",
    "    # If running as script, print scraped data\n",
    "    print(scrape_all())\n",
    "    \n",
    "    \n",
    "def hemisphere(browser):\n",
    "    # 1. Use browser to visit the URL \n",
    "    url = 'https://marshemispheres.com/'\n",
    "    browser.visit(url)\n",
    "    \n",
    "    # 2. Create a list to hold the images and titles.\n",
    "    hemisphere_image_urls = []\n",
    "    \n",
    "     #items = browser.find_by_css('a.product-item h3')\n",
    "        \n",
    "     # 3. Write code to retrieve the image urls and titles for each hemisphere.\n",
    "    for i in range(4):\n",
    "        #create empty dictionary\n",
    "        #hemispheres = {}\n",
    "        browser.find_by_css('a.product-item h3')[i].click()\n",
    "        #element = browser.find_link_by_text('Sample').first\n",
    "        #img_url = element['href']\n",
    "        #title = browser.find_by_css(\"h2.title\").text\n",
    "        #hemispheres[\"img_url\"] = img_url\n",
    "        #hemispheres[\"title\"] = title\n",
    "        hemisphere_data = scrape_hemisphere(browser.html)\n",
    "        hemisphere_image_urls.append(hemisphere_data)\n",
    "        browser.back()\n",
    "    return hemisphere_image_urls\n",
    "\n",
    "\n",
    "def scrape_hemisphere(html_text):\n",
    "    # parse html text\n",
    "    hemi_soup = soup(html_text, \"html.parser\")\n",
    "    # adding try/except for error handling\n",
    "    try:\n",
    "        title_elem = hemi_soup.find(\"h2\", class_=\"title\").get_text()\n",
    "        sample_elem = hemi_soup.find(\"a\", text=\"Sample\").get(\"href\")\n",
    "    except AttributeError:\n",
    "        # Image error will return None, for better front-end handling\n",
    "        title_elem = None\n",
    "        sample_elem = None\n",
    "    hemispheres = {\n",
    "        \"title\": title_elem,\n",
    "        \"img_url\": sample_elem\n",
    "    }\n",
    "    return hemispheres\n",
    "\n",
    "\n",
    "    \n",
    "    \n",
    "    \n",
    "    \n",
    "\n",
    "\n",
    "    \n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "67aa7cd4",
   "metadata": {},
   "outputs": [],
   "source": [
    "# browser.find_by_css('a.product-item h3')[0].click()\n",
    "# element = browser.find_link_by_text('Sample').first\n",
    "# print(element['href'])\n",
    "# browser.find_by_css(\"h2.title\").text"
   ]
  }
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "eb2e28f0",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
