import CYKParse
import Tree
import Covid
import datetime


requestInfo = {
        'time1': '',
        'time2': '',
        'location': '',
        'comp': '',
        'special': ''
}
haveGreeted = False

#py "C:\Users\Lanxiang Yang\source\repos\CS171 Project Part 3\CS171 Project Part 3\chatbot.py"
date_map,Anaheim,Costa_Mesa,Huntington_Beach,Irvine,Laguna_Hills,Lake_Forest,Newport_Beach,Orange,Santa_Ana,Tustin,Total = Covid.getData('Anaheim','Costa_Mesa', 'Huntington_Beach', 'Irvine', 'Laguna_Hills', 'Lake_Forest','Newport_Beach','Orange', 'Santa_Ana', 'Tustin','Total')
database = {'anaheim':Anaheim,'costa_mesa':Costa_Mesa, 'huntington_beach':Huntington_Beach, 'irvine':Irvine, 'laguna_hills':Laguna_Hills, 'lake_forest':Lake_Forest,'newport_beach':Newport_Beach,'orange':Orange, 'santa_ana':Santa_Ana, 'tustin':Tustin, 'orange_county':Total}

# Given the collection of parse trees returned by CYKParse, this function
# returns the one corresponding to the complete sentence.
def getSentenceParse(T):
    sentenceTrees = { k: v for k,v in T.items() if k.startswith('S/0') }
    if list(sentenceTrees.keys()) == []:
        return -1
    else:
        completeSentenceTree = list(sentenceTrees.keys())[-1]
        return T[completeSentenceTree]

# Processes the leaves of the parse tree to pull out the user's request.
def updateRequestInfo(Tr):
    global requestInfo
    lookingForLocation = False
    two = 0
    for leaf in Tr.getLeaves():
        if (leaf[0] == 'Adverb' and leaf[1] in ['now','today','yesterday']) or (leaf[0] == 'Date') or (leaf[0] == 'Noun' and leaf[1] == 'month'):
            two += 1
    if two < 2:
        for leaf in Tr.getLeaves():
            if (leaf[0] == 'Adverb' and leaf[1] in ['now','today','yesterday']) or (leaf[0] == 'Date') or (leaf[0] == 'Noun' and leaf[1] == 'month'):
                requestInfo['time1'] = leaf[1]
            if lookingForLocation and leaf[0] == 'Name':
                requestInfo['location'] = leaf[1]
            if leaf[0] == 'Preposition' and leaf[1] == 'in':
                lookingForLocation = True
            else:
                lookingForLocation = False
            if leaf[0] == 'Noun' and leaf[1] == 'name':
                lookingForName = True
    else:
        for leaf in Tr.getLeaves():
            if leaf[0] == 'Adverb' or 'Date':
                if leaf[1] in ['now','today','yesterday'] or '-' in leaf[1]:
                    if requestInfo['time1'] == '':
                        requestInfo['time1'] = leaf[1]
                    if requestInfo['time1'] != '':
                        requestInfo['time2'] = leaf[1]
            if lookingForLocation and leaf[0] == 'Name':
                requestInfo['location'] = leaf[1]
            if leaf[0] == 'Preposition' and leaf[1] == 'in':
                lookingForLocation = True
            else:
                lookingForLocation = False
            if leaf[0] == 'Comp':
                requestInfo['comp'] = leaf[1]


# This function contains the data known by our simple chatbot
def getNumber(location, time):
    if location != '':
        if time in ['now', 'today']:
            x = datetime.datetime.now()
            #x = datetime.datetime.today() - datetime.timedelta(days=1)
            s = str(x.day) + '-' + x.strftime("%b") + '-' + x.strftime("%y")
            if s in date_map:
                return str(database[location][date_map[s]])
            else:
                return -1
        elif time in ['yesterday']:
            x = datetime.datetime.today() - datetime.timedelta(days=1)
            s = str(x.day) + '-' + x.strftime("%b") + '-' + x.strftime("%y")
            if s in date_map:
                return str(Irvine[date_map[s]])
            else:
                return -1
        elif time in date_map.keys():
            return str(database[location][date_map[time]])
        elif time == 'month':
            x = datetime.datetime.today() - datetime.timedelta(days=1)
            t = x.strftime("%b") + '-' + x.strftime("%y")
            l = []
            for i,j in date_map.items():
                if t in i:
                    l.append(j)
            if len(l) <= 1:
                return -1
            else:
                return Irvine[l[-1]] - Irvine[l[0]]
        else:
            return 'unknown'
    else:
        return 'unknown'

