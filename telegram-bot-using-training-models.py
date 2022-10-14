import telebot
from telebot import types
import pickle
import sklearn
import numpy as np
import ktrain
import joblib

def clean_text(text):
    alphabet = ["а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м", "н", "о",
                "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я"]
    text = text.lower()
    new_line = ""
    for symbol in text:
        if (symbol == ' ' or symbol == " ") and len(new_line) > 0 and new_line[-1] != ' ':
            new_line += ' '
            continue
        if symbol not in alphabet:
            continue
        new_line += symbol

    return new_line


def bies(clean_message):
    with open('trained_bayes_model.pkl', 'rb') as fin:
        vectorizer, clf = pickle.load(fin)

        X_new = vectorizer.transform([clean_message]).reshape(1, -1)
        X_new_preds = clf.predict_proba(X_new)
        return (X_new_preds)


def perceptrone(clean_message):
    with open('MLP.pkl', 'rb') as fin:
        vectorizer, clf = pickle.load(fin)

        X_new = vectorizer.transform([clean_message]).reshape(1, -1)
        X_new_preds = clf.predict_proba(X_new)
        return (X_new_preds)

def log_reg(clean_message):
    with open('LogisticRegression.pickle', 'rb') as fin:
        vectorizer, clf = pickle.load(fin)

        X_new = [clean_message]
        X_new_preds = clf.predict_proba(X_new)
        return(X_new_preds)

#def LSTM(clean_text):
    #with open('LSTM_trained_model.pkl', 'rb') as fin:
        #clf = pickle.load(fin)

        #X_new =[clean_text]
        #tok = Tokenizer(num_words=1000)
        #test_sequences = tok.texts_to_sequences(X_new)
        #test_sequences_matrix = sequence.pad_sequences(test_sequences, maxlen = 150)

        #res = np.array([0])
        #a = clf.evaluate(test_sequences_matrix, res)
        #print(a)

def BERT(mes):
    p = ktrain.load_predictor('C:/Users/kalch/PycharmProjects/bot/distilbert')
    return p.predict([mes], return_proba = True)

def chastotniy(mes):
    clf = joblib.load('chastotn_model.pkl')
    X_new = [mes]
    X_new_preds = clf.predict_proba(X_new)
    return(X_new_preds)

##keyboard1 = telebot.types.ReplyKeyboardMarkup()
##keyboard1.row("Байес", 'LSTM')

bot = telebot.TeleBot("******************")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет, я работаю и готов выдавать предсказания!")


@bot.message_handler(func=lambda message: True)

def echo_all(message):
    clean_message = clean_text(str(message))

    res_bies = bies(clean_message)

    res_mlp = perceptrone(clean_message)

    res_reg_log = log_reg(clean_message)
#[[0, 1]]
    chastotn = chastotniy(clean_message)

    bert = BERT(clean_message)

    #LSTM(clean_message)

    bot.reply_to(message, "Вероятность того, что текст был сгенерирован:\n" + "bies:....." + str(res_bies[0][0]) +
                 '\n' + "MLP:....." + str(res_mlp[0][1]) + '\n' +
                 "LogRegression:..." + str(res_reg_log[0][1]) + '\n'
                 + "Частотный анализ:....." + str(chastotn[0][1]) + '\n'
                 + "BERT:....." + str(bert[0][1] - 0.1) + '\n')


bot.infinity_polling()
