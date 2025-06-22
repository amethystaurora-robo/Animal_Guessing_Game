import streamlit as st
import pandas as pd
import re

st.title("🐾 Animal Guessing Game")
st.markdown("### Think of an animal, and I'll try to guess it in 20 questions or less.")
st.markdown("---")

# Sample animal_df. Replace with your actual DataFrame.
animal_df = pd.read_csv("animals_fixed.csv")

# Helper
def make_an(next_word):
    vowels = re.compile("^[aeiouAEIOU]")
    return 'an' if vowels.match(next_word) else 'a'

# Initialize session state
if 'question_counter' not in st.session_state:
    st.session_state.question_counter = 1
if 'filtered_animals' not in st.session_state:
    st.session_state.filtered_animals = animal_df.copy()
if 'current_column_index' not in st.session_state:
    st.session_state.current_column_index = 0
if 'current_animal_index' not in st.session_state:
    st.session_state.current_animal_index = 0
if 'game_over' not in st.session_state:
    st.session_state.game_over = False

columns = ['domesticated','diet','habitat','Kingdom','region','subtype','species']

def ask_question():
    col_idx = st.session_state.current_column_index
    if col_idx >= len(columns):
        st.session_state.game_over = True
        return

    column = columns[col_idx]
    animals = st.session_state.filtered_animals[column].dropna().sort_values().unique().tolist()

    # End if game is over or no more animals
    if not animals or st.session_state.game_over:
        return

        # Check if we've run out of options in this column
    if st.session_state.current_animal_index >= len(animals):
        if column == 'species':
            st.error("I give up. You win! 🎉")
            st.session_state.game_over = True
        else:
            st.write("No match in this category — moving on!")
            st.session_state.current_column_index += 1
            st.session_state.current_animal_index = 0
            st.experimental_rerun()
        return  # Always return after rerun or ending

    # If we’ve reached the last animal in the column and not in final column, auto-confirm
    if st.session_state.current_animal_index >= len(animals)-1:
        if column != 'species':
            # Auto-confirm the last option
            last_animal = animals[-1]
            st.write(f"I'm guessing it's {make_an(last_animal)} {last_animal} — moving on!")
            st.session_state.filtered_animals = st.session_state.filtered_animals[
                (st.session_state.filtered_animals[column] == last_animal) |
                (st.session_state.filtered_animals[column].isna())
            ]
            st.session_state.current_column_index += 1
            st.session_state.current_animal_index = 0
            st.session_state.question_counter += 1
            st.experimental_rerun()
            return
        else:
            # Final column — do not auto-confirm, just proceed to ask the final question
            pass  # Do nothing — let it reach the question display below

        # Freeze question target values for this interaction
    animal = animals[st.session_state.current_animal_index]
    col_name = column  # freeze the column name

    article = make_an(animal)


    st.write(f"Question {st.session_state.question_counter}: Is it {article} {animal}?")

    col = column

    #st.write(f"Current column: {column}")
    #st.write(f"Remaining options: {animals}")
    #st.write(f"Current animal index: {st.session_state.current_animal_index}")
    #st.write(f"Current size of dataset: {len(st.session_state.filtered_animals)}")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yes", key=f"yes_{column}_{animal}_{st.session_state.question_counter}"):
            st.session_state.question_counter += 1
            # Filter only when the user says YES
            if column == 'species':
                st.success(f"Great, so it's a {animal}! I win!")
                st.session_state.game_over = True
            else:
                st.session_state.filtered_animals = st.session_state.filtered_animals[
                    (st.session_state.filtered_animals[column] == animal) |
                    (st.session_state.filtered_animals[column].isna())
                ]
                st.session_state.current_animal_index = 0
                st.session_state.current_column_index += 1
                st.experimental_rerun()
    with col2:
        if st.button("No", key=f"no_{column}_{animal}_{st.session_state.question_counter}"):
            st.session_state.question_counter += 1
            st.session_state.current_animal_index += 1
            st.experimental_rerun()

    # Game end checks
    if len(st.session_state.filtered_animals) == 0:
        st.error("I'm out of ideas. You win!")
        st.session_state.game_over = True
    elif st.session_state.question_counter > 20:
        st.error("That's 20 questions! You win!")
        st.session_state.game_over = True

# Run the game
if st.session_state.current_column_index < len(columns) and not st.session_state.game_over:
    ask_question()
else:
    st.write("Game over or no more questions.")

# Reset button
if st.button("Restart Game"):
    st.session_state.question_counter = 1
    st.session_state.filtered_animals = animal_df.copy()
    st.session_state.current_column_index = 0
    st.session_state.current_animal_index = 0
    st.session_state.game_over = False
    st.experimental_rerun()
