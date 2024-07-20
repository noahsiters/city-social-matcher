import matcher
import jotform_api
import json
import submission
import operator
import random

# have tests that shuffle the order of inputs, and tests that switch the order by girls instead of guys
def testStableMatching():
    preferences = {
        'Noah': ['Natalie', 'Brianna', 'Katie', 'Sarah', 'Dana', 'Kate', 'Taylor'],
        'Nat': ['Natalie', 'Brianna', 'Katie', 'Dana', 'Kate', 'Taylor', 'Sarah'],
        'Chad': ['Katie', 'Kate', 'Natalie', 'Sarah', 'Brianna', 'Taylor', 'Dana'],
        'Evan': ['Sarah', 'Natalie', 'Katie', 'Brianna', 'Kate', 'Taylor', 'Dana'],
        'Patrick': ['Sarah', 'Natalie', 'Kate', 'Katie', 'Taylor', 'Brianna', 'Dana'],
        'Jesue': ['Taylor', 'Katie', 'Natalie', 'Brianna', 'Dana', 'Sarah', 'Kate'],
        'Will': ['Brianna', 'Natalie', 'Kate', 'Dana', 'Katie', 'Sarah', 'Taylor'],
        'Natalie': ['Nat', 'Noah', 'Evan', 'Patrick', 'Will', 'Chad', 'Jesue'],
        'Dana': ['Will', 'Noah', 'Nat', 'Jesue', 'Patrick', 'Chad', 'Evan'],
        'Kate': ['Patrick', 'Chad', 'Will', 'Noah', 'Nat', 'Evan', 'Jesue'],
        'Sarah': ['Evan', 'Patrick', 'Noah', 'Chad', 'Will', 'Nat', 'Jesue'],
        'Brianna': ['Will', 'Nat', 'Noah', 'Chad', 'Evan', 'Patrick', 'Jesue'],
        'Taylor': ['Patrick', 'Jesue', 'Chad', 'Will', 'Nat', 'Noah', 'Evan'],
        'Katie': ['Chad', 'Patrick', 'Evan', 'Noah', 'Nat', 'Will', 'Jesue']
        }
    
    males = ['Noah', 'Nat', 'Chad', 'Evan', 'Patrick', 'Jesue', 'Will']
    females = ['Natalie', 'Dana', 'Kate', 'Sarah', 'Brianna', 'Taylor', 'Katie']

    random.shuffle(males)

    matches = gale_shapley(preferences, males)

    print(f'\nMatches\n{matches}')
    
    
    for key in preferences:
        print(preferences.get(key))

def gale_shapley(prefs, proposers):
    matches = []
    while len(proposers) > 0:  #terminating condition - all proposers are matched
        proposer = proposers.pop(0)  #Each round - proposer is popped from the free list
        proposee = prefs[proposer].pop(0)  #Each round - the proposer's top preference is popped
        matchLen= len(matches)
        found = False
        
        for index in range(matchLen):  
            match = matches[index]
            if proposee in match:  #proposee is already matched
                found = True
                temp = match.copy()
                temp.remove(proposee)
                matchee = temp.pop()
                if prefs[proposee].index(proposer) < prefs[proposee].index(matchee):  #proposer is a higher preference 
                    matches.remove(match)  #remove old match
                    matches.append([proposer, proposee])  #create new match with proposer
                    proposers.append(matchee)  #add the previous proposer to the free list of proposers
                else:
                    proposers.append(proposer)  #proposer wasn't a higher prefence, so gets put back on free list
                break
            else:
                continue
        if not found:  #proposee was not previously matched so is automatically matched to proposer
            matches.append([proposer, proposee])
        else:
            continue
    return matches

def test():
    testStableMatching()

test()