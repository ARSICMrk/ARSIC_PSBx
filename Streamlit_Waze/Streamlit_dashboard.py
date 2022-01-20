"""
Presentation of my drive activity dasbboard with streamlit
"""

#Import packages
from typing import Counter
import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pydeck as pdk
from nltk.corpus import stopwords
from wordcloud import WordCloud,STOPWORDS
from wordcloud import WordCloud
from wordcloud import STOPWORDS

#Organize app pages
st.set_page_config(
    page_title="My Waze Streamlit Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",)

st.title("Welcome to my Streamlit Waze Dashboard !")

st.write(""" 
If you want to extract an archive of all your personal data colleced by Waze, you can now be requested and downloaded from the Dashboard.\n
Login to your dashboard https://www.waze.com/dashboard, click "Download your data archive" and follow the instructions.\n
The archive contains the following data in 3 csv files : \n
* Account details
* Reports sent from the app (hazards, traffic jams, etc.)
* Summary list of drives (from, to, date)
* Favorites
* Location history (drives with GPS coordinates :!: )
* Login history
* Search history
* Dashboard summary (miles/kms driven, points, edit count, etc.)
* Last 500 edits""")

#Download my csv files into a df
drives = pd.read_csv("drives.csv", sep=';')
logins = pd.read_csv("logins.csv", sep=',')
locations = pd.read_csv("locations.csv", sep=';')
waze_full = pd.read_csv("waze_full_unique.csv", sep=';')

#My sidebars : parameters
st.sidebar.markdown('<p class="header-style">AUTHOR : Marko ARSIC</p>',
                     unsafe_allow_html=True
                     )

#Create pages from 0 to 3
selected_pages = st.sidebar.selectbox("Select my Waze activity dashboard",
                                       ["Data Overwiew",
                                        "Metrics",
                                        "Trips"]
                                       )

#Select box in streamlit
st.title("Let's take a look on the raw downloaded files")

selectbox = st.selectbox(
    "Select the dataframe you want to see",
    ["-",
     "Drives dataframe",
     "Logins dataframe",
     "Locations dataframe",
     "Final dataframe"
     ]
)
st.write(f"You selected {selectbox}")
#The first argument to st.selectbox is the string to display and the second argument is a list of options to select. 
#And then we display the selected value in the app using st.write method.

###Page 0 : owerview
if selectbox == "Drives dataframe":
        #0 - My welcome page : explaination about my dashboard
        st.header("MY LAST DRIVES")
        st.write("This dashboard shows my last daily trips from source to destination \r I extract from columns Source and Destination the latitude and longitude of geographic points")
        st.table(drives)

if selectbox == "Logins dataframe":
        #0 - My welcome page : explaination about my dashboard
        st.header("MY LAST LOGIN TIMES")
        st.write("This dashboard shows some my use of the application with le login times")
        st.write(logins)

if selectbox == "Locations dataframe":
        #0 - My welcome page : explaination about my dashboard
        st.header("MY LAST LOCATION MOVEMENTS")
        st.write("This dashboard shows all my geographical movements")
        st.write(locations)

if selectbox == "Final dataframe":
        #0 - My welcome page : explaination about my dashboard
        st.header("FINAL DATAFRAME")
        st.write("The dashboard below shows the final file after processing that I use to construct my visualisations ")
        st.write(waze_full)

###Page 1 : Metrics
if selected_pages == "Metrics":
        #0 - General metrics
        st.header("Snapshot of my Waze usage")
        drivenkm, reports, munched, duree = st.columns(4)
        drivenkm.metric("Driven kilometers", "28188.012 Km", "156 Km")
        reports.metric("Reports", "7")
        munched.metric("Munched meters", "84680 m", "-2356 m")
        duree.metric(label="AVG Login Time",value = str("{:,.2f}".format(waze_full["duree_min"].mean()))+" min")

        st.title("Chart about my activity")

        col_chart, col_cloud = st.columns(2)
        with col_chart:
            st.header("Login activity")
            fig = plt.figure(figsize=(12, 10))
            ax = fig.add_axes([0,0,1,1])
            langs = list(waze_full['date'])
            students = list(waze_full['Total_distance'])
            ax.bar(langs,students)
            st.pyplot(fig)

# Cloud chart
        with col_cloud:
            st.header("Most popular words")
            destination = []
            for i in range(len(waze_full)):
                destination.append(waze_full.loc[i,"Destination_propre"])

            all_tokens1 = []
            for line in destination:
                for mot in line.split():
                    all_tokens1.append(mot)
            
            total_term_frequency = Counter(all_tokens1)

            tfdict = {}
            for w, f in total_term_frequency.most_common():
        
                relative_tf = f / sum(list(total_term_frequency.values())) # nobre relative
                tfdict[w]  = relative_tf

            wordcloud = WordCloud(
                                stopwords=STOPWORDS,
                                background_color='black',
                                mode = 'RGB',
                                max_words=100,
                                width=1000,
                                height=1000
                                ).generate_from_frequencies(tfdict) #utilisez un dictionaire de mot nétoyer en fréquence relative
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            st.set_option('deprecation.showPyplotGlobalUse', False)
            st.pyplot()


###Page 2 : Maps
if selected_pages == "Trips":
        #0 - General metrics
        st.header("My favorites places")

        waze = pd.read_csv("drives.csv",sep=";")
        waze = waze.dropna(subset=["s_lat"])
        waze = waze.dropna(subset=["s_long"])
        waze = waze.dropna(subset=["d_lat"])
        waze = waze.dropna(subset=["d_long"])

        HEXAGON_LAYER_DATA = waze

        # Define a layer to display on a map
        layer = pdk.Layer(
            "HexagonLayer",
            HEXAGON_LAYER_DATA,
            get_position=["s_lat", "s_long"],
            auto_highlight=True,
            elevation_scale=50,
            pickable=True,
            elevation_range=[0, 100],
            extruded=True,
            coverage=1,
        )

        # Set the viewport location
        view_state = pdk.ViewState(
            longitude=2.3522219, latitude=48.856614, zoom=10, min_zoom=5, max_zoom=15, pitch=40.5, bearing=-27.36,
        )

        # Render
        r = pdk.Deck(layers=[layer], initial_view_state=view_state)
        st.write(r)

        st.header("Plot of my recent travels")

        df = waze

        GREEN_RGB = [0, 255, 0, 40]
        RED_RGB = [240, 100, 0, 40]

        # Specify a deck.gl ArcLayer
        arc_layer = pdk.Layer(
            "ArcLayer",
            data=df,
            get_width="S000 * 2",
            get_source_position=["s_lat", "s_long"],
            get_target_position=["d_lat", "d_long"],
            get_tilt=15,
            get_source_color=RED_RGB,
            get_target_color=GREEN_RGB,
            pickable=True,
            auto_highlight=True,
        )

        view_state = pdk.ViewState(latitude=48.856614, longitude=2.3522219, bearing=45, pitch=50, zoom=13,)

        TOOLTIP_TEXT = {"html": "{S000} jobs <br /> destination in red; source in green"}
        graph2 = pdk.Deck(arc_layer, initial_view_state=view_state, tooltip=TOOLTIP_TEXT)
        st.write(graph2)

