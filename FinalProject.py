"""
Class:\tCS230 — Section HB1S
Name:\tYiming Zhang
\tI pledge that I have completed the programming assignment independently.
\tI have not copied the code from a student or any other source.
\tI have not given my code to any student.
"""
import statistics
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
print(__doc__)

print("Final Project: Craigslist Used Car Data Presentation Using Streamlit")

# This section's codes are mostly about reading data and clearing/sorting data
GEOFILE = 'USZIPCodes202108.csv'
dfGeoInfo = pd.read_csv(GEOFILE)
FILE = "cl_used_cars_7000_sample.csv"
dfAllUsedCar = pd.read_csv(FILE)
carInfo = [dfAllUsedCar['manufacturer'], dfAllUsedCar['model'], dfAllUsedCar['odometer'], dfAllUsedCar['year'], dfAllUsedCar['price'], dfAllUsedCar['lat'], dfAllUsedCar['long'], dfAllUsedCar['url']]
headers = ['manufacturer', 'model', 'odometer', 'year', 'price', 'lat', 'long', 'url']
dfUsedCarQ1 = pd.concat(carInfo, axis=1, keys=headers)
dfUsedCarQ1 = dfUsedCarQ1.dropna()
dfUsedCarQ1 = dfUsedCarQ1.sort_values(by=['manufacturer', 'model', 'year'])


# This section's codes are mostly about defining functions that will be used in the main application
def get_car_make():
    carMakes = []
    manuFacturerList = []
    carMakes.append(dfUsedCarQ1['manufacturer'].values.tolist())
    carMakesV2 = [make for makes in carMakes for make in makes]

    for n in range(len(carMakesV2)):
        if carMakesV2[n] not in manuFacturerList:
            manuFacturerList.append(carMakesV2[n])

    clientSeleMake = st.selectbox("Select a car make from the following list", manuFacturerList)
    st.text(f"the selected car make is {clientSeleMake}")
    return clientSeleMake


def get_car_model(clientSeleMake):
    carModels = []
    ModelList = []
    dfSelectedMake = dfUsedCarQ1[dfUsedCarQ1.manufacturer == clientSeleMake]
    carModels.append(dfSelectedMake['model'].values.tolist())
    carModelV2 = [model for models in carModels for model in models]

    for n in range(len(carModelV2)):
        if carModelV2[n] not in ModelList and pd.isnull(carModelV2[n]) == False:
            ModelList.append(carModelV2[n])
        ModelList = [str(x) for x in ModelList]

    clientSeleModel = st.selectbox("Select a car model from the following list", ModelList)

    st.text(f"the selected car model is {clientSeleModel}")
    return clientSeleModel


def get_car_year(clientSeleMake, clientSeleModel):
    carYears = []
    yearList = []
    dfSelectedMake = dfUsedCarQ1[dfUsedCarQ1.manufacturer == clientSeleMake]
    dfSelectedModel = dfSelectedMake[dfSelectedMake.model == clientSeleModel]
    carYears.append(dfSelectedModel['year'].values.tolist())
    carYearsV2 = [year for years in carYears for year in years]

    for nn in range(len(carYearsV2)):
        if carYearsV2[nn] not in yearList:
            yearList.append(carYearsV2[nn])

    clientSeleYear = st.selectbox("Select a production year from the following list", yearList)
    st.text(f"the selected car year is {clientSeleYear}")
    return clientSeleYear


def get_stats(clientSeleMake, clientSeleModel, clientSeleYear):
    carPrices = []
    priceList = []
    carMiles = []
    mileList = []
    dfSelectedMake = dfUsedCarQ1[dfUsedCarQ1.manufacturer == clientSeleMake]
    dfSelectedModel = dfSelectedMake[dfSelectedMake.model == clientSeleModel]
    dfSelectedYear = dfSelectedModel[dfSelectedModel.year == clientSeleYear]

    carPrices.append(dfSelectedYear['price'].values.tolist())
    carPricesV2 = [price for prices in carPrices for price in prices]

    for n in range(len(carPricesV2)):
        priceList.append(float(carPricesV2[n]))

    carMiles.append(dfSelectedYear['odometer'].values.tolist())
    carMilesV2 = [mile for miles in carMiles for mile in miles]

    for n in range(len(carMilesV2)):
        mileList.append(float(carMilesV2[n]))

    st.write(f"A typical private-seller-listed {clientSeleYear:.0f} {clientSeleMake} {clientSeleModel} on Craigslist has a median odometer of {statistics.median(mileList):.2f} miles and an average odometer of {statistics.mean(mileList):.2f} miles. The median and mean price that the sellers offer are ${statistics.median(priceList):.2f} and ${statistics.mean(priceList):.2f}, respectively.")


