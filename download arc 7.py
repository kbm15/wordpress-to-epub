import requests
from bs4 import BeautifulSoup
import os

# Starting URL of the webpage to be crawled
url = "https://witchculttranslation.com/2021/01/23/arc-7-chapter-1-initiation/"

# Number of times to crawl the website
n = 115

# Image counter for dynamic filename
img_cnt = 1

for i in range(n):
	# Send a GET request to the URL and store the response
	response = requests.get(url)

	# Use BeautifulSoup to parse the HTML content of the response
	soup = BeautifulSoup(response.content, 'html.parser')

	# Find the first <p> tag with id="L69" and style="text-align: center;"
	p_tag = soup.find('p', {'id': 'L69', 'style': 'text-align: center;'})

	# Find the parent <article> tag of the <p> tag
	article_tag = p_tag.find_parent('article')

	# Extract the text between the <p> tag and </article> tag
	paragraphs = article_tag.find_all('p')
	start_tag = article_tag.find('p', {'id': 'L69', 'style': 'text-align: center;'})

	# Extract the filename from the URL
	chapter_words = url.split('/')[-2].split('-')[2:]
	chapter_name = ''
	for word in chapter_words:
		chapter_name += word
		chapter_name += ' '
	chapter_name = chapter_name[:-1]

	# Save the text to a file with the filename as the last string of the path after "/"
	with open("Arc_7.html", 'a', encoding="utf-8")  as f:
		can_write = False
		f.write("<h1>" + chapter_name + "</h1>\n")
		for paragraph in paragraphs:		
			if can_write: 
				if paragraph.find('img'): 
					image = paragraph.select('img') [0]
					if image.get('srcset'): image_url = image.get('srcset').split(' ')[-2]
					else: image_url = image['src'] 
					img_data = requests.get(image_url).content
					img_headers =  requests.get(image_url).headers['content-type']
					img_ext = "." + str(img_headers.split('/')[-1])
					with open("pictures/" + str(img_cnt) + img_ext, 'wb') as handler: 
						handler.write(img_data) 		
					f.write("<p><img src=\"pictures/" + str(img_cnt) + img_ext + "\"/></p>")
					img_cnt+=1
				else: f.write(str(paragraph) + "\n")
			if paragraph == start_tag: can_write = True
	if i < n:
		# Find the URL under the <div class="nav-next"> tag and update the URL variable
		next_link = soup.find('div', {'class': 'nav-next'}).find('a')['href']
		url = next_link
