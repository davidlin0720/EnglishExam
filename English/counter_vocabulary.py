import csv
import re
from googletrans import Translator

# 实例化翻译器，由于模块默认的服务url在国内无法使用，所以我们修改成国内可用的google翻译服务地址
translator = Translator(service_urls=["translate.google.cn"])

csv_file = 'all_exam_vocabulary.csv'
fileList = ['exams/101.txt', 'exams/102.txt', 'exams/103.txt', 'exams/104.txt', 'exams/105.txt', 
           'exams/106.txt', 'exams/107.txt', 'exams/108.txt', 'exams/109.txt', 'exams/109_1.txt', 'exams/110.txt']
# fileList = ['exams/110.txt']
# csv_file = '110_exam_vocabulary.csv'

ignore_words = ['(A)', '(B)', '(C)', '(D)', '1.', '2.', '3.', '4.', '______', '_____', '_______', '________', '__________', '-', ':', '－－', 
                '(a)','(b)', '(c)', '(b)', '(d)','(e)','(f)','(g)','(h)','(i)', '(j)','(“iq)', '(-)',
                '1.','2.','3.','4.','5.','6.','7.', '8.','9.',
                '10.','11.','12.','13','14.','15.','16.','17.','18.','19.',
                '20.','21.','22.','23','24.','25.','26.','27.','28.','29.',
                '30.','31.','32.','33','34.','35.','36.','37.','38.','39.',
                '40.','41.','42.','43','44.','45.','46.','47.','48.','49.',
                '50.','51.','52.','53','54.','55.','56.','57.','58.','59.',
                 'i', 'he', 'she', 'you', 'your', 'me', 'their', 'that', 'the', 'it', 'this', 'do', 'ect'
                 'has', 'have', 'good', 'bad', 'as', 'on', 'with', 'be', 'us', 'out', 'works', 'us', 'up',
                 'was', 'did', 'is', 'to', 'for', 'is', 'you’ve', 'it’s', 'don’t', 'can’t', 'didn’t',
                 'they’ll', 'you’re', 'i’m',
                 'am', 'any', 'what', 'why', 'come', 'are', 'other', 'mr', 'so', 'being', 'here',
                 'Mr', 'and', 'or', 'when', 'in', 'not', 'size', 'if', 'will',
                 'yet', 'top', 'couldn’t', 'say', 'name', 'use', 'year-', 'then', '-digit', '(th', 'century)',
                 'too', 'dog', 'its', 'go', 'vi', 'of', 'at', 'see', 'them', 'by', 'but',
                 'john', 'no', 'uk', 'us', 'nor', 'itself', 'big', 'may', 'our', 'way', 'about', 'true', 'ie', 'name', 'we', 'get',
                 'over','push', 'hand', 'over', 'day', 'off', 'face', 'room', 'job', 'doesn’t', # 已知單字
                 'tom', 'really', 'boy', 'likes', 'play', 'jokes', 'his', 'younger', 'sister', 'parents', 'store',
                 'take', 'than', 'which', 'move', 'fast', 'keep', 'such', 'eat', 'drink', 'new', 'plant', 'know', 
                 'hearing', 'her', 'since', 'many', 'house', 'plants', 'from', 'they', 'need', 'air', 'green', 'healthy', 'those', 'turn', 'area',
                 'end', 'floor', 'land', 'safty', 'after', 'jumping', 'failed', 'open', 'used', 'power', 'heavy', 'change', 'classroom', 'teacher',
                 'market', 'local', 'place', 'went', 'trash', 'number', 'still', 'food', 'class', 'into', 'asked', 'together', 'lisa', 'onto', 'playing',
                 'basketball', 'hundreds', 'free', 'city', 'government', 'hope', 'key', 'future', 'idea', 'following', 'personal', 
                 'three', 'women', 'made', 'company', 'making', 'great', 'under', 'often', 'turns', 'does', 'travel', 'person',
                 'foreign', 'earliest', 'absolutely', 'money', 'an', 'car', 'cannot', 'driver', 'very', 'one', 'king', 'agreed', 'gave', 'river',
                 'safe', 'through', 'lands', 'later', 'form', 'bara’s', 'bas', 'million', 'years', 'week', 'typhoon', 'were', 'finally', 'opened',
                 'bus', 'most', 'area', 'street', 'who', 'enter', 'helping', 'cities', 'visit', 'just', 'would', 'same', 'them', 'historic',
                 'buildings', 'public', 'however', 'birds', 'now', 'came', 'international', 'war', 'today', 'cause', 'given', 'thousand', 'invite',
                 'fathers', 'acocomplished', 'scientist', 'idea', 'strong', 'animal', 'another', 'giving', 'birth', 'control', 'put', 'eggs',
                 'bird', 'achievements', 'music', 'both', 'glass', 'living', 'heard', 'musical', 'glasses', 'create', 'color', 'paint', 'notes', 
                 'there', 'first', 'year', 'between', 'four', 'without', 'break', 'down', 'set', 'similarly', 'having', 'ran', 'largest', 'smallest', 
                 'wheel', 'foot', 'turned', 'friends', 'popular', 'thousands', 'build', 'sold', 'fashions', 'life', 'seven', 'different', 'park',
                 'more', 'human', 'each', 'two', 'death', 'took', 'changed', 'moving', 'large', 'colored', 'lose', 'stom', 'cloud', 'him', 'until',
                 'thing', 'happened', 'again', 'all', 'could', 'got', 'anyway', 'june', 'final', 'fishing', 'believe', 'god', 'enough', 'can', 'hard', 
                 'famous', 'musicians', 'probllems', 'fashionable', 'wonderland', 'located', 'children', 'real', 'th', '-year', 'hou-i', 'year—', 'asset—her', 
                 'myself', 'ad', 'three-year-old', 'is—trips', 'mei-ling', 'warm-up', 'foolishness—a', 'health-policy', 'large-scale',
                 'graduate-level', 'one-size-fits-all', 'six', 'ii', 'sex', 'users', 'fire', 'bc', 'wi', 'aa', 'ali', 'bli', 'cli', 'cnn', 'etc' ]
fomart = 'abcdefghijklmnopqrstuvwxyz'
vocabulary = {}
rows = []
cvs_colums = ['ENGLISH', 'CHINESE', 'COUNT']
g_cvsVocabulary = []

def countVocabulary(row):
    row = row.lower();
    row = row.replace('\r\n', '')
    row = row.replace('-', ' ')
    row = row.replace('—', ' ')
    row = row.replace(':', ' ')
    row = row.replace('(', '')
    row = row.replace(')', '')
    row = row.replace('”', '')
    row = row.replace('“', '')
    row = row.replace(';', '')
    row = row.replace(',', '')
    row = row.replace('’s', '')
    row = row.replace('!', '')
    row = row.replace('?', '')
    row = row.replace('""', '')
    row = row.replace('.', '')
    row = row.replace('0', '')
    row = row.replace('1', '')
    row = row.replace('2', '')
    row = row.replace('3', '')
    row = row.replace('4', '')
    row = row.replace('5', '')
    row = row.replace('6', '')
    row = row.replace('7', '')
    row = row.replace('8', '')
    row = row.replace('9', '') 
    regex = re.compile('\s+')

    words = regex.split(row)
    for word in words:
        if not(word in ignore_words):
            if vocabulary.get(word, -1) == -1:
                if len(word) > 2:
                    vocabulary.setdefault(word, 1)
            else:
                vocabulary[word] = vocabulary[word]+1

for file in fileList:
    print("分析 - ", file)
    with open(file, 'r', encoding='utf-8-sig', newline='') as examfile:
        for line in examfile:
            # rows.append(line)
            countVocabulary(line)
   
for row in vocabulary:
    # result = translator.translate(row, src='en', dest='zh-TW')
    # print(row, '= ', result.text)
    dict1 = {'ENGLISH':row, 'CHINESE':'', 'COUNT': vocabulary[row]}   
    # 假設不同, 就全部取代
    g_cvsVocabulary.append(dict1)
    # print(row, '= ', result.text, '(', result.extra_data, ')')
    # print(row, '= ', result.text)
        
#print(vocabulary)
print('單字數', len(vocabulary))
with open(csv_file, 'w', encoding='utf-8-sig', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=cvs_colums)
    writer.writeheader()
    writer.writerows(g_cvsVocabulary)
