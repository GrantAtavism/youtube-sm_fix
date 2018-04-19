import os
import time

from threading import Thread
from .sock import (
	download_xml,
	download_html)
from .tools import (
	Progress,
	type_id)



def html_init(path):
	"""To init the html file"""
	open('sub.html', 'w').write("""<html>
	<head>
		<meta charset="utf-8" />
		<link rel="stylesheet" href="css/sub.css" />
		<link rel="stylesheet" media="screen and (max-width: 1081px)" href="css/sub_mobile.css"/>
		<title>Abonnements</title>
	</head>
	<body>
<!-- {} -->
""".format(time.ctime()))

def init(urls, min_date, path='', mode='html', loading=False, method=0):
	"""Run all the analyze in a thread"""
	threads = []
	ending = 0
	nb = len(urls)
	if loading:
		prog = Progress(nb)
		prog.progress_bar()
	if method == '0':
		for url in urls:
			if loading:
				thr = Analyzer(mode, url, min_date, method, path, prog)
			else:
				thr = Analyzer(mode, url, min_date, method, path)
			thr.Thread()
			threads.append(thr)
			thr.start()
		for i in threads:
			i.join()
	elif method == '1':
		for i in range(nb):
			if loading:
				thr = Analyzer(mode, urls[i], min_date, method, path, prog)
			else:
				thr = Analyzer(mode, urls[i], min_date, method, path)
			thr.Thread()
			threads.append(thr)
			thr.start()
			if i%50 == 0 or nb == i+1:
				for y in threads:
					y.join()
				threads = []
	if loading and prog.xmin != prog.xmax:
		prog.xmin = prog.xmax
		prog.progress_bar()


class Analyzer(Thread):
	"""It's a group of fonctions to recup the videos informations"""
	def __init__(self, mode='', url_id='', min_date='', method='0', path='', prog=None):
		self.mode = mode
		# self.method is the way you're going to recv the data (0 -> RSS, 1 -> https://youtube.com/channel/{id}/videos) 
		self.method = method
		self.id = url_id
		self.path_cache = path
		self.min_date = min_date
		self.type = self._type_id()
		#all the var user in class
		self.url = ""
		self.url_channel = ""
		self.title = ""
		self.channel = ""
		self.date = ""
		self.data_file = ""
		#Progress
		self.prog = prog

	def Thread(self):
		Thread.__init__(self)

	def run(self):
		self.analyzer_sub()
		if self.prog != None:
			self.prog.add()

	def _type_id(self):
		return type_id(self.id)

	def _download_page(self):
		if self.method == '0':
			return download_xml(self.id, self.type)
		elif self.method == '1':
			return download_html(self.id, self.type)
		else:
			return None

	def analyzer_sub(self):
		"""Recover all the videos of a channel or a playlist
		and add the informations in $HOME/.cache/youtube_sm/data/."""
		linfo = self._download_page()
		if linfo == False or linfo == None:
			return
		try:
			os.mkdir(self.path_cache + 'data/' + self.method)
		except:
			pass
		if self.method == '0':
			for i in linfo:
				date = int(i.split("<published>")[1].split("</published>")[0].replace('-', '').replace('+00:00', '').replace('T', '').replace(':', ''))
				if self.min_date <= date:
					self.info_recup_rss(i)
					self.write()
		elif self.method == '1':
			if self.type: #Channel
				try:
					self.channel = linfo[0].split('<title>')[1].split('\n')[0]
				except IndexError:
					pass
				except:
					pass
				del linfo[0]
			for i in linfo:
				try:
					self.info_recup_html(i)
				except:
					pass
				else:
					self.write()

	def _url(self, i):
		if self.method == '0':
			self.url = i.split('<yt:videoId>')[1].split('</yt:videoId>')[0]
		elif self.method == '1':
			if self.type:
				self.url = i.split('href="/watch?v=')[1].split('" rel')[0]
			else:
				self.url = i.split('data-video-id="')[1].split('"')[0]

	def info_recup_html(self, i):
		"""Recover the informations of the html page"""
		if self.type: #Channel
			self.url = i.split('href="/watch?v=')[1].split('" rel')[0]
			self.url_channel = self.id
			self.title = i.split('dir="ltr" title="')[1].split('"')[0]
			self.date = i.split('</li><li>')[1].split('</li>')[0]
			self.data_file = [self.date.split(' ')[1], self.date.split(' ')[0]]
		else: #Playlist
			self.url = i.split('data-video-id="')[1].split('"')[0]
			if '<a href="/user/' in i:
				self.url_channel = i.split('<a href="/user/')[1].split('"')[0]
			elif '<a href="/channel/' in i:
				self.url_channel = i.split('<a href="/channel/')[1].split('"')[0]
			self.title = i.split('data-title="')[1].split('"')[0]
			self.channel = i.split('</a>')[2].split('" >')[1]
			self.data_file = ['Playlist/', self.id]

	def info_recup_rss(self, i):
		"""Recover the informations of a rss page"""
		self.url = i.split('<yt:videoId>')[1].split('</yt:videoId>')[0]
		self.url_channel = i.split('<yt:channelId>')[1].split('</yt:channelId>')[0]
		self.title = i.split('<media:title>')[1].split('</media:title>')[0]
		self.channel = i.split('<name>')[1].split('</name>')[0]
		self.data_file = i.split('<published>')[1].split('+')[0].split('T')
		self.date = self.data_file[0]

	def write(self):
		"""Write the information in a file"""
		if self.mode == 'html':
			return self.generate_data_html()
		elif self.mode == 'raw':
			return self.append_raw()
		elif self.mode == 'list':
			return self.append_list()

	def append_raw(self):
		"""Append the informations wich are been recover 
		in the file 'sub_raw'."""
		if self.method == '0':
			var = self.date + '\t' + self.url + '\t' + self.url_channel + '\t' + self.title + '\t' + self.channel + '\thttps://i.ytimg.com/vi/{}/mqdefault.jpg'.format(self.url) + '\n'
			if len(var) > 300:
				return False
			open('sub_raw', 'a', encoding='utf8').write(var)
		elif self.method == '1':
			var = self.url + '\t' + self.url_channel + '\t' + self.title + '\t' + self.channel + '\thttps://i.ytimg.com/vi/{}/mqdefault.jpg'.format(self.url) + '\n'
			if len(var) > 300:
				return False
			open('sub_raw', 'a', encoding='utf8').write(var)
		var = ""
		return True

	def append_list(self):
		""""Append the informations wich are been recover
		in the file 'sub_raw'. The date is add to sort the
		videos, it is deleted"""
		if len(self.url) != 11:
			return False 
		if self.method == '0':
			open('sub_list', 'a', encoding='utf8').write(self.date + ' https://www.youtube.com/watch?v=' + self.url + '\n')
		elif self.method == '1':
			open('sub_list', 'a', encoding='utf8').write('https://www.youtube.com/watch?v=' + self.url + '\n')
		return True

	def generate_data_html(self):
		"""Append the informations wich are been recover
		in a file in '.../data/[date]/.' """
		try:
			data = open(self.path_cache + 'data/' + self.method + '/' + self.data_file[0], 'rb+').read().decode("utf8")
			if self.url in data:
				return False
		except:
			try:
				os.mkdir(self.path_cache + 'data/' + self.method + '/' + self.data_file[0])
			except:
				pass
		if self.url_channel[:2] == 'UC':
			self.url_channel = 'channel/' + self.url_channel
		else:
			self.url_channel = 'user/' + self.url_channel
		open('{}data/{}/{}/{}'.format(self.path_cache, self.method, self.data_file[0], self.data_file[1].replace(':', '')), 'a', encoding='utf-8').write("""<!--NEXT -->
	<div class="video">
		<a class="left" href="https://www.youtube.com/watch?v={}"> <img src="https://i.ytimg.com/vi/{}/mqdefault.jpg" ></a>
		<a href="https://www.youtube.com/watch?v={}"><h4>{}</h4> </a>
		<a href="https://www.youtube.com/channel/{}"> <p>{}</p> </a>
		<p>{}</p>
		<p class="clear"></p>
	</div>
	""".format(self.url, self.url, self.url, self.title, self.url_channel, self.channel, self.date))
		return True

