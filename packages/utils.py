import streamlit as st
import seaborn as sns
import pandas as pd

# State management -----------------------------------------------------------

# I like to use state instead of the long form 
state = st.session_state


def init_state(key, value):
  if key not in state:
    state[key] = value

init_state('login_successful', False)
init_state('username', '')
init_state('password', '')
print(state)
print(state.login_successful)

# generic callback to set state
def _set_state_cb(**kwargs):
    for state_key, widget_key in kwargs.items():
        val = state.get(widget_key, None)
        if val is not None or val == "":
            setattr(state, state_key, state[widget_key])

def _set_login_cb(username, password):
    state.login_successful = login(username, password)  

def _reset_login_cb():
    state.login_successful = False
    state.username = ""
    state.password = "" 

# print('a')
# init_state('login_successful', False)
# init_state('username', '')
# init_state('password', '')
# print(state.login_successful)
# -----------------------------------------------------------------------------

# Function to check login credentials
def login(username, password):
    return username == "jsmith" and password == "password"

def main2():
    st.sidebar.button("Logout", on_click=_reset_login_cb)
    st.subheader("My Page")
    st.write("Hello")

### Main function
def authorisation():
    state = st.session_state
    init_state('login_successful', False)
    init_state('username', '')
    init_state('password', '')
    ### If login is successful, display "Hello"
    if state.login_successful:
        # st.sidebar.subheader("utils.py")
        # st.sidebar.
        st.sidebar.write(f"*Welcome, {state.username}*")
        st.sidebar.button("Logout", on_click=_reset_login_cb)
        return True
    else:
        st.title("Countries Dashboard")
        st.subheader("Login")
        st.info(
            """The login page for this dashboard is for illustrative purposes only. Please use the credentials below:

Username:  `jsmith`

Password:  ```password```
            """, 
            icon="ℹ️"
        )

        ### Display login form
        st.text_input(
            "Username:", value=state.username, key='username_input',
            on_change=_set_state_cb, kwargs={'username': 'username_input'}
        )
        st.text_input(
            "Password:", type="password", value=state.password, key='password_input',
            on_change=_set_state_cb, kwargs={'password': 'password_input'}
        )
        # st.write(state.username)
        # st.write(state.password)
        # Check login credentials
        if not state.login_successful and st.button("Login", on_click=_set_login_cb, args=(state.username, state.password)):
            st.warning("Wrong username or password.")

def load_datasets():
    ### dataset 1 - from seaborn
    # df1 = sns.load_dataset('healthexp')
    # df1['Country'] = df1['Country'].replace({'Great Britain':'United Kingdom'})
    ### dataset 1 - a fuller version downloaded from online
    df1 = pd.read_csv('data/life-expectancy-vs-health-expenditure.csv')
    df1_proc = df1.assign(Continent=df1.groupby('Entity')['Continent'].ffill().bfill())
    df1_proc['Entity'] = df1_proc['Entity'].replace({
        'United States': 'USA'
    })
    df1_proc = df1_proc.rename(columns={
        'Entity': 'Country',
        'Population (historical estimates)': 'Population',
        'Life expectancy - Sex: all - Age: at birth - Variant: estimates': 'Life Expectancy',
        'Health expenditure per capita - Total': 'Health Expenditure'
    })
    ### dataset 2
    df2 = pd.read_csv('data/world-data-2023.csv', thousands=',')
    df2['Country'] = df2['Country'].replace({'United States':'USA'})
    return df1_proc, df2

if __name__ == "__main__":
    print('Running "utils.py" on its own.')
    if authorisation():
        main2()

