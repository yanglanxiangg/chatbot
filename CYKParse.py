# Code for CS 171, Winter, 2021

import Tree
import Covid

verbose = False
def printV(*args):
    if verbose:
        print(*args)

# A Python implementation of the AIMA CYK-Parse algorithm in Fig. 23.5 (p. 837).
def CYKParse(words, grammar):
    T = {}
    P = {}
    # Instead of explicitly initializing all P[X, i, k] to 0, store
    # only non-0 keys, and use this helper function to return 0 as needed.
    def getP(X, i, k):
        key = str(X) + '/' + str(i) + '/' + str(k)
        if key in P:
            return P[key]
        else:
            return 0
    # Insert lexical categories for each word
    for i in range(len(words)):
        for X, p in getGrammarLexicalRules(grammar, words[i]):
            P[X + '/' + str(i) + '/' + str(i)] = p
            T[X + '/' + str(i) + '/' + str(i)] = Tree.Tree(X, None, None, lexiconItem=words[i])
    printV('P:', P)
    printV('T:', [str(t)+':'+str(T[t]) for t in T])
    # Construct X_i:j from Y_i:j + Z_j+i:k, shortest spans first
    for i, j, k in subspans(len(words)):
        for X, Y, Z, p in getGrammarSyntaxRules(grammar):
            printV('i:', i, 'j:', j, 'k:', k, '', X, '->', Y, Z, '['+str(p)+']', 
                    'PYZ =' ,getP(Y, i, j), getP(Z, j+1, k), p, '=', getP(Y, i, j) * getP(Z, j+1, k) * p)
            PYZ = getP(Y, i, j) * getP(Z, j+1, k) * p
            if PYZ > getP(X, i, k):
                printV('     inserting from', i, '-', k, ' ', X, '->', T[Y+'/'+str(i)+'/'+str(j)], T[Z+'/'+str(j+1)+'/'+str(k)],
                            'because', PYZ, '=', getP(Y, i, j), '*', getP(Z, j+1, k), '*', p, '>', getP(X, i, k), '=',
                            'getP(' + X + ',' + str(i) + ',' + str(k) + ')')
                P[X + '/' + str(i) + '/' + str(k)] = PYZ
                T[X + '/' + str(i) + '/' + str(k)] = Tree.Tree(X, T[Y+'/'+str(i)+'/'+str(j)], T[Z+'/'+str(j+1)+'/'+str(k)])
    printV('T:', [str(t)+':'+str(T[t]) for t in T])
    return T, P

# Python uses 0-based indexing, requiring some changes from the book's
# 1-based indexing: i starts at 0 instead of 1
def subspans(N):
    for length in range(2, N+1):
        for i in range(N+1 - length):
            k = i + length - 1
            for j in range(i, k):
                yield i, j, k

# These two getXXX functions use yield instead of return so that a single pair can be sent back,
# and since that pair is a tuple, Python permits a friendly 'X, p' syntax
# in the calling routine.
def getGrammarLexicalRules(grammar, word):
    for rule in grammar['lexicon']:
        if rule[1] == word:
            yield rule[0], rule[2]

def getGrammarSyntaxRules(grammar):
    rulelist = []
    for rule in grammar['syntax']:
        yield rule[0], rule[1], rule[2], rule[3]

