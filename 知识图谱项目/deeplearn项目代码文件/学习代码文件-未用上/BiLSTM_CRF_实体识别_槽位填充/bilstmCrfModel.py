from tensorflow import keras
import torch
import torch.nn as nn
from TorchCRF import CRF


class BilstmCrfModel(object):
    def __init__(
            self,
            # 长度模型句子的最大长度
            max_len,
            # 词向量的字典的大小
            vocab_size,
            # 词向量的惟独
            embedding_dim,
            # lstm隐藏单元的数量
            lstm_units,
            # 标签的数量--根据实际情况来设置
            class_nums,
            # 词向量矩阵（若没有，下方也会加入）
            embedding_matrix=None
    ):
        super(BilstmCrfModel, self).__init__()
        self.max_len = max_len
        self.vocab_size = vocab_size
        self.lstm_units = lstm_units
        self.embedding_dim = embedding_dim
        self.class_nums = class_nums
        self.embedding_matrix = embedding_matrix
        if self.embedding_matrix is not None:
            self.vocab_size, self.embedding_dim = self.embedding_matrix.shape

    def build(self):
        # 设置了最大长度max_len
        inputs = keras.layers.input(
            shape=self.max_len,
            dtype='int32'
        )
        # Masking:减小***对模型的影响
        x = keras.layers.Masking(
            mask_value=0
        )(input)

        x = keras.layers.Embedding(
            input_dim=self.vocab_size,
            output_dim=self.embedding_dim,
            # 不训练的意思
            trainable=False,
            weights=self.embedding_matrix,
            mask_zero=True
        )(input)
        x = keras.layers.Bidirectional(
            keras.layers.LSTM(
                self.lstm_units,
                # 返回序列，取每一个输出，而不是最后一个,方便对每一字解码
                return_equences=True
            )(x)
        )
        x = keras.layers.TimeDistributed(
            keras.layers.Dropout(
                0.2
            )
        )(x)
        crf = CRF(self.class_nums)
        outputs = crf(x)

        model = keras.Model(inputs=inputs, outputs= outputs)
        model.compile(
            optimizer='adam',
            loss=crf.loss_function,
            metrics=[crf.accuracy]
        )
        print(model.summary())
        return model