# Format a reply to the user, based on what the user wrote.
def reply():
    global requestInfo
    global cumaltive
    # Special conditions
    if requestInfo['special'] == 1:
        print("Sorry one or more of the dates you entered is not recorded yet")
        return

    # Time and location
    time = 'now' # the default
    if requestInfo['time2'] == '':
        if requestInfo['time1'] != '':
            time = requestInfo['time1']

        if getNumber(requestInfo['location'], time) == -1 and time in ['now','today','month','yesterday']:
            print("Sorry the date you entered is not recorded yet.")
            print("The latest recorded date is:",list(date_map.keys())[-1])
            recent = input("\nDo you want to see the most recent recorded data? (Y for Yes, N for No): ")
            if recent == "Y":
                print('\nThe number of cases in ' + requestInfo['location'] + ' on ' + list(date_map.keys())[-1] + ' is ' + str(getNumber(requestInfo['location'], list(date_map.keys())[-1])) + '.')
            else:
                pass
        else:
            if time.count('-') == 2:
                print('The number of cases in ' + requestInfo['location'] + ' ' +
                    'on ' + time + ' is ' + str(getNumber(requestInfo['location'], time)) + '.')
            elif time == 'month':
                print('The number of cases are reported in ' + requestInfo['location'] + ' ' +
                    'this ' + time + ' is ' + str(getNumber(requestInfo['location'], time)) + '.')
            else:
                print('The number of cases in ' + requestInfo['location'] + ' ' +
                    time + ' is ' + str(getNumber(requestInfo['location'], time)) + '.')
    else:
        time1 = requestInfo['time1']
        time2 = requestInfo['time2']
        if getNumber(requestInfo['location'], time1) == -1 or time1 in ['now','today'] or getNumber(requestInfo['location'], time2) == -1 or time2 in ['now','today']:
            print("Sorry the date you entered is not recorded yet.")
            print("The latest recorded date is:",list(date_map.keys())[-1])
        else:
            if time1.count('-') == 2:
                if requestInfo['comp'] == 'more':
                    if getNumber(requestInfo['location'], time1) > getNumber(requestInfo['location'], time2):
                        print("Yes, there are more cases on {} than {}".format(time1,time2))
                    elif getNumber(requestInfo['location'], time1) < getNumber(requestInfo['location'], time2):
                        print("No, there are less cases on {} than {}".format(time1,time2))
                    elif getNumber(requestInfo['location'], time1) == getNumber(requestInfo['location'], time2):
                        print("No, the number of cases remains the same")

# Reset the information
def reset(requestInfo):
    for i in requestInfo.keys():
        requestInfo[i] = ''
    return requestInfo


# Tokenize the message
def tokenizer(msg):
    msg = msg.split(' ')
    words = []
    for word in msg:
        if word.count("-") == 2:
            words.append(word)
        elif word.isalnum() or "_" in word:
            words.append(word.lower())
    return words

# Verify words
def verify(words,lexicon):
    dic = []
    for i in lexicon:
        dic.append(i[1])
    for word in words:
        if word not in dic:
            return -1

city_list = ['Anaheim','Costa_Mesa', 'Huntington_Beach', 'Irvine', 'Laguna_Hills', 'Lake_Forest','Newport_Beach','Orange', 'Santa_Ana', 'Tustin', "Orange_County"]
def main():
    global requestInfo
    count = 0
    print("Welcome to the chatbot about Covid information in Orange County")
    print("Currently, this chatbot can answer question about the current count of cases\ndaily and monthy in the supported cities and overall count in OC \nAnd, it can also compare two days' counts\n")
    print("The latest recorded date is {}. Please enter date in this format.\n".format(list(date_map.keys())[-1]))
    cities = ""
    for i in city_list:
        if i != city_list[-1]:
            cities += i
            cities += ", "
        else:
             cities += i
    print("The supported cities are: {}. Please enter the names as provided.\n".format(cities))
    while True:
        if count == 0:
            message = input("Please enter your message (S to stop the chat): ")
        else:
            requestInfo = reset(requestInfo)
            message = input("\nPlease enter your message (S to stop the chat): ")
        count += 1
        if message == 'S':
            break
        words = tokenizer(message)
        grammar = CYKParse.getGrammarCovid()
        priorCYK = False
        for word in words:
            if '-' in word:
                if word not in date_map.keys():
                    priorCYK = True
        if priorCYK == True:
            requestInfo['special'] = 1
            reply()
        else:
            T, P = CYKParse.CYKParse(words, grammar)
            sentenceTree = getSentenceParse(T)
            if sentenceTree == -1 or verify(words,grammar['lexicon']) == -1:
                print("Sorry I can not understand your message, please enter the message agin.")
            else:
                updateRequestInfo(sentenceTree)
                reply()
        
main()