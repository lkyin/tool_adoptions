# Python program to generate topics 
  
# importing all necessery modules 
from wordcloud import WordCloud, STOPWORDS 
import matplotlib.pyplot as plt 
import os
from tqdm import tqdm

# set your tool name
toolname = 'mocha'

path = './data/{}/'.format(toolname)

files = os.listdir(path)

stopwords = set(STOPWORDS)

stopwords.add(toolname)

stopwords.add('test')

stopwords.add('tests')

for file in files:

    comment_words = ' '

    with open(path+file, 'rb') as f:

        csv_lines = eval(f.readlines()[0])

    # iterate through the csv file 
    for val in csv_lines:

        # split the value 
        tokens = val.split() 
          
        # Converts each token into lowercase 
        for i in range(len(tokens)):

            tokens[i] = tokens[i].lower() 

        tokens = [token for token in tokens if token[0] != 'x']

        tokens = [token for token in tokens if len(token) > 1]

        for word in tokens:

            comment_words = comment_words + word + ' '
      
      
    wordcloud = WordCloud(width = 800, height = 800, 
                    background_color ='white', 
                    stopwords = stopwords, 
                    min_font_size = 10).generate(comment_words)

    top_10_words = sorted(wordcloud.words_.items(), key = lambda item: item[1], reverse=True)[10:20]

    fname = file.replace('.txt', '.jpg')

    print([fname, top_10_words])

      
    # plot the WordCloud image                        
    plt.figure(figsize = (8, 8), facecolor = None) 
    plt.imshow(wordcloud) 
    plt.axis("off") 
    plt.tight_layout(pad = 0) 
    plt.show()

    

    plt.savefig('{}_{}'.format(toolname, fname), format="jpg")


print('all done~!')