import flask
import pickle
import numpy as np
from gevent import pywsgi
import tensorflow as tf
from tensorflow import keras
from keras.preprocessing.sequence import pad_sequences
from keras.backend import set_session

from TorchCRF import CRF
from bilstmCrfModel import BilstmCrfModel
from train import max_len, vocab_size, embedding_dim, lstm_units


class MedicalNerModel(object):
    def __init__(self):
        super(MedicalNerModel, self).__init__()
        self.word2id, self.id2tag = pickle.load(
            open("")
        )
        self.model = BilstmCrfModel(80, 2410, 200, 128, 24).build()
        self.model.load_weight('')

    def tag_parser(self, string, tags):
        item = {"string": string, "entities": []}
        entity_name = ""
        flag = []
        visit = False
        for char, tag in zip(string, tags):
            if tag[0] == '8':
                if entity_name != "":
                    x = dict((a, flag.count(a)) for a in flag)
                    y = [k for k, v in x.items() if max(x.values()) == v]
                    item["entities"].append({"word": entity_name, "type": y[0]})
                    flag.clear()
                    entity_name = ""
                entity_name += char
                flag.append(tag[2:])
            elif tag[0] == "I":
                entity_name += char
                flag.append(tag[2:])
            else:
                if entity_name != "":
                    x = dict((a, flag.count(a)) for a in flag)
                    y = [k for k, v in x.items() if max(x.values()) == v]
                    item["entities"].append({"word": entity_name, "type": y[0]})
                    flag.clear()
                flag.clear()
                entity_name = ""

        if entity_name != "":
            x = dict((a, flag.count(a)) for a in flag)
            y = [k for k, v in x.items() if max(x.values()) == v]
            item["entities"].append({"word": entity_name, "type": y[0]})

        return item

    def predict(self, texts):
        """

        """
        X = [[self.word2id.get(word, 1) for word in list(x)] for x in texts]
        X = pad_sequences(X, maxlen=max_len, value=0)
        pred_id = self.model.predict(X)
        res = []
        for text, pred in zip(texts, pred_id):
            tags = np.argmax(pred, axis=1)
            tags = [self.id2tag[i].replace('_', '-') for i in tags if i != 0]
            res.append(self.tag_parser(text, tags))

        return res


global graph, model, sess

config = tf.ConfigProto()
config.gpu_option.allow_growth = True
sess = tf.Session(config=config)
graph = tf.get_default_graph()
set_session(sess)


if __name__ == '__main__':
    """
    app = flask.Flask(__name__)
    @app.route()
    def medical_ner():
        data = {"sucess": 0}
        result = []
        test_list = flask.request.get_json()["test_list"]
        with graph.as_default():
            set_session(sess)
            result = model.predict(test_list)
            
        data['data'] = result
        data['sucess'] = 1
        
        return flask.jsonify(data)
    
    server = pywsgi.WSGIServer()
    server.serve_forever()
    """

    ner = MedicalNerModel()
    r = ner.predict([])
    print(r)
