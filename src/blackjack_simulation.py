import random
from tqdm import tqdm
import matplotlib.pyplot as plt
import pandas as pd

def generate_deck():
    deck = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10] * 4
    return deck

def check_win(deposit, base_deposit, deck):
    check = False

    if deposit >= base_deposit * 2:
        check = True

    if deposit <= 0:
        check = True

    if len(deck) <= 10:
        check = True
    
    return check

def check_ace(deck, score):
    if score == 22:
        score -= 10
        deck[1] = 1
    return deck, score, True

def hit(cards, score, deck, extracted, ace):
    card = random.choice(deck)
    cards.append(card)
    extracted.append(card)
    score += card      
    deck.remove(card)
    
    if card == 11 and ace == True:
        cards[-1] = 1
        score -= 10
        
    return cards, score, deck, extracted

def probability(extracted, best_case):
    copy_deck = generate_deck()

    for card_extr in extracted:
        copy_deck.remove(card_extr)

    probability = []
    for best in best_case:
        counter = copy_deck.count(best)
        probability.append((counter / len(copy_deck)) * 100)

    return probability

def check_bust(score):
    if score >= 22:
        return True

    else:
        return False

def check_match(player_score, dealer_score, counter, deposit, bet, base_bet):
    if player_score > dealer_score:
        counter[0] += 1
        deposit += bet * 2
        bet = base_bet

    elif player_score < dealer_score:
        counter[1] += 1
        bet *= 2

    elif player_score == dealer_score:
        deposit += bet

    return counter, deposit, bet

def match(counter, base_deposit, base_bet):
    check = False
    deck = generate_deck()
    extracted = []
    deposit = base_deposit
    bet = base_bet

    while check == False:
        deposit -= bet

        player = []
        dealer = []
        player_score = 0
        dealer_score = 0
        p_ace = False
        d_ace = False

        for i in range(2):
            p_card = random.choice(deck)
            player.append(p_card)
            extracted.append(p_card)
            player_score += p_card            
            deck.remove(p_card)

            d_card = random.choice(deck)
            dealer.append(d_card)
            extracted.append(d_card)
            dealer_score += d_card
            deck.remove(d_card)

        player, player_score, p_ace = check_ace(player, player_score)
        dealer, dealer_score, d_ace = check_ace(dealer, dealer_score)
        
        if dealer_score == 21:
            counter[1] += 1
            bet *= 2
            
        else:
            while player_score < 11:
                player, player_score, deck, extracted = hit(player, player_score, deck, extracted, p_ace)

            best_case = []
            if player_score >= 11 and player_score < 20:
                for best in range(player_score, 20):
                    best_case.append(21 - best)
            
                if len(extracted) > 4: 
                    best_probability = probability(extracted[:3] + extracted[4:], best_case)

                elif len(extracted) == 4:
                    best_probability = probability(extracted[:3], best_case)
                
                audacity = random.randint(20,100)
                if max(best_probability) >= audacity:
                    player, player_score, deck, extracted = hit(player, player_score, deck, extracted, p_ace)

            if check_bust(player_score) == True:
                counter[1] += 1
                bet *= 2

            elif check_bust(player_score) == False:
                while dealer_score < 17:
                    dealer, dealer_score, deck, extracted = hit(dealer, dealer_score, deck, extracted, d_ace)

                if check_bust(dealer_score) == True:
                    counter[0] += 1
                    deposit += (bet * 2)
                    bet = base_bet

                elif check_bust(dealer_score) == False:
                    counter, deposit, bet = check_match(player_score, dealer_score, counter, deposit, bet, base_bet)
        
        check = check_win(deposit, base_deposit, deck)

    return counter

def bet1(counter, deposit, bet):
    counter = match(counter, deposit, bet)

    return counter

counter1 = [0] * 2

data1 = []
percent1 = []
d = []
per = []

matches = 1000000

for deposit in range(100, 1001, 100):
    for x in tqdm(range(matches), ascii=True, desc=f"Matches with deposit = {deposit} in progress"):
        counter1 = bet1(counter1, deposit, 5)
    d.append(deposit)
    d.append(counter1[0])
    d.append(counter1[1])
    data1.append(d)
    d = []

    per.append(deposit)
    per.append((counter1[0]/(counter1[0]+counter1[1])*100))
    per.append((counter1[1]/(counter1[0]+counter1[1])*100))
    percent1.append(per)
    per = []
    
    counter1 = [0] * 2

p1 = pd.DataFrame(percent1, columns=["Deposit","Player (%)","Dealer (%)"])
print(p1)

d1 = pd.DataFrame(data1, columns=["Deposit","Player","Dealer"])
d1.plot(x="Deposit", y=["Player","Dealer"], kind="bar",figsize=(10,8))
plt.show()

'''
counter2 = [0] * 2

data2 = []
percent2 = []
d = []
per = []

matches = 10000     #in order to speed up the execution, the number of games has been reduced

for deposit in range(100, 1001, 100):
    for bet in range(5, 26, 5):
        for x in tqdm(range(matches), ascii=True, desc=f"Matches with deposit = {deposit} and bet = {bet} in progress"):
            counter2 = bet1(counter2, deposit, bet)
        d.append(deposit)
        d.append(bet)
        d.append(counter2[0])
        d.append(counter2[1])
        data2.append(d)
        d = []
        counter2 = [0] * 2

        per.append(deposit)
        per.append(bet)
        per.append((counter2[0]/(counter2[0]+counter2[1])*100))
        per.append((counter2[1]/(counter2[0]+counter2[1])*100))
        percent2.append(per)
        per = []
        
        counter2 = [0] * 2

p2 = pd.DataFrame(percent2, columns=["Deposit","Bet","Player (%)","Dealer (%)"])
print(p1)

d2 = pd.DataFrame(data2, columns=["Deposit","Bet","Player","Dealer"])
d2.plot(x="Deposit", y=["Player","Dealer"], kind="bar",figsize=(30,8))
plt.show()
'''