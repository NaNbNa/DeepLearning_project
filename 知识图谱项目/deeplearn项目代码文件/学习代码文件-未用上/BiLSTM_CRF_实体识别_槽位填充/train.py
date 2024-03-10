from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score, classification_report
from tensorflow import keras
import numpy as np
from bilstmCrfModel import BilstmCrfModel
from TorchCRF import CRF
from nltk import word_tokenize
from NerDataProcessor import NerDataProcessor
import pickle


max_len = 80
vocab_size = 2410
embedding_dim = 200
lstm_units = 128

if __name__ == '__main__':
    # 实例化
    ndp = NerDataProcessor(max_len, vocab_size)
    train_x, train_y = ndp.read_data(
        "",
        is_training_data=False
    )
    train_x, train_y = ndp.encode(train_x, train_y)
    dev_x, dev_y = ndp.read_data(
        "",
        is_training_data=False
    )
    dev_x, dev_y = ndp.encode(dev_x, dev_y)
    test_x, test_y = ndp.read_data(
        "",
        is_training_data=False
    )
    test_x, test_y = ndp.encode(test_x, test_y)

    class_nums = ndp.encode(test_x, test_y)
    word2id = ndp.word2id
    tag2id = ndp.tag2id
    id2tag = ndp.id2tag
    # 保存字典
    pickle.dump(
        (word2id, tag2id),
        open("", "wb")
    )
    bilstm_crf = BilstmCrfModel(
        max_len,
        vocab_size,
        embedding_dim,
        lstm_units,
        class_nums
    )
    model = bilstm_crf.build()
    # 学习率
    reduce_lr = keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=4,
        verbose=1
    )

    earlystop = keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=10,
        verbose=2,
        mode='min'
    )
    bast_model_filepath = ''
    checkpoint = keras.callbacks.ModelCheckpoint(
        bast_model_filepath,
        monitor='val_loss',
        verbose=1,
        save_best_only=True,
        mode='min'
    )

    model.fit(
        train_x,
        train_y,
        batch_size=12,
        epochs=100,
        validation_data=(dev_x, dev_y),
        shuffle=True,
        callbacks=[reduce_lr, earlystop, checkpoint]
    )
    model.load_weights(bast_model_filepath)
    model.save('model_crf.h5')

    pred = model.predict(test_x)

    true_y, pred_y = [], []

    for t_oh, p_oh in zip(test_y, pred):
        t_oh = np.argmax(t_oh, axis=1)
        t_oh = [id2tag[i].replace('_', '-') for i in t_oh if i != 0]
        p_oh = np.argmax(p_oh, axis=1)
        t_oh = [id2tag[i].replace('_', '-') for i in p_oh if i != 0]

        true_y.append(t_oh)
        pred_y.append(p_oh)

    f1 = f1_score(true_y, pred_y)
    p = precision_score(true_y, pred_y)
    r = recall_score(true_y, pred_y)
    acc = accuracy_score(true_y, pred_y)
    print('f1_score:', f1)
    print('precision_score:', p)
    print('recall_score:', r)
    print('accuracy_score:', acc)
    print(classification_report(true_y, pred_y, digits=4))






