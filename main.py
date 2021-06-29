""""
Name: Megan Winslow
CS230: SN2F
Data: Skyscrapers around the World
URL :

Description:
This program creates a webpage separated into different pages to showcase each function. Included in these pages is:
a bar chart that shows how many skyscrapers were created per year, a pie chart showing percentage of materials used,
statistics on both the number of floors as well as the height in meters, a map that showcases all 100 skyscrapers,
a query that lets you pick a city and then displays the information about all the skyscrapers in the city chosen,
and the last query that lets you chose the city, year, and material and then it displays the name and where its located on the map.
The main function calls all the other functions, while splitting them into different pages and using embedded css to
add background images and change font colors
"""

$ pip install matplotlib
import csv
import statistics
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

#creates a bar chart with lets you call it with a color and charts how many skyscrapers were created per year
def bar_chart(skyscrapers, col):
    skyscrapers["COMPLETION"].astype(int).value_counts().plot(kind = 'bar', color = col)
    plt.xlabel('Years')
    plt.ylabel('Number Completed')
    plt.title('Number of Skyscrapers Completed per Year')
    return plt
#creates a pie chart with custom colors of materials used in skyscrapers
def pie_chart(skyscrapers):
    colors = ['cadetblue','paleturquoise','darkturquoise','mediumturquoise']
    skyscrapers["MATERIAL"].value_counts().plot(kind = 'pie', autopct='%1.1f%%', colors = colors)
    plt.axis('off')
    plt.title("Skyscrapers Percentage of Material Used", loc='right')
    return plt
#gives the max, min, mean, and median of floors using a dictionary
def statistic_floors(skyscrapers):
    a = pd.to_numeric(skyscrapers["FLOORS"], downcast='signed')
    statistics = {}
    statistics["max"] = a.max()
    statistics["min"] = a.min()
    statistics["mean"] = a.mean().round()
    statistics["median"]= a.median()
    return statistics
#makes the max, min, mean, and median of the height in meters
def statistics_height(skyscrapers):
    b = skyscrapers["Meters"].str.strip('m')
    a = pd.to_numeric(b)
    max = a.max()
    min = a.min()
    mean = a.mean()
    mean = mean.round()
    median = a.median()
    return max, min, mean, median
def map(skyscrapers, z = 1):
    cordinate_tuple = ("lat", "lon") #made a tuple to chnage lat and lon
    cordinates = skyscrapers[["Latitude", "Longitude"]]
    #rename to lat and lon because have to map that way
    cordinates = cordinates.rename(columns = {'Latitude':cordinate_tuple[0], 'Longitude':cordinate_tuple[1]})
    cordinates = cordinates.apply(pd.to_numeric) #makes them an number
    st.map(cordinates, zoom=z) #maps the coordinates

def pick_city(skyscrapers):
    city_list = skyscrapers["CITY"].tolist() #makes list of vities
    city_list = list(set(city_list))
    city_list.sort() #sorts cities
    option = st.selectbox('Which city would you like?', city_list) #makes drop down to let you select city
    st.write('You selected:', option) #shows what you selected
    df_new = skyscrapers[skyscrapers['CITY'] == option] #grabs database of all skyscrapers within that city
    st.write(df_new) #prints it out

    #MOST PROUD OF
def find_skyscraper(skyscrapers):
    city_list = skyscrapers["CITY"].drop_duplicates().tolist() #changes to a list and then drop cities listed more than once
    city_list.sort() #sort them in alphabetical order
    make_choice = st.sidebar.selectbox('Select Location:', city_list) #makes drop down box with city
    years = skyscrapers["COMPLETION"].loc[skyscrapers["CITY"] == make_choice].astype(int) #gives years based off city chosen
    year_choice = st.sidebar.selectbox('Select Year:', years.drop_duplicates().tolist()) #lets you pick year
    #gives list of material based on city and year
    materials = skyscrapers["MATERIAL"].loc[skyscrapers["COMPLETION"] == year_choice].loc[skyscrapers["CITY"] == make_choice]
    #lets you pick choice of material
    material_choice = st.sidebar.selectbox('Select Material:', materials.drop_duplicates().tolist())
    #put all the pieces together to then find the name
    skyscraper = skyscrapers.loc[skyscrapers["MATERIAL"] == material_choice].loc[skyscrapers["COMPLETION"] == year_choice].loc[skyscrapers["CITY"] == make_choice]
    #puts name of skyscraper
    st.sidebar.subheader(skyscraper["NAME"].to_string(index=False))
    #maps the skyscraper chosen on the map
    map(skyscraper,12)

    #calls all the other functions as well as creates a page layout
