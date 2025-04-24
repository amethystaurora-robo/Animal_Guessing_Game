import streamlit as st
import pandas as pd
import re

@st.cache_data
def load_data():
    return pd.read_csv("animals_fixed.csv")

animal_df = load_data()
columns = ['domesticated', 'diet', 'habitat', 'Kingdom', 'region', 'subtype', 'species']

# Initialize session state
if 'filtered_animals' not in st.session_state:
    st.session_state.filtered_animals = animal_df.copy()
if 'column_index' not in st.session_state:
    st.session_state.column_index = 0
if 'question_counter' not in st.session_state:
    st.session_state.question_counter = 1

# Restart game
def reset_game():
    st.session_state.filtered_animals = animal_df.copy()
    st.session_state.question_counter = 1

# Determine "a" or "an"
def make_an(word):
    return 'an' if re.match("^[aeiouAEIOU]", str(word)) else 'a'

# UI
st.title("🦁 20 Questions: Animal Edition")
st.header("Think of an animal...")

if st.button("🔁 Restart Game"):
    reset_game()
'''
Right now this displays a list of 20 questions.
Need to fix it so the next question only displays on click of yes or no
To do that need other functions which respond to yes or no click, 
do different responses for each use case
'''
def loop_questions(column,filtered_animals):
    #print("Size of dataset: ",len(filtered_animals))
    list = filtered_animals[column].sort_values().unique().tolist()

    for animal in list:
        st.text(f"Question {st.session_state.question_counter}: ")
        if pd.notna(animal):
            a_an = make_an(animal)
            st.text(f"Is it {a_an} {animal}?")
            response_yes = st.button('Yes')
            response_no = st.button('No')
            st.session_state.question_counter+=1
            if response == "no":
                filtered_animals = filtered_animals.loc[filtered_animals[column]!=animal]
            if (st.session_state.question_counter<=20) & (column=='species') & (response=="yes"):
                st.text(f"Amazing. So it's a {animal}. I win!")
                return filtered_animals
            if (len(filtered_animals[column].unique())==1):
                return filtered_animals
            if response == "yes":
                filtered_animals = filtered_animals.loc[(filtered_animals[column]==animal)|(filtered_animals[column].isna())]
                break
            if (st.session_state.question_counter>20):
                st.text("That's 20 questions! You win!")
                return filtered_animals
            if (len(filtered_animals)==0):
                st.text("I'm out of ideas. You win!")
                return filtered_animals
        
    return filtered_animals

columns = ['domesticated','diet','habitat','Kingdom','region','subtype','species']

for column in range(len(columns)):
    st.session_state.filtered_animals = loop_questions(columns[column],st.session_state.filtered_animals)
    print("Size of dataset: ",len(st.session_state.filtered_animals))

#filtered_animals=animal_df