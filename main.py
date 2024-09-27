import streamlit as st

# Title of the app
st.title("Celebrity Info App")

# Text to display Shah Rukh Khan's information initially
info_sharukh = """
**Shah Rukh Khan** is an Indian actor, film producer, and television personality. He is known as the "King of Bollywood", having appeared in more than 80 Bollywood films.
He has a massive fan following and has won numerous awards for his contribution to Indian cinema.
"""

info_angelina = """
**Angelina Jolie** is an American actress, filmmaker, and humanitarian. She has received various accolades, including an Academy Award and three Golden Globe Awards.
Jolie is also known for her humanitarian work and is a Special Envoy for the UN Refugee Agency.
"""

# Display initial information about Shah Rukh Khan
if "show_jolie" not in st.session_state:
    st.session_state.show_jolie = False

if st.session_state.show_jolie:
    st.markdown(info_angelina)
else:
    st.markdown(info_sharukh)

# Button to toggle information
if st.button("Show information about Angelina Jolie"):
    st.session_state.show_jolie = True