def show_scatter_plt(clientSeleMake, clientSeleModel, clientSeleYear):
    dfSelectedMake = dfUsedCarQ1[dfUsedCarQ1.manufacturer == clientSeleMake]
    dfSelectedModel = dfSelectedMake[dfSelectedMake.model == clientSeleModel]
    dfSelectedYear = dfSelectedModel[dfSelectedModel.year == clientSeleYear]

    st.write(f'Please use the chart below  as a reference to determine the depreciation {clientSeleYear:.0f} {clientSeleMake} {clientSeleModel} per odometer reads: ')

    fig, ax = plt.subplots()
    ax.scatter(x=dfSelectedYear['odometer'], y=dfSelectedYear['price'], color="red")
    plt.title(f"{clientSeleYear:.0f} {clientSeleMake} {clientSeleModel}, price by millage scatter plot")
    plt.xlabel('millage/odometer read', color="red")
    plt.ylabel('price', color="red")
    plt.grid(True, color='#D3D3D3', linestyle=':')
    st.pyplot(fig)


def find_price_range():
    maxPrice = int(dfUsedCarQ1['price'].max())

    def histo_plt(maxPriceHis, dfUsedCarQ1His):
        dfUsedCarQ1['price'] = pd.to_numeric(dfUsedCarQ1['price'], downcast="float")
        fig, ax = plt.subplots()
        binNum = maxPriceHis // 2500
        ax.hist(dfUsedCarQ1His['price'], binNum, color='#0ABAB5')
        plt.title(f"Histogram: Price Distribution of All Used Cars in the Dataset", color='red')
        plt.xlabel('Price', color="red")
        plt.ylabel('Frequency', color="red")
        plt.grid(True, color='#D3D3D3', linestyle=':')
        st.pyplot(fig)

    priceRange = st.slider("Choose your budget range: ", min_value=0, max_value=maxPrice, value=[0, maxPrice], step=100)

    dfMinPriceEntered = dfUsedCarQ1[dfUsedCarQ1.price >= int(priceRange[0])]
    dfMaxPriceEntered = dfMinPriceEntered[dfMinPriceEntered.price <= int(priceRange[1])]

    st.write(f"You entered a minimal price of ${priceRange[0]:.0f} and a maximal price of ${priceRange[1]:.0f} for you desired vehicle.")
    st.write(f"Across the country, {len(dfMaxPriceEntered.index)} cars in our dataset correspond to your selected price range.")

    clientCheckBox = st.checkbox("Show dynamic data for the histogram", value=False)
    if clientCheckBox == False:
        histo_plt(maxPriceHis=maxPrice, dfUsedCarQ1His=dfUsedCarQ1)
    elif clientCheckBox == True:
        histo_plt(maxPriceHis=int(dfMaxPriceEntered['price'].max()), dfUsedCarQ1His=dfMaxPriceEntered)

    return dfMaxPriceEntered


