import numpy as np
import seaborn as sns
import pandas as pd
import re

df = pd.read_csv('animals.txt',on_bad_lines='skip')

df.head(300)

#turn df columns into list
kingdom_list = df.Kingdom.unique().tolist()
type_list = df.type.unique().tolist()
subtype_list = df.type.unique().tolist()
species_list = df.species.unique().tolist()
master_list = [kingdom_list,type_list,subtype_list,species_list]

#iterate through a list and make guesses, return final guess
def count_questions(list, question):
    count=0
    for item in list:
        a_an = make_an(list[count])
        print('Question ' + question + ': Is it ' + a_an + list[count] + '?')
        if yes():
            question = int(question)
            question +=1
            question = str(question)
            return [list[count], question]
        question = int(question)
        if question == 20:
            print('That is 20 questions! You win! Play again?')
            return
        question = str(question)
        count+=1
        question=int(question)
        question+=1
        question=str(question)
            

#chooses a or an for questions with vowels
def make_an(next_word):
    vowels = re.compile("^[aeiouAEIOU]")
    match = vowels.match(next_word)
    if match:
       return 'an '
    else:
       return 'a '

#get user input: yes or no
def yes():
    yes_or_no = input("Type 'yes' or 'no':")
    if yes_or_no == 'yes':
        return True
    else:
        return False

#main, iterate through each column in df until a correct guess is reached
def current_animal():
    try:
        animal_kingdom = count_questions(kingdom_list, str(1))
        current_animal_kingdom = df.type[df.Kingdom==animal_kingdom[0]].unique().tolist()
        animal_type = count_questions(current_animal_kingdom, animal_kingdom[1])
        a_an = make_an(animal_type[0])
        current_animal_type = df.subtype[df.type==animal_type[0]].unique().tolist()
        if len(current_animal_type)==1:
            print('Great! So it is ' + a_an + animal_type[0])
            return
        animal_subtype = count_questions(current_animal_type, animal_type[1])
        current_animal_subtype = df.species[df.subtype==animal_subtype[0]].unique().tolist()
        if len(current_animal_subtype)==1:
            print('Great! So it is ' + a_an + animal_subtype[0])
            return
        animal_species = count_questions(current_animal_subtype, animal_subtype[1])
        a_an = make_an(animal_species[0])
        print('Great! So it is ' + a_an + animal_species[0])
    except NameError:
        print('You win! Play again?')
    except TypeError:
        print('You win! Play again?')
        

#take question number
#add to new question then start that

def question_num(num):
    question = num
    return question

current_animal()