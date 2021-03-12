import requests
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
import multiprocessing

class TextComparer():

    def __init__(self, url_list = []):
        self.url_list = url_list
        self.filenames = []

    def download(self, url, filename):
        response = requests.get(url)
        
        if response.ok:
            with open(filename, 'wb') as fd:
                self.filenames.append(filename)
                for chunk in response.iter_content(chunk_size=1024):
                    fd.write(chunk)
        elif response.status_code == 404:
            raise NotFoundException(f'Statuse code: {response.status_code} , Please try again')

    def multi_download(self, workers = 5):
        with ThreadPoolExecutor(workers) as ex:
            for i in range(0, len(self.url_list)):
                print("Files are downloading..." + str(i+1))
                self.download(self.url_list[i], 'book' + str(i+1) + ".txt")

    def __iter__(self):
        self.number = 0
        return self

    def __next__(self):
        current_number = self.number

        if current_number < len(self.filenames):
            self.number += 1
            return self.filenames[current_number]
        else:
            raise StopIteration

    def urllist_generator(self):
        for url in self.url_list:
            yield url

    def avg_vowels(self, text):
        vowel_List = ["a", "e", "i", "o", "u", "y"]

        with open(text) as read_file:
            txt = read_file.read()

        words = txt.split()
        word_count = len(words)
        vowels = 0

        for word in words:
            for letter in word:
                if letter.lower() in vowel_List:
                    vowels += 1
        
        vowel_median = round(vowels / word_count, 2)
        return vowel_median, text


    def hardest_read(self):
        workers = multiprocessing.cpu_count()

        with ProcessPoolExecutor(workers) as ex:
            results = ex.map(self.avg_vowels, self.filenames)
        
        hardest_book = None

        for result in results:
            if hardest_book is None or hardest_book[0] < result[0]:
                hardest_book = result
        
        return self.avg_vowels(hardest_book[1])
            
class NotFoundException(Exception):
    pass