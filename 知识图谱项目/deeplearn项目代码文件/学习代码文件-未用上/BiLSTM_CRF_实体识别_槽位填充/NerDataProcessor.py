from collections import Counter
import re
from itertools import chain
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np


class NerDataProcessor(object):
    def __init__(self, max_len, vocab_size):
        super(NerDataProcessor, self).__init__()
        # 最大长度
        self.max_len = max_len
        # 字典大小
        self.vocab_size = vocab_size
        # 每一字映射成数字id
        self.word2id = {}

        # 放所有的标签，比如B_disease
        self.tags = []
        # 标签映射数字
        self.tag2id = {}
        # 数字映射标签
        self.id2tag = {}

        #
        self.class_nums = 0
        self.sample_nums = 0


    def read_data(self, path, is_training_data=True):
        """
        数据格式如下（分隔符为空格）：
        便 B_disease
        秘 I_disease
        两 O
        个 O
        多 O
        月 O
        """
        X = []
        y = []
        sentence = []
        labels = []
        # 对句子进行切分，保证句子长度不超过max_len
        split_pattern = re.compile(r'[：:；;。.、？?! ，,/]')
        with open(path, 'r', encoding='utf8') as f:
            for line in f.readlines():
                line = line.strip().split()
                if not line or len(line) < 2:
                    X.append(sentence.copy())
                    y.append((labels.copy()))
                    sentence.clear()
                    labels.clear()
                    continue
                word, tag = line[0], line[1]
                tag = tag if tag != 'o' else 'O'
                if split_pattern.match(word) and len(sentence) >= self.max_len:
                    sentence.append(word)
                    labels.append(tag)
                    X.append(sentence.copy())
                    y.append(labels.copy())
                    sentence.clear()
                    labels.clear()
                else:
                    sentence.append(word)
                    labels.append(tag)
            if len(sentence):
                X.append(sentence.copy())
                sentence.clear()
                y.append((labels.copy()))
                labels.clear()

        if is_training_data:
            self.tags = sorted(list(set(chain(*y))))
            self.tag2id = {tag: idx + 1 for idx, tag in enumerate(self.tags)}
            self.id2tag = {idx + 1: tag for idx, tag in enumerate(self.tags)}

            self.tag2id['padding'] = 0
            self.id2tag[0] = 'padding'
            self.class_nums = len(self.id2tag)
            self.sample_nums = len(X)

            vocab = list(chain(*X))
            print('vocab length:', len(set(vocab)))
            print(self.id2tag)
            vocab = Counter(vocab).most_common(self.vocab_size - 2)
            vocab = [v[0] for v in vocab]
            for index, word in enumerate(vocab):
                self.word2id[word] = index + 2

            self.word2id['padding'] = 0
            self.word2id['OOV'] = 1

            return X, y


    def encode(self, X, y):
        """
        将训练样本映射成数字，以及惊醒padding
        将标签进行 one-hot
        """
        X = [[self.word2id.get(word, 1) for word in x] for x in X]
        X = pad_sequences(X)
        X = [[self.tag2id.get(tag, 0) for tag in t] for t in y]
        y = pad_sequences(y, maxlen=self.max_len, value=0)

        def label_tp_one_hot(index: []):
            data = []
            for line in index:
                data_line = []
                for i, index in enumerate(line):
                    line_line = [0]*self.class_nums
                    line_line[index] = 1
                    data_line.append(line_line)
                data.append(data_line)
            return np.array(data)

        y = label_tp_one_hot(index=y)
        print('y,shape', y.shape)

        return X, y


