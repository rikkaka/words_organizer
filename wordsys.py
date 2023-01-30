import datetime, pickle, os

recite_intervel = {0: 0, 1: 1, 2: 2, 3: 4, 4: 8, 5: 16, 6: 32}
cwd = os.getcwd()
libFileName = 'WordsLibrary'
Path = cwd + '/' + libFileName

class Word:
    def __init__(self, word, translation):
        self.wordtext = word
        self.translation = translation
        self.condition = 0
        self.date = datetime.date.today()  # 可以改成凌晨四点前都是今天

    def recitable(self):
        intervel = self.date.__sub__(datetime.date.today()).days
        if self.condition not in recite_intervel.keys():
            return False
        if intervel >= recite_intervel[self.condition]:
            return True
        else:
            return False

    def improve(self):
        self.condition += 1

    def back(self):
        self.date = datetime.date.today()
        self.condition = 0

    def master(self):
        self.condition = -1


class WordsLibrary:
    def __init__(self):
        self.words = []
        self.recite_nums = -1

    def len(self):
        return len(self.words)

    def get_recite_list(self):
        recite_list = []
        for word in self.words:
            if word.recitable():
                recite_list.append(word)
        self.recite_nums = len(recite_list)
        return recite_list

    def get_recite_nums(self):
        self.get_recite_list()
        return self.recite_nums

    def get_word(self):
        return self.get_recite_list()[0]

    def get_total_nums(self):
        return len(self.words)

    def add_word(self, word):
        self.words.append(word)

    def get_words(self):
        return self.words

    def load_words(self, path=Path):
        try:
            with open(path, 'rb') as file:
                self.words = pickle.load(file)
        except:
            pass

    def save_words(self, path=Path):
        with open(path, 'wb') as file:
            pickle.dump(self.words, file, 2)


if __name__ == "__main__":
    word = Word('apple', '苹果')
    library = WordsLibrary()
    library.add_word(word)
    print(word.recitable())
    print(library.get_recite_list())
    word.improve()
    print(word.recitable())
    print(library.get_recite_list())