def main():
    skyscrapers = pd.read_csv("Skyscrapers.csv")
    skyscrapers = skyscrapers.drop(labels=0, axis=0)
    page = st.sidebar.selectbox("Choose your page", ["Page 1", "Page 2", "Page 3", "Page 4", "Page 5", "Page 6", "Page 7"])
    if page == "Page 1":
        main_title = '<p style="font-family:sans-serif; color:Black; font-size: 42px;">Going to New Heights</p>'
        sub_title = '<p style="font-family:sans-serif; color:Black; font-size: 22px;">This is the Burj Khalifa - The Tallest Skyscraper in the World</p>'
        st.markdown(main_title, unsafe_allow_html=True)
        st.markdown(sub_title, unsafe_allow_html=True)
        sub2_title = '<p style="font-family:sans-serif; color:Black; font-size: 16px;">by Megan Winslow</p>'
        st.markdown(sub2_title, unsafe_allow_html=True)
        #lets me add a background image using css
        st.markdown(
        """
        <style>
        .reportview-container {
            background: url("https://websaweprd.blob.core.windows.net/cms-assets-international/styles/640w/public/2021-04/News%20article_New%20Record%20World%27s%20Highest%20Revolving%20Doors%20Burj%20Khalifa%20_main%20pic_2880%20x%201620px.jpg?itok=5Kzv7b-J");
        background-size: cover;
        }
        </style>
        """,
        unsafe_allow_html=True)
    elif page == "Page 2":
        st.title("Page 2 - Bar Chart")
        st.pyplot(bar_chart(skyscrapers, 'slateblue'), clear_figure=True)
    elif page == "Page 3":
        st.title("Page 3 - Pie Chart")
        pie = pie_chart(skyscrapers)
        st.pyplot(pie, clear_figure=True)
    elif page == "Page 4":
        st.title("Page 4 - Statistical Data")
        st.subheader("Max, Min, Mean, & Median of Floors in Skyscrapers")
        floors = statistic_floors(skyscrapers)
        st.write("Max:", floors["max"])
        st.write("Min:", floors["min"])
        st.write("Mean:", floors["mean"])
        st.write("Median:", floors["median"])
        st.subheader("Max, Min, Mean, & Median of Height of Skyscrapers in Meters")
        max, min, mean, median = statistics_height(skyscrapers)
        st.write("Max:", max)
        st.write("Min:", min)
        st.write("Mean:", mean)
        st.write("Median:", median)
        #lets me add a background image using css
        st.markdown(
        """
        <style>
        .reportview-container {
            background: url("data:image/jpeg;base64,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");
        background-size: cover;
        }
        </style>
        """,
        unsafe_allow_html=True)
    elif page == "Page 5":
        st.title("Page 5 - Map of All Skyscrapers")
        map(skyscrapers)
    elif page == "Page 6":
        st.title("Page 6 - Find Top Skyscrapers Based on Selected City")
        pick_city(skyscrapers)
        #lets me add a background image using css
        st.markdown(
        """
        <style>
        .reportview-container {
            background: url("data:image/jpeg;base64,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");
        background-size: cover;
        }
        </style>
        """,
        unsafe_allow_html=True)
    elif page == "Page 7":
        st.title("Page 7 - Find Skyscraper Based on Location, Year, & Material")
        st.subheader("Displays Choice on Map")
        find_skyscraper(skyscrapers)
main()

#https://towardsdatascience.com/creating-multipage-applications-using-streamlit-efficiently-b58a58134030 (helped creating multiple pages)
#https://discuss.streamlit.io/t/filter-dataframe-by-selections-made-in-select-box/6627/2 (helped with the find skyscraper function)
#https://docs.streamlit.io/en/stable/api.html (used reference for most questions I had)
#https://matplotlib.org/stable/gallery/color/named_colors.html (for list of colors)
#https://discuss.streamlit.io/t/change-backgroud/5653 (help me add image to background)
#https://discuss.streamlit.io/t/change-font-size-and-font-color/12377/3 (change title colors)
