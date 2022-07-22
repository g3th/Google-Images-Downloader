import requests
import concurrent.futures
import os
import shutil
import sys
import header
import time

from pathlib import Path
from bs4 import BeautifulSoup as soup

class Google_image_Downloader:

	def __init__(self):
		
		self.file_path = str(Path(__file__).parent)
		self.user_input = str(input('Enter search query: '))
		self.query = self.user_input.replace(' ','+')
		self.image_list = []
		self.links = []
		self.blacklist = ['google','twitter','facebook','instagram','youtube'] #cancer
		self.index = 0
		self.page_start_index = 0
		self.image_page = 0
		self.progress_bar = '+'
		
	def initial_request(self):
		page = 'https://www.google.co.uk/search?gbv=1&tbm=isch&q='+self.query+'&tbs=ift:jpg&start='+str(self.page_start_index)
		while self.image_page < 5: 										
			request = requests.get(page)
			request.encoding = 'utf-8'
			fetch = soup(request.content,'html.parser')
			find_links = fetch.find_all('a',href=True)
			for i in find_links:
				if 'https' in str(i) and not any(word in str(i) for word in self.blacklist):
					self.image_list.append(str(i).split('=')[2].split('&amp')[0])
			#self.image_list = list(dict.fromkeys(self.image_list))
			self.image_page += 1
			self.page_start_index += 20

	def fetch_images(self):
		self.initial_request()
		while self.index < len(self.image_list):
			try:
				progress_bar = round(self.index / len(self.image_list) * 100, 1)
				sys.stdout.write('Fetching URLs - Progress : '+ str(progress_bar)+'%')
				links_request = requests.get(self.image_list[self.index], timeout = 8)
				fetch_links = soup(links_request.content,'html.parser')
				link_images = fetch_links.find('meta', attrs={'property':'og:image'})
				if link_images == None:
					link_images = fetch_links.find_all('a',{'class':'image-link'})
					for image in link_images:
						if '.jpg' or '.jpeg' in str(i):
							self.links.append(image['href'])				
				else:
					self.links.append(link_images['content'])	
								
			except Exception as e:#(TypeError, requests.exceptions.ReadTimeout, requests.exceptions.MissingSchema,requests.exceptions.SSLError):			
				print('\n {} \n'.format(e))
			sys.stdout.flush()
			sys.stdout.write('\033[2K\033[1G')
			self.index +=1
				
	def download_image(self, image_link, filename, iterator_index, len_of_image_list):		
		get_content = requests.get(self.links[image_link]).content
		with open (self.file_path+'/Downloaded_Images/image'+str(filename)+'.jpg', 'wb') as image:
			image.write(get_content)
			progress_bar = round(iterator_index / len(image_list) * 100, 1)
			sys.stdout.write('Downloading Images - Progress : '+ str(progress_bar)+'%')
			sys.stdout.flush()
			sys.stdout.write('\033[2K\033[1G')
	def multi_threaded_downloads(self):
		try:
			os.mkdir('Downloaded_Images')
		except FileExistsError:
			shutil.rmtree('Downloaded_Images')
			os.mkdir('Downloaded_Images')
		filename = 0
		with concurrent.futures.ThreadPoolExecutor() as executor:
			for image in range(len(self.links)):				
				executor.submit(self.download_image, filename, image, image, len(self.links))								
				filename +=1
				
header.header()
downloader = Google_image_Downloader()
downloader.fetch_images()
downloader.multi_threaded_downloads()
