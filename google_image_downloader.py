import requests
import concurrent.futures
import time
from bs4 import BeautifulSoup as soup
print('\x1bc')
class fetching_images:

	def __init__(self):
	
		self.user_input = str(input('Enter search query: '))
		self.query = self.user_input.replace(' ','+')
		self.image_list = []
		self.links = []
		self.blacklist = ['google','twitter','facebook','instagram','youtube']
		self.wordlist = ['.jpg','.jpeg']
		self.index = 0
		self.page_start_index = 0
		self.image_page = 0
		
	def initial_request(self):
		page = 'https://www.google.co.uk/search?gbv=1&tbm=isch&q='+self.query+'&tbs=ift:jpg&start='+str(self.page_start_index)
		print(page)
		while self.image_page < 2:
			request = requests.get(page)
			fetch = soup(request.content,'html.parser')
			find_links = fetch.find_all('a',href=True)
			for i in find_links:
				if 'https' in str(i) and not any(word in str(i) for word in self.blacklist):
					self.image_list.append(str(i).split('=')[2].split('&amp')[0])
			self.image_list = list(dict.fromkeys(self.image_list))
			self.image_page += 1
			self.page_start_index += 20

	def fetch_images(self):
		print(self.initial_request())
		while self.index < len(self.image_list):
			try:
				print('Fetching original image at address {}'.format(self.image_list[self.index]))
				links_request = requests.get(self.image_list[self.index], timeout = 8)
				fetch_links = soup(links_request.content,'html.parser')
				link_images = fetch_links.find('meta', attrs={'property':'og:image'})
				self.links.append(link_images['content'])
				self.index +=1
				
			except Exception as e:#(TypeError, requests.exceptions.ReadTimeout, requests.exceptions.MissingSchema,requests.exceptions.SSLError):
			
				print(e)
				self.index +=1
			time.sleep(0.8)		
			
		return self.links


image = fetching_images()
print(image.fetch_images())
