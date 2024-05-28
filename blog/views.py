import threading
from django.shortcuts import render
from django.http import HttpResponse
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

import collections.abc
collections.Hashable = collections.abc.Hashable

# Create your views here.

# bot = ChatBot('chatbot', read_only=False, 
#               logic_adapters=[{
#                   'import_path':'chatterbot.logic.BestMatch'
#                 #   'default_response': 'I am sorry, but I do not understand.',         # Added a default response
#                 #   'maximum_similarity_threshold': 0.90                                # Added a maximum similarity threshold
#                   }])                                                                   # Added a logic adapter to the bot

list_to_train = [
    "hi",
    "hi, there!",
    "what is your name?",
    "My name is Chatbot",
    "how are you?",
    "I am good, thank you",
    "that's good to hear",
    "thank you",
    "you're welcome",
    "bye",

]                                       # List of responses to train the bot with


# chatterbotCorpusTrainer = ChatterBotCorpusTrainer(bot)

# # trainer = ListTrainer(bot)                      # Created a trainer for the ListTrainer bot
# # trainer.train(list_to_train)                    # Training the bot with the list_to_train list

# chatterbotCorpusTrainer.train('chatterbot.corpus.english')

local = threading.local()

def get_bot():
    # Check if we already have a bot in this thread
    if not hasattr(local, 'bot'):
        # Create a new bot for this thread
        local.bot = ChatBot('chatbot', read_only=False, logic_adapters=['chatterbot.logic.BestMatch'])
        chatterbotCorpusTrainer = ChatterBotCorpusTrainer(local.bot)
        chatterbotCorpusTrainer.train('chatterbot.corpus.english')
    # Return the bot for this thread
    return local.bot


def index(request):
    return render(request, 'blog/index.html')


def getResponse(request):
    bot = get_bot()
    userMessage = request.GET.get('usermessage')
    chatResponse = str(bot.get_response(userMessage))
    return HttpResponse(chatResponse)

