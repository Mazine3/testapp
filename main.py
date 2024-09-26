import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import re
from PIL import Image
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder
from datetime import datetime
import base64

#Page icon & titre
st.set_page_config(page_title="Prédiction des Quantités Ventes de Médicaments", page_icon="./images/logo.png", layout="wide")


#login
st.header("Predictive Analytics for Future Sales of Medical Products")
st.markdown("An advanced application utilizing machine learning techniques to forecast future sales of medical products. The application aims to leverage historical sales data, market trends, and relevant factors to provide accurate and actionable predictions, enhancing strategic decision-making and optimizing inventory management.")


st.header("")
st.header("")
st.header("")


# i7,i8,i9=st.columns(3)

# with i7:
#     i77 = Image.open('./images/lml.png')
#     st.image(i77, width=390)

# with i8:
#     i88 = Image.open('./images/tte.png')
#     st.image(i88, width=480)

# with i9:
#     i99 = Image.open('./images/bi.png')
#     st.image(i99, width=390)


image = Image.open('./images/logo.png')
with open('./images/logo.png', 'rb') as f:
    image_bytes = f.read()
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
st.sidebar.markdown(f'<div style="display: flex; justify-content: center; align-items: flex-start;"><img src="data:image/png;base64,{image_base64}" width="250"></div>', unsafe_allow_html=True)


#LOGIN BAR
st.sidebar.markdown(" ")
st.sidebar.markdown(" ")
username=st.sidebar.text_input("Username")
password= st.sidebar.text_input("Password",type='password')

if st.sidebar.checkbox("Login"):
    if username=="mhamed" and password=="123":
        st.success("Connected as {}".format(username))
        #Head
        selected = option_menu(
            menu_title=None,
            options=["PREDICTION",'DASHBOARD BI'],  
            icons = ['robot','tv'],
            menu_icon="cast",
            default_index = 0,
            orientation="horizontal",)


        if (selected == 'PREDICTION'):
            
            selected = option_menu(
            menu_title=None,
            options=['ITEM PREDICTION','DATA PREDICTION'],
            icons = ['person','tv'],
            menu_icon="cast",
            default_index = 0,
            orientation="horizontal",)


            if (selected == 'ITEM PREDICTION'):
                # Load the model
                loaded_model = xgb.XGBRegressor()
                loaded_model.load_model("./Model/xgboost_model.json")

                # Encoding dictionary for 'Famille'
                famille_encoding = {
                    "GROSSISTE": 1,
                    "PHARMACIEN": 2,
                    "EXPORT": 3,
                    "SOUSTRAITANT": 4,
                    "MARCHE": 5,
                    "MILITAIRE": 6
                }

                # Load articles and clients data
                articles = pd.read_csv("./Data/Article_name.csv")
                clients = pd.read_csv("./Data/client_names.csv")
                articles_list = articles["Libellé"].unique().tolist()
                clients_list = clients["Raison Sociale"].unique().tolist()

                # Function to get season based on month
                def get_season(month):
                    if month in [12, 1, 2]:
                        return 1  # Winter
                    elif month in [3, 4, 5]:
                        return 2  # Spring
                    elif month in [6, 7, 8]:
                        return 3  # Summer
                    else:
                        return 4  # Fall
                    

                col1,col2,col3=st.columns([1, 2, 1])
                with col2:
                    selected_medicament = st.selectbox("Choose a medication :", articles_list)
                with col2:
                    selected_client = st.selectbox("Choose a client :", clients_list)
                with col2:
                    selected_date = st.date_input("Select a date :", datetime.today())
                    selected_year = selected_date.year
                    selected_month = selected_date.month
                    season = get_season(selected_month)
                with col2:
                    price = st.number_input("Enter the price :", min_value=0.0, step=0.01, format="%.3f")

                with col2:
                    famille = st.selectbox("Select the family :", options=list(famille_encoding.keys()))
                    famille_encoded = famille_encoding[famille]

                def get_result():
                    # Get encoded values for article and client
                    output_article = articles[articles["Libellé"] == selected_medicament]
                    encode_article = output_article["Article"].iloc[0]
                    output_client = clients[clients["Raison Sociale"] == selected_client]
                    encode_client = output_client["Client"].iloc[0]

                    # Prepare data for prediction
                    data = {
                        "Year": [selected_year],
                        "Month": [selected_month],
                        "Season": [season],
                        "Article": [encode_article],
                        "Client": [encode_client],
                        "Prix": [price],
                        "Famille": [famille_encoded]
                    }

                    # Prediction
                    input_data = pd.DataFrame(data)
                    predicted_quantities = loaded_model.predict(input_data)

                    st.success(f"The quantity we predicted for this client is {int(predicted_quantities)} ✅✅")
                
                col1,col2,col3=st.columns(3)
                with col2:
                    st.write(f'<style>div.row-widget.stButton > button:first-child {{background-color: green}}</style>', unsafe_allow_html=True)
                    if st.button('PREDICTION'): 
                        get_result()

            if selected == 'DATA PREDICTION':   # DATA PREDICTION

                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.subheader('PREDICTION WITH DATASET')

                    # number = st.number_input("Insert the Year", value=None, placeholder="Type a Year...")
                    number = st.number_input("Insert the Year", 2014.0, 2035.0, "min", 1.0, format="%.0f", placeholder="Type a Year...")

                    if number:
                        number = int(number)
                        # st.write("The Year is ", number)

                    good_data = None
                    df2 = st.file_uploader("Upload your dataset from here:", type=["csv", "xlsx"])

                    def clean_data(df2):
                        df2 = pd.read_csv(df2, delimiter=';', encoding='latin1')

                        df2 = df2[:-1]
                        df2 = df2.drop_duplicates()
                        df2 = df2.reset_index(drop=True)

                        #date
                        df2['Date'] = pd.to_datetime(df2['Date'], format='%d/%m/%Y', errors='coerce')
                        df2['Day'] = df2['Date'].dt.day
                        df2['Month'] = df2['Date'].dt.month
                        df2['Year'] = df2['Date'].dt.year
                        df2['Season'] = df2['Date'].dt.month % 12 // 3 + 1

                        #price
                        df2["Prix"] = pd.to_numeric(df2["Prix"].str.replace(',', '.').str.strip(), errors='coerce')

                        # Article cleaning
                        for i in range(len(df2)):
                            try:  
                                df2.at[i, "Article"] = int(df2.at[i, "Article"])
                            except ValueError:
                                numeric_part = re.findall(r'\d+', df2.at[i, "Article"])
                                if numeric_part:
                                    df2.at[i, "Article"] = int(numeric_part[0])
                                else:
                                    df2.at[i, "Article"] = None  

                        df2["Article"] = pd.to_numeric(df2["Article"], errors='coerce').fillna(0).astype(int)
                        df2["Client"] = pd.to_numeric(df2["Client"], errors='coerce').fillna(0).astype(int)
                        df2["Quantité"] = pd.to_numeric(df2["Quantité"], errors='coerce').fillna(0).astype(int)

                        # Phase 2
                        final = df2[["Date", "Year", "Month", "Season", "Article", "Libellé", "Client", "Raison Sociale", "Prix", "Famille", "Quantité"]]
                        
                        famille_mapping = {
                            "GROSSISTE": 1,
                            "PHARMACIEN": 2,
                            "EXPORT": 3,
                            "SOUSTRAITANT": 4,
                            "MARCHE": 5,
                            "MILITAIRE": 6}
                        
                        final["Famille"] = final["Famille"].replace(famille_mapping)
                        final["Famille"] = final["Famille"].replace('(Aucun)', None)
                        final["Famille"] = pd.to_numeric(final["Famille"], errors='coerce').fillna(0).astype(int)

                        
                        #encoding
                        le = LabelEncoder()
                        final['Article'] = le.fit_transform(final['Article'])
                        final['Client'] = le.fit_transform(final['Client'])


                        final = final.groupby(['Year', 'Month', 'Season', 'Article', 'Client', 'Prix', 'Famille'], as_index=False).agg(
                        Quantité=('Quantité', 'sum'))
                        cols = final.columns.tolist()
                        final = final[cols]

                        final = final[final['Year'] >= 2023]

                        final.sort_values('Year', inplace=True)
                        final = final.reset_index(drop=True)

                        final["Year"] = int(number)

                        final2 = final[["Year", "Month", "Season", "Article", "Client", "Prix", "Famille"]]
                    
                        # Prediction
                        # Load the model
                        loaded_model = xgb.XGBRegressor()
                        loaded_model.load_model("./Model/xgboost_model.json")
                        predicted_quantities = loaded_model.predict(final2)
                        final["Prediction_Quantité"] = predicted_quantities
                        final["Prediction_Quantité"] = final["Prediction_Quantité"].astype(int)

                        
                        # Decode "Famille"
                        inverse_famille_mapping = {v: k for k, v in famille_mapping.items()}
                        final['Famille'] = final['Famille'].map(inverse_famille_mapping)


                        clients = pd.read_csv("./Data/client_names.csv")
                        final = pd.merge(final, clients[['Client', 'Raison Sociale']], on='Client', how='left')

                        articles = pd.read_csv("./Data/Article_name.csv")
                        articles = articles.groupby('Article').first().reset_index()
                        final = pd.merge(final, articles[['Article', 'Libellé']], on='Article', how='left')
                        

                        final["Prix_total"] = final["Prediction_Quantité"] * final["Prix"]
            
                        final["Prix_total"] = final["Prix_total"].astype(float)
                        final["Prix_total"] = final["Prix_total"].map('{:.2f}'.format)
                        final["Prix_total"] = pd.to_numeric(final["Prix_total"], errors='coerce')

                        final["Prediction_Quantité"] = pd.to_numeric(final["Prediction_Quantité"], errors='coerce')

                        print(final.info())

                        final = final[["Year", "Month", "Libellé", "Prix", "Prix_total", "Prediction_Quantité"]]  #"Raison Sociale" Famille


                        final = final.groupby(['Year', 'Month', 'Libellé']).agg({
                            'Prix_total': 'sum', 
                            'Prediction_Quantité': 'sum'}).reset_index()        

                        final["Prix_total"] = final["Prix_total"].astype(float)
                        final["Prix_total"] = final["Prix_total"].map('{:.2f}'.format)

                        return final
                
                message = None
                col1,col2,col3=st.columns(3)
                with col3:
                    st.write(f'<style>div.row-widget.stButton > button:first-child {{background-color: green}}</style>', unsafe_allow_html=True)
                    if st.button('PREDICTION'):
                        message = False
                        try:
                            if df2 is not None:
                                good_data = clean_data(df2)
                            
                                for col in good_data.columns:
                                    good_data[col] = good_data[col].astype(str)
                                
                                message = True
                        except Exception:
                            message = False


                st.markdown(" ")
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if message == True:
                        st.markdown(" ")
                        st.success("Your data has been processed and predicted successfully ✅✅")
                    elif message == False:
                        st.error("There are errors in your document. Please check it ! 🚨🚨")

                if good_data is not None:
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        st.markdown(" ")
                        st.dataframe(good_data)


        #parti DASHBOARD BI
        if (selected == "DASHBOARD BI"):
            # Embed Power BI report
            iframe_code = '<iframe title="Report Section" width="90%" height="800" src="https://app.powerbi.com/view?r=eyJrIjoiMGJmMDVjODEtZDI1Yy00YWM4LWEwNmYtMTY0ODc4MWEzMDFiIiwidCI6ImRiZDY2NjRkLTRlYjktNDZlYi05OWQ4LTVjNDNiYTE1M2M2MSIsImMiOjl9" frameborder="0" allowFullScreen="true"></iframe>'
            st.write(iframe_code, unsafe_allow_html=True)

    else:
        st.error("Error Your username or password is incorrect!! 🚨🚨")