import requests
from lxml import html
from urlparse import urljoin
from collections import deque

from threading import Thread


MAX_THREADS = 4
num_threads = 0
que = deque(['https://en.wikipedia.org/wiki/Duck'])
crawled = set()

graph = set()

def spawn_new_worker():
	t = Thread(target=crawl, args=())
	t.start()


def valid_page(link):
	if 'https://en.wikipedia.org/wiki/' not in link:
		return False
	if 'https://en.wikipedia.org/wiki/Wikipedia:' in link:
		return False

	return True;




def crawl():
	global que
	global crawled

	while True:
		if len(que) == 0:
			return

		url = que.popleft()

		if url in crawled or url.split('#')[0] in crawled:
			continue
		crawled.add(url)

		r = requests.get(url)
		page_content = r.text

		links = html.fromstring(page_content).xpath('//a/@href')
		print(url + "   " + str(len(crawled)))

		for link in links:
			link = urljoin(url,link)
			if valid_page(link):
				que.append(link)

		if num_threads <= MAX_THREADS and len(que) > 1:
			spawn_new_worker()

	print("DONE")


def main():
	global num_threads

	t_1 = Thread(target=crawl, args=())
	num_threads += 1
	t_1.start()

	t_1.join()

if __name__ == '__main__':
	main()