def find_geo_data(dfMaxPriceEntered):
    userInputZipfloat = st.number_input('Enter your local zip code: ', format="%i")
    userInputZipInt = int(userInputZipfloat)
    try:
        if userInputZipInt in dfGeoInfo.ZipCode:
            dfClientInputZip = dfGeoInfo[dfGeoInfo.ZipCode == userInputZipInt]
            clientZipLat = dfClientInputZip['ZipLatitude'].unique().tolist()
            clientZipLong = dfClientInputZip['ZipLongitude'].unique().tolist()
            st.write(f"The zip code you entered has a latitude of {clientZipLat[0]:.4f} and a longitude of {clientZipLong[0]:.4f}")
    except IndexError:
        st.write('Please enter a valid zip code')
    userTravelRange = st.selectbox("Please select the distance (in miles) that you are willing to travel to get your car: ", [5, 10, 25, 50, 100, 250, 500, 1000, 2500, 5000])
    try:
        deltaLat = userTravelRange / 69  # https://www.usgs.gov/faqs/how-much-distance-does-a-degree-minute-and-second-cover-your-maps?qt-news_science_products=0#
        deltaLong = userTravelRange / 54.6  # https://www.usgs.gov/faqs/how-much-distance-does-a-degree-minute-and-second-cover-your-maps#:~:text=One%2Ddegree%20of%20longitude%20equals,one%20second%20equals%2080%20feet.
        dfLowerLatCalculated = dfMaxPriceEntered[dfMaxPriceEntered.lat >= (clientZipLat[0] - deltaLat)]
        dfUpperLatCalculated = dfLowerLatCalculated[dfMaxPriceEntered.lat <= (clientZipLat[0] + deltaLat)]
        dfLowerLongCalculated = dfUpperLatCalculated[dfMaxPriceEntered.long >= (clientZipLong[0] - deltaLong)]
        dfUpperLongCalculated = dfLowerLongCalculated[dfMaxPriceEntered.long <= (clientZipLong[0] + deltaLong)]
    except IndexError:
        st.write('Please enter a valid zip code')
    try:
        dfPlotInfo = pd.DataFrame(dfUpperLongCalculated, columns=["lat", "long"])
        dfPlotInfo.columns = ["lat", "lon"]
        st.map(dfPlotInfo)
        st.write(f"There are {len(dfPlotInfo.index)} used cars listed on Craigslist within your inputted price range and they locate within {userTravelRange} Miles to your local address.")
        dfShowUserInfo = pd.DataFrame(dfUpperLongCalculated, columns=['manufacturer', 'model', 'odometer', 'year', 'price'])
        dfShowUserInfoWithUrl = pd.DataFrame(dfUpperLongCalculated, columns=['manufacturer', 'model', 'odometer', 'year', 'price', 'url'])
        st.write(f"All the qualified vehicles are listed below, for more info about a specific vehicle, please expand the DataFrame below to see more details: ")
        st.write(dfShowUserInfo)
    except UnboundLocalError:
        st.write('Please enter a valid zip code')
    try:
        clientInputIndex = st.selectbox("Please select your interested index number listed in above chart ", dfShowUserInfo.index)
        dfIndexInputed = dfShowUserInfoWithUrl.loc[clientInputIndex]
        st.write(f"You have selected a vehicle with an index number of {clientInputIndex}, for more info about this vehicle, please visit: ")
        st.write(dfIndexInputed.url)
    except UnboundLocalError:
        st.write('Please enter a valid zip code')


def home_page(WELCOME_PHRASE, HEADER_TEXT):
    st.title(WELCOME_PHRASE)
    st.subheader(HEADER_TEXT)
    st.write(f"This is the final project for Bentley's summer 2021 course -CS230. In the Project, we created data-driven apps using Streamlit.io.")
    st.write(f"This App has two functions:")
    st.write(f" 1. You can input the make, model, and year info of your desirable car, and the app will show you statistics regarding the car's prices listed on Craigslist.")
    st.write(f" 2. You can input a price range, your local zip code, and a travel distance, the app will show you all the available cars that qualify your inputs, then you can select a specific one to learn more details.")
    st.write('Please select an app function using the sidebar on the left. Enjoy!')


# This section's codes are some symbolic constants that wont change.
WELCOME_PHRASE = 'Craigslist Car Data Presentation'
HEADER_TEXT = 'Welcome to this website, hope it can help you make better decisions purchasing a used vehicle.'
PAGE_HEADER = '<p style="font-family:monospace; color:black; font-size: 12px;">Your can select an app function using the sidebar on the left.</p>'
WATERMARK = '<p style="font-family:monospace; color:black; font-size: 12px;">This is the CS230 final project made by Yiming Zhang</p>'

SELECTIONS = ['visit the homepage', 'find the market price of a specific car model', 'find a used car in a given budget']


# Starting here is the main function for this application, enjoy~
functionSelect = st.sidebar.selectbox('I want to', SELECTIONS)

if functionSelect == SELECTIONS[0]:
    st.markdown(PAGE_HEADER, unsafe_allow_html=True)
    home_page(WELCOME_PHRASE, HEADER_TEXT)
    st.markdown(WATERMARK, unsafe_allow_html=True)

elif functionSelect == SELECTIONS[1]:
    st.markdown(PAGE_HEADER, unsafe_allow_html=True)
    st.write(f"Currently, the App is guiding you to {SELECTIONS[1]}.")
    clientSeleMake = get_car_make()
    clientSeleModel = get_car_model(clientSeleMake)
    clientSeleYear = get_car_year(clientSeleMake, clientSeleModel)
    get_stats(clientSeleMake, clientSeleModel, clientSeleYear)
    show_scatter_plt(clientSeleMake, clientSeleModel, clientSeleYear)
    " "
    st.markdown(WATERMARK, unsafe_allow_html=True)

elif functionSelect == SELECTIONS[2]:
    st.markdown(PAGE_HEADER, unsafe_allow_html=True)
    st.write(f"Currently, the App is guiding you to {SELECTIONS[2]}.")
    dfMaxPriceEntered = find_price_range()
    find_geo_data(dfMaxPriceEntered)
    " "
    st.markdown(WATERMARK, unsafe_allow_html=True)