def html_end(count=7, path='', method='0'):
	"""Recover the file in '.../data/.' with all the
	informations, sort by date and add the informations
	in './sub.html'. """
	fch = sorted(os.listdir(path + 'data/' + method + '/'))
	if len(fch) < count:
		count = len(fch)
	elif count == -1:
		count = len(fch)
	for i in range(count):
		fch_in = sorted(os.listdir(path + 'data/' + method + '/' + fch[-1-i]))
		for a in range(len(fch_in)):
			data = open(path + 'data/' + method + '/' + fch[-1-i] + '/' + fch_in[-1-a], 'r', encoding='utf-8').read()
			open('sub.html', 'a', encoding='utf-8').write(data)
	open('sub.html', 'a').write('</body></html>')

def raw_end(count=7):
	"""Sorted the videos by date"""
	nb = 0
	linfo = sorted(open('sub_raw', 'rb').read().decode('utf8').replace('\r', '').split('\n'))
	if count == -1:
		nb = len(linfo)	
	for i in range(len(linfo)):
		if linfo[i] == '':
			continue
		try:
			if linfo[-1-i][:10] != linfo[-2-i][:10]:
				nb += 1
				if nb == count:
					nb = i
					break
		except IndexError:
			break
		except:
			pass
	os.remove('sub_raw')
	time.sleep(0.01)
	fichier = open('sub_raw', 'a', encoding='utf8')
	for i in range(nb):
		try:
			fichier.write(linfo[-1-i] + '\n')
		except IndexError:
			continue

def list_end(count=7):
	"""Sorted the videos by date"""
	nb = 0
	linfo = sorted(open('sub_list', 'r').read().split('\n'))
	if count == -1:
		nb = len(linfo)
	else:
		for i in range(len(linfo)):
			try:
				if linfo[-1-i][:10] != linfo[-2-i][:10]:
					nb += 1
					if nb == count:
						nb = i
						break
			except IndexError:
				break
			except:
				pass
	os.remove('sub_list')
	fichier = open('sub_list', 'a', encoding='utf8')
	for i in range(nb):
		fichier.write(linfo[-1-i][11:] + '\n')

