import json
from collections import Counter
from hazm import word_tokenize, Normalizer
from wordcloud import WordCloud
from pathlib import Path
from typing import Union

from data import data_path

# data_path = Path(__file__).resolve().parent.parent / 'data'

class ChatAnalysis:
    """Processes chat data and creates word cloud
    """    
    def __init__(self, chat_data: Union[str, Path] , stopwords_path: Union[str, Path]=None , alternative_words: dict={} ):
        """
        :param chat_data: Path to json file of telegram output
        :param stopwords_path: Path to stopwords text file. if it is None, it'll use defult stopwords file  , defaults to None
        :param alternative_words: Dictionary that contains alternative words in order to count all of them in single reprsentation
        example:
        dict = {
            'bro' : 'brother'
        }
        , defaults to {}
        """                       
        self.chat_data = chat_data
        if stopwords_path is None:
            stopwords_path = data_path / 'stopwords.txt'
        self.alternative_words = alternative_words
        
        # read chat data
        with open(chat_data, 'r') as f:
            self.data = json.load(f)

        # read stop words and process on them
        with open(stopwords_path, 'r') as f:
            self.stopwords = f.read()
        self.normalizer = Normalizer()
        self.stopwords = self.normalizer.normalize(self.stopwords)
        self.stopwords = word_tokenize(self.stopwords)
        self.stopwords = set(self.stopwords)
        
        #process on chat data
        self.data_str = ''
        for message in self.data['messages']:
            if type(message['text']) is str:
                single_message = self.normalizer.normalize(message['text'])
                single_message = single_message.replace('\u200c', ' ')
                tokens = word_tokenize(single_message)
                tokens = filter(lambda w: w not in self.stopwords, tokens)
                tokens = map(self._alternative_word, tokens)
                self.data_str += f" {' '.join(tokens)}"

    #replace with proper alternative
    def _alternative_word(self, word):
        if word in self.alternative_words:
            return self.alternative_words[word]
        else:
            return word

    #Generate and show word cloud
    def generate_wordcloud(self, width: int=1200, height: int=800, font_path: Union[str, Path]=data_path / 'Vazir.ttf', background_color: str='white'):
        """Generates a word cloud

        :param width: word cloud width, defaults to 1200
        :param height: word cloud height, defaults to 800
        :param font_path: Path to font file that will use to create word cloud, defaults to data_path/'Vazir.ttf'
        :param background_color: word cloud background color, defaults to 'white'
        :return: word cloud image
        """                
        font_path = str(font_path)
        self.wordcloud = WordCloud(width=width, height=height, font_path=font_path, background_color=background_color).generate(self.data_str)
        return self.wordcloud.to_image()

    # Save word cloud
    def save_wordcloud(self, save_path: Union[str, Path]=None, extension: str='png'):
        """Saves word cloud image to save path

        :param save_path: Path to save word cloud image, defaults to None
        :param extension: Desired extension of word cloud image, defaults to 'png'
        """               
        if save_path == None:
            save_path = data_path / f'word_cloud.{extension}'
        save_path = str(save_path)
        self.wordcloud.to_file(save_path)
        return f'wordcloud image saved in: {save_path}'






if __name__ == '__main__':
    
    chat = ChatAnalysis(chat_data=data_path / 'result.json')
    chat.generate_wordcloud()
    print(chat.save_wordcloud())
    print('Done')