from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import pickle

chatbot=ChatBot("instagram_bot")
f = open('./InstagramComments_.p', 'rb')
comment=pickle.load(f)
f.close()



chatbot.set_trainer(ListTrainer)



for i in range(2000):
    chatbot.train(comment[i])
    print(i)

print("finish")
response = chatbot.get_response("how are you")
print(response)