from openai import OpenAI
from dotenv import load_dotenv
import os
import sqlite3
import streamlit as st
st.set_page_config(layout="wide")
st.set_page_config(
    page_title="Hear Me Out",
    page_icon="📣",
    layout="wide"
)


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

h1, h2, h3, h4, h5, h6, p, label, input, button, li, .stMarkdown{
    font-family: 'Poppins', sans-serif !important;      
}


div.stButton > button {
    background: linear-gradient(135deg, #00B894, #00B894);
    color: black;
    border: none;
    border-radius: 12px;
    padding: 0.5rem 1.75rem;
    font-weight: 700;
    font-size: 1rem;
    transition: opacity 0.2s, transform 0.1s;
}
div.stButton > button:hover {
    opacity: 0.88;
    transform: translateY(-1px);
    color: white;
}
div.stButton > button:active {
    transform: scale(0.97);
}

/* Sidebar — sunny yellow tint */
section[data-testid="stSidebar"] {
    background-color: #A8E6CF;
    border-right: 2px solid #FC9F5B;
}
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stSlider label,
section[data-testid="stSidebar"] .stNumberInput label,
section[data-testid="stSidebar"] .stTextArea label {
    font-weight: 700;
    color: #1C1C2E;
}

/* Slider thumb — teal */
div[data-testid="stSlider"] div[role="slider"] {
    background-color: #009978 !important;
}
.stApp {
    background-color: #FFF3B0 !important;
}
header[data-testid="stHeader"] {
    background-color: #FFF3B0 !important;
}
/* Headings */
h1 { color: #2D3436; }
h3 { color: #2D3436; }

/* Chat message — mint with teal border */
div[data-testid="stChatMessage"] {
    background-color: #EDFFF8;
    border-left: 4px solid #00C9A7;
    border-radius: 12px;
    padding: 0.5rem
}

/* Caption — orange pill badge */
div[data-testid="stCaptionContainer"] p {
    background: #FF8C42;
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    color: white;

}
</style>
""", unsafe_allow_html=True)

# 1. Setup
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def AI_solutions(feedback, passion, urgency):
    system_role_prompt = f'''
    You are a kind and helpful system that helps students figure out their feedback to give to the school, and also help make a clear solution to improve the school.
    Your main goal is to give them a clear view of their plan and problem and empower them to improve the problem / solve it.
    '''

    user_role_prompt = f'''
    You are Hear Me Out, a system that helps underrepresented kids who feel disconnected from their school and have no impact on it.
    - You help them by identify the main problem they are trying to solve/report in that feedback, {feedback}
    - Then help them brainstorm solutions for that problem
    - Then you help them make a plan to execute their solutions based on their {urgency}
    Always adjust based on their passion level, {passion}.
    - YOU MUST MUST MUST PROVIDE CONCRETE SOLUTIONS! Remember, these are underrepresented kids that were brave enough to submit! Make something that they can actually do! (e.g. hallways are too boring = Hallway Beautification Committee instead of 'add color')
    '''

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_role_prompt},
            {"role": "user", "content": user_role_prompt}
        ]
    )

    return response.choices[0].message.content

def AI_connection(solution, file, feedback, grade, name):
    system_role_prompt = f'''
    You are a kind and helpful system that helps students figure out their feedback to give to the school, and also help make a clear solution to improve the school.
    Your main goal is to and connect them with other students/authority figures/teachers/etc. that can help them feel less alone.
    '''

    user_role_prompt = f'''
    - You run through the student records database below, {file}, and connect them to authority figures and/or kids with the same ideas as their's, {solution}.
    The student's name is {name}
    Their grade is {grade}
    Their feedback is {feedback}
    And their solution is {solution}
    This is the most important step, so you have to make sure that the students' ideas are similar, and provide the name of the person, their idea, and the contact information for that person exactly in the format below:
    Let's get you connected! Here are some students with similar ideas that can get your plan off the ground:
    - [Name]: [idea], [feedback] - [contact information], [grade].
    - [Name]: [idea], [feedback] - [contact information], [grade].
    - etc.
    Be quite generous when matching - find common words, ideals, themes, or solutions in their feedbacks too, {feedback}! The ultimate goal is to have people come out of their shell!
    Encourage the people to get connected to each other.
    IMPORTANT: If NO PEOPLE WITH THE SAME IDEA are found inside the student database, {file}, connect them to the authority figures, like the principal, superintendent, clubs, etc. below:
    
    Authority figures:
    - Principal Dumbledore: lemondrops@schools.org
    - Superintendent Chalmers: skinner@schools.org
    - Dr. Harleen Quinzel, counselor: puppeteer@schools.org

    Teachers:
    - Mr. Skywalker, teaches PE: lukeiamyourfather@schools.org
    - Prof. McGonagall, teaches language arts: catsarecool@schools.org
    - Ms. Frizzle, teaches science: thefrizzler@schools.org
    - Dr. Ryland Grace, teaches flight and space: iloverocky@schools.org
    - Dr. Donald Duk, teaches math: mathmagicland@schools.org
    - Mr. Bob Ross, teaches art: happylittletrees@schools.org
    - Miss Honey, teaches philosophy: sweetashoney@schools.org
    - Prof. Hagrid, teaches animal sciences: ishouldnothavesaidthat@schools.org
    - Mrs. Puff, teaches automative mechanics: ohneptune@schools.org
    - Mr. Ratburn, teaches spelling: isitcake@schools.org
    - Mr. Aaron Burr, teaches history: talklessmilemore@schools.org
    - Ms. Circe, teaches psychology: ivegotallthepower@schools.org
    - Ms. Angelica Schuyler, teaches women's studies: amindatworkwork@schools.org
    - Ms. Jenny Lind, teaches choir: neverenough@schools.org

    Clubs:
    - Self Defense Club: theDA@clubs.org. Leader - Harry Potter: pottermore@students.org
    - Sports Club: thejocks@clubs.org. Leader - Oliver Wood: ilovequidditch@students.org
    - Drama Club: dramaqueensandkings@clubs.org. Leader - Sharpay Evans: fabuloussharpay@students.org
    - Newspaper Club: extraextra@clubs.org. Leader - Rory Gilmore: whocaresifimprettyififailmyfinals@students.org
    - Decathlon Team: thesmarties@clubs.org. Leader - Michelle Jones: dontcallmemichellejones@students.org
    - Cheerleading Squad: cheerocracy@clubs.org. Leader - Torrance Shipman: bringiton@students.org
    - Basketball Team: bball@clubs.org. Leader - Troy Bolton: allinthistogether@students.org
    - Choir: lalala@clubs.org. Leader - Veronica Lodge: thepussycats@students.org

    Student council:
    - Paris Geller, president: sleepwhenyouredead@students.org
    - Cher Horowitz, vice president: asif@students.org
    - Dwight Schrute, presidential advisor: perfectenschlag@students.org
    - Peter Parker, publicist commissioner: spooderman@students.org
    - Gumball Watterson, activities commissioner: whatthewhat@students.org
    - Blair Waldorf, treasurer: gossipgirl@students.org
    - Hermione Granger, secretary: spew@students.org

    MOST IMPORTANTLY: encourage!! encourage!! encourage!!
    '''

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_role_prompt},
            {"role": "user", "content": user_role_prompt}
        ]
    )

    return response.choices[0].message.content


# 2. Streamlit UI
st.title("Hear Me Out")
st.write("Have some feedback that will help [school name]? I'll help you identify the problem, generate possible solutions, and plan it! Then we'll connect you with some students with similar ideas, the school admin, and student council.")

#UI
st.sidebar.header("Profile ✨:")
feedback = st.sidebar.text_input("Your feedback:")
name = st.sidebar.text_input("Your name:")
age = st.sidebar.number_input("Your grade:", min_value=0, max_value=12)
contact = st.sidebar.text_input("Your contact info:")
passion = st.sidebar.slider("Passion level:", min_value=0, max_value=10)
urgency = st.sidebar.slider("Urgency level:", min_value=0, max_value=10)

conn = sqlite3.connect('school_ideas.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS users (name TEXT, grade INTEGER, email TEXT, feedback TEXT, idea TEXT)')
conn.commit() 

#tabs
tab1, tab2, tab3, tab4 = st.tabs(["💡 Solutions", "🔗 Get Connected", "📋 My Action Plan", "📱 Contact Directory"])

with tab1:
    if "AI_sol_output" not in st.session_state:
        st.session_state.AI_sol_output = None

    st.write("Brainstorm solutions, create a plan, and get connected here!")
    if st.button("Brainstorm solutions"):
        with st.spinner("Brainstorming solutions..."):
            st.session_state.AI_sol_output = AI_solutions(feedback, passion, urgency)

    if st.session_state.AI_sol_output:
        st.write(st.session_state.AI_sol_output)
        

with tab2:
    chosen_sol = st.text_input("Type your chosen solution here!: ")
    if st.button("Submit chosen solution"):
        if chosen_sol:

            cursor.execute('SELECT * FROM users')
            records = cursor.fetchall()

            text_conversion = ""
            for row in records:
                text_conversion += f"Name: {row[0]}, Grade: {row[1]}, Contact: {row[2]}, Feedback: {row[3]}, Idea: {row[4]}\n"

            cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?)", (name, age, contact, feedback, chosen_sol))
            conn.commit()

            with st.spinner("Searching the database..."):
                connection_output = AI_connection(chosen_sol, text_conversion, feedback, age, name)
                st.write(connection_output)
                st.success("Your feedback has been safely submitted to the database! 🎉")
                st.balloons()


with tab3:
    st.header("📋 Your Action Plan")
    st.write("What are your next steps? Build your plan and organize your thoughts below!")

    if "todo_list" not in st.session_state:
        st.session_state.todo_list = [
            "Brainstorm a solution",
            "Get connected!"
        ]
    
    new_task = st.text_input("Add a new step to your plan:")

    if st.button("Add step"):
        if new_task:
            st.session_state.todo_list.append(new_task)
            st.toast("Task added to your action plan! ✨")
            st.rerun()
    
    st.write("My plan:")
    for task in st.session_state.todo_list:
        st.checkbox(task)

    st.write("---")
    if "todo_list" in st.session_state and len(st.session_state.todo_list) > 0:
        my_plan = "My Hear Me Out Action Plan\n\n"

        for task in st.session_state.todo_list:
            my_plan += f"[] {task}\n"

        st.download_button(
            label = "📥 Download Action Plan",
            data = my_plan,
            file_name = "My_Action_Plan.txt",
            mime="text/plain"
        )


with tab4:
    st.header("📱 Contact Directory")
    st.markdown("""
    Authority figures:
    - Principal Dumbledore: lemondrops@schools.org
    - Superintendent Chalmers: skinner@schools.org
    
    Staff:
    - Dr. Harleen Quinzel, counselor: joking@schools.org
    - Mrs. DePoint, lunch lady: eatupeatup@schools.org
    - Mike Wazowski, janitor: schmoopsiepoo@schools.org

    Teachers:
    - Mr. Skywalker, teaches PE: lukeiamyourfather@schools.org
    - Prof. McGonagall, teaches language arts: catsarecool@schools.org
    - Ms. Frizzle, teaches science: thefrizzler@schools.org
    - Dr. Ryland Grace, teaches flight and space: iloverocky@schools.org
    - Dr. Donald Duk, teaches math: mathmagicland@schools.org
    - Mr. Bob Ross, teaches art: happylittletrees@schools.org
    - Miss Honey, teaches philosophy: sweetashoney@schools.org
    - Prof. Hagrid, teaches animal sciences: ishouldnothavesaidthat@schools.org
    - Mrs. Puff, teaches automative mechanics: ohneptune@schools.org
    - Mr. Ratburn, teaches spelling: isitcake@schools.org
    - Mr. Aaron Burr, teaches history: talklessmilemore@schools.org
    - Ms. Circe, teaches psychology: ivegotallthepower@schools.org
    - Ms. Angelica Schuyler, teaches women's studies: amindatworkwork@schools.org
    - Ms. Jenny Lind, teaches choir: neverenough@schools.org

    Clubs:
    - Self Defense Club: theDA@clubs.org. Leader - Harry Potter: pottermore@students.org
    - Sports Club: thejocks@clubs.org. Leader - Oliver Wood: ilovequidditch@students.org
    - Drama Club: dramaqueensandkings@clubs.org. Leader - Sharpay Evans: fabuloussharpay@students.org
    - Newspaper Club: extraextra@clubs.org. Leader - Rory Gilmore: whocaresifimprettyififailmyfinals@students.org
    - Decathlon Team: thesmarties@clubs.org. Leader - Michelle Jones: dontcallmemichellejones@students.org
    - Cheerleading Squad: cheerocracy@clubs.org. Leader - Torrance Shipman: bringiton@students.org
    - Basketball Team: bball@clubs.org. Leader - Troy Bolton: allinthistogether@students.org
    - Choir: lalala@clubs.org. Leader - Veronica Lodge: thepussycats@students.org

    Student council:
    - Paris Geller, president: sleepwhenyouredead@students.org
    - Cher Horowitz, vice president: asif@students.org
    - Dwight Schrute, presidential advisor: perfectenschlag@students.org
    - Peter Parker, publicist commissioner: spooderman@students.org
    - Gumball Watterson, activities commissioner: whatthewhat@students.org
    - Blair Waldorf, treasurer: gossipgirl@students.org
    - Hermione Granger, secretary: winguardiumleviosa@students.org
    """)