# 'Grammar' here is used to include both the syntax part and the lexicon part.
def getGrammarCovid():
    date_map,_,_ ,_,_ ,_,_ ,_,_ ,_,_,_ = Covid.getData('Anaheim','Costa_Mesa', 'Huntington_Beach', 'Irvine', 'Laguna_Hills', 'Lake_Forest','Newport_Beach','Orange', 'Santa_Ana', 'Tustin','Total')
    total_days = len(date_map.keys())
    dic = {
        'syntax' : [
            ['S', 'S', 'AdverbPhrase', 0.20],
            ['S', 'NP+AdverbPhrase', 'VP', 0.16],
            ['S', 'WQuestion', 'VP', 0.16],
            ['S', 'WQuestion', 'S', 0.16],
            ['S', 'VP', 'NP', 0.16],
            ['S', 'S', 'Conj+Adverb', 0.16],
            ['NP', 'Article', 'Noun', 0.25],
            ['NP', 'Adjective', 'Noun', 0.25],
            ['NP', 'Article', 'NP', 0.25],
            ['NP', 'Comp', 'Noun', 0.25],
            ['VP', 'Verb', 'Adverb', 0.4],
            ['VP', 'Verb', 'PassiveVerb', 0.2],
            ['VP', 'Verb', 'NP+AdverbPhrase', 0.3],
            ['VP', 'VP', 'Adjective', 0.1],
            ['NP+AdverbPhrase','AdverbPhrase','Noun',0.5],
            ['NP+AdverbPhrase', 'NP', 'AdverbPhrase', 0.5],
            ['AdverbPhrase','InterAdverb','Adjective',0.2],
            ['AdverbPhrase', 'Preposition', 'Name', 0.1],
            ['AdverbPhrase', 'Preposition', 'Noun', 0.05],
            ['AdverbPhrase', 'Preposition', 'Date', 0.05],
            ['AdverbPhrase', 'Preposition', 'Date+Conj', 0.05],
            ['AdverbPhrase','InterAdverb','Adjective',0.2],
            ['AdverbPhrase','AdverbPhrase','NP',0.1],
            ['AdverbPhrase', 'AdverbPhrase', 'Adverb', 0.2],
            ['AdverbPhrase', 'AdverbPhrase', 'AdverbPhrase', 0.1],
            ['Conj+Adverb', 'Adverb', 'Conj+Adverb', 0.5],
            ['Conj+Adverb', 'Conj', 'Adverb', 0.5],
            ['Date+Conj', 'Conj', 'Date', 0.5],
            ['Date+Conj', 'Date', 'Date+Conj', 0.5]
        ],
        'lexicon' : [
            ['InterAdverb', 'how', 1.0],
            ['Noun', 'cases', 0.5],
            ['Noun', 'number', 0.3],
            ['Noun', 'month', 0.1],
            ['Noun', 'people', 0.1],
            ['Verb', 'are', 0.5],
            ['Verb', 'is', 0.5],
            ['PassiveVerb', 'reported',0.5],
            ['PassiveVerb', 'tested',0.5],
            ['Adverb', 'now', 0.3],
            ['Adverb', 'today', 0.4],
            ['Adverb', 'there', 0.15],
            ['Adverb', 'yesterday', 0.15],
            ['Adjective', 'many', 0.25],
            ['Adjective', 'positive', 0.25],
            ['Adjective', 'total', 0.25],
            ['Adjective', 'cumulative', 0.25],
            ['Article', 'the', 0.8],
            ['Article', 'this', 0.2],
            ['Preposition', 'in', 0.5],
            ['Preposition', 'of', 0.25],
            ['Preposition', 'on', 0.25],
            ['Name','anaheim',0.1],
            ['Name','costa_mesa',0.1],
            ['Name','huntington_beach',0.1],
            ['Name','irvine',0.1],
            ['Name','laguna_hills',0.1],
            ['Name','lake_forest',0.1],
            ['Name','newport_beach',0.1],
            ['Name','orange',0.1],
            ['Name','santa ana',0.1],
            ['Name','tustin',0.05],
            ['Name','orange_county',0.05],
            ['WQuestion','what',1.0],
            ['Comp','more',0.5],
            ['Comp','less',0.5],
            ['Conj', 'than', 1]
         ]
    }
    for date in date_map.keys():
        l = ['Date',date,1/total_days]
        dic['lexicon'].append(l)
    return dic

# Unit testing code
if __name__ == '__main__':
    verbose = True
    #CYKParse(['how','many','cases','are','there','in','Irvine','now'], getGrammarCovid())
    #CYKParse(['how','many','cases','are','reported','in','Irvine','today'], getGrammarCovid())
    #CYKParse(['what', 'is', 'the', 'number', 'of', 'cases', 'in', 'Irvine', 'on', '23-Feb-21'], getGrammarCovid())
    #CYKParse(['what', 'is', 'the', 'number', 'of', 'cases', 'in', 'Irvine'], getGrammarCovid())
    #CYKParse(['what', 'is', 'the', 'cumulative', 'number', 'of', 'cases', 'in', 'Irvine'], getGrammarCovid())
    #CYKParse(['are','there','more','cases','today','than','yesterday'], getGrammarCovid())
    #CYKParse(['are','there','more','cases','on', '23-Feb-21', 'than','24-Feb-21', 'in', 'Irvine'], getGrammarCovid())
    #CYKParse(['how','many','cases','are','reported','in','Irvine','this','month'], getGrammarCovid())
    #CYKParse(['what', 'is', 'the', 'cumulative', 'number', 'of', 'cases', 'in', 'Irvine', 'on', '1-Feb-21'], getGrammarCovid())
    #CYKParse(['are','there','more','cases','on', '23-Feb-21', 'than','24-Feb-21', 'in', 'Irvine'], getGrammarCovid())
    #CYKParse(['how','many','people','are','tested','positive','in','irvine','now'], getGrammarCovid())
