import requests
import sqlite3

with open("census_api_key.txt") as fh:
    api_key = fh.read().strip()

# Base url of decennial census data
dec_base_url = "https://api.census.gov/data/2020/dec/pl"
# subdivisions contains all the subdivisions of Washtenaw County included in the data
subdivisions_url = f"{dec_base_url}?get=NAME&for=county%20subdivision:*&in=state:26%20county:161&key={api_key}"
subdivisions_response = requests.get(subdivisions_url)
subdivisions = subdivisions_response.json()
#print(subdivisions)
# AA city code: 03000, AA charter township code: 03020 Ypsilanti: 89140
aa = f"03000"
ypsilanti = f"89140"

def get_race_pop(city):
    """
    This function takes in the id of a city in Washtenaw City (for example "03000" stands for Ann Arbor) and returns a dictionary 
    whose keys are different races and values are the population of each race.
    """
    races = ["Total", "White", "Black or African American", "American Indian and Alaska Native", "Asian", 
         "Native Hawaiian and Other Pacific Islander", "Some Other Race", "Population of two or more races"]
    # P1_001N, ..., P1_009N represent the nine races in the races list respectively
    race_code = ["001"] + [f"00{n}" for n in range(3, 10)]
    race_pop = {}
    for i in range(len(race_code)):
        race_url = f"{dec_base_url}?get=NAME,P1_{race_code[i]}N&for=county%20subdivision:{city}&in=state:26%20county:161&key={api_key}"
        # Retrieve the population of a certain race
        race_pop[races[i]] = requests.get(race_url).json()[1][1]
    return race_pop

aa_race_pop = get_race_pop(aa)
ypsi_race_pop = get_race_pop(ypsilanti)

#print(aa_race_pop) 
#print(ypsi_race_pop)

acs_base_url = "https://api.census.gov/data/2021/acs/acs1/subject"
test = f"{acs_base_url}?get=NAME,S1901_C01_001E&for=county%20subdivision:03000&in=state:26%20county:161&key={api_key}"
#print(requests.get(test).text)

def get_income_distribution(city):
    categories = ["Less than $10,000", "$10,000 to $14,999", "$15,000 to $24,999", "$25,000 to $34,999", "$35,000 to $49,999",
                  "$50,000 to $74,999", "$75,000 to $99,999", "$100,000 to $149,999", "$150,000 to $199,999", "$200,000 or more",
                  "Median income", "Mean income"]
    category_codes = [f"00{n}" for n in range(2, 10)] + [f"0{n}" for n in range(10, 14)]
    income_distribution = {}
    for i in range(len(category_codes)):
        url = f"{acs_base_url}?get=NAME,S1901_C01_{category_codes[i]}E&for=county%20subdivision:{city}&in=state:26%20county:161&key={api_key}"
        income_distribution[categories[i]] = float(requests.get(url).json()[1][1])
    
    return income_distribution

aa_income_distribution = get_income_distribution(aa)
ypsi_income_distribution = {'Less than $10,000': 10.6, '$10,000 to $14,999': 9.0, '$15,000 to $24,999': 12.0, '$25,000 to $34,999': 13.4, 
 '$35,000 to $49,999': 14.9, '$50,000 to $74,999': 16.3, '$75,000 to $99,999': 7.9, '$100,000 to $149,999': 9.9, 
 '$150,000 to $199,999': 2.1, '$200,000 or more': 3.8, 'Median income': 40256, 'Mean income': 56621 }
print(aa_income_distribution)
# Sorry, something is wrong with the API so I had to hardcode the Ypsilanti numbers

def scale_to_100(income_distribution):
    sum = 0
    for k, v in income_distribution.items():
        if k not in ["Median income", "Mean income"]:
            sum += v
    for k, v in income_distribution.items():
        if k not in ["Median income", "Mean income"]:
            income_distribution[k] = round(100 * v / sum, 2) 

    return income_distribution

aa_income_distribution = scale_to_100(aa_income_distribution)
ypsi_income_distribution = scale_to_100(ypsi_income_distribution)

print(aa_income_distribution)

'''
yp_url = f"https://api.census.gov/data/2021/acs/acs1/subject?get=NAME,S0101_C01_001E&for=county%20subdivision:*&in=state:26&in=county:*&key={api_key}"
print(requests.get(yp_url).text)
'''

def get_median_income_by_race(city):
    """
    Return the median household income by races
    """
    races = ["Total", "White", "Black or African American", "American Indian and Alaska Native", "Asian", 
         "Native Hawaiian and Other Pacific Islander", "Some Other Race", "Population of two or more races"]
    race_code = [f"00{n}" for n in range(1, 9)]
    median_income = {}
    for i in range(len(race_code)):
        url = f"{acs_base_url}?get=NAME,S1903_C03_{race_code[i]}E&for=county%20subdivision:{city}&in=state:26%20county:161&key={api_key}"
        median_income[races[i]] = int(requests.get(url).json()[1][1])
        for k, v in median_income.items():
            if v > 1000000 or v < -1000000:
                # replace the empty values with 0
                median_income[k] = 0
    return median_income

aa_median_income = get_median_income_by_race(aa)
ypsi_median_income = {'Total': 40256, 'White': 46379, 'Black or African American': 27742, 
 'American Indian and Alaska Native': 0, 'Asian': 47083, 'Native Hawaiian and Other Pacific Islander': 0, 'Some Other Race': 36417, 
 'Population of two or more races': 32083}
#print(get_median_income_by_race(ypsilanti))
print(aa_median_income)

yelp_base_url = "https://api.yelp.com/v3/businesses/search"
aa = "?location=Ann%20Arbor&sort_by=best_match&limit=50"
headers = {
    "accept": "application/json",
    "Authorization": "Bearer YbKDICu5zESDf_dYVUgv_Gbf_-DeFCzzaEFckfUuLqNlSrS6Jg19-hn8IYK9SxEANnfNrGVedoleHeb5xuxJo0eH-lKLGUkpVYDrajJ0GypF-K5zi5QtqtJ06bw8ZHYx"
}

def get_100_restaurants(location):
    """
    location should be the name of the city, for example: Ann Arbor ("Ann%20Arbor") or ("Ypsilanti")
    """
    rests = {}
    # get the 1-100th search results
    for offset in [0, 50]:
        
        url = f"{yelp_base_url}?location={location}&sort_by=best_match&limit=50&offset={offset}"
        response = requests.get(url, headers=headers)
        rest_data = response.json()["businesses"]
        for rest in rest_data:
            details = {}
            details["price"] = rest.get("price", "NA")
            details["categories"] = [c["alias"] for c in rest["categories"]]
            name = rest["name"]
            rests[name] = details

    # add 1 more restaurant to get to 100 if there is 1 overlapping data point in the first 100 search results
    if len(rests) == 99:
        url = f"{yelp_base_url}?location={location}&sort_by=best_match&limit=1&offset=101"
        response = requests.get(url, headers=headers)
        rest_data = response.json()["businesses"]
        for rest in rest_data:
            details = {}
            details["price"] = rest.get("price", "NA")
            details["categories"] = [c["alias"] for c in rest["categories"]]
            name = rest["name"]
            rests[name] = details

    return rests

#print((get_100_restaurants("Ann%20Arbor")))
#print(len(get_100_restaurants("Ypsilanti")))


# Define the schema for the database
schema = '''
    CREATE TABLE IF NOT EXISTS Cities (
        City_ID INTEGER PRIMARY KEY,
        City_Name TEXT,
        Population INTEGER,
        Median_Income INTEGER,
        Mean_Income INTEGER
    );

    CREATE TABLE IF NOT EXISTS Race (
        Race_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        City_ID INTEGER NOT NULL,
        Race TEXT NOT NULL,
        Population INTEGER NOT NULL,
        Median_Income INTEGER,
        FOREIGN KEY (City_ID) REFERENCES Cities (City_ID)
    );

    CREATE TABLE IF NOT EXISTS Income (
        Income_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        City_ID INTEGER NOT NULL,
        Household_Income_Range TEXT NOT NULL,
        Percentage FLOAT NOT NULL,
        FOREIGN KEY (City_ID) REFERENCES Cities (City_ID)
    );
'''

# Connect to the database
conn = sqlite3.connect('restaurant_data.db')

# Create a cursor object
cur = conn.cursor()

# Create the tables if they don't already exist
cur.executescript(schema)
# Insert data into the Cities table first
cur.execute("INSERT OR IGNORE INTO Cities (City_ID, City_Name, Population, Mean_Income, Median_Income) VALUES (1, 'Ann Arbor', ?, ?, ?)",
            (aa_race_pop["Total"], aa_income_distribution['Mean income'], aa_income_distribution["Median income"]))
cur.execute("INSERT OR IGNORE INTO Cities (City_ID, City_Name, Population, Mean_Income, Median_Income) VALUES (2, 'Ypsilanti', ?, ?, ?)",
            (ypsi_race_pop["Total"], ypsi_income_distribution["Mean income"], ypsi_income_distribution["Median income"]))

# Create the Restaurants table if it doesn't already exist
cur.execute('''
    CREATE TABLE IF NOT EXISTS Restaurants (
        Restaurant_ID INTEGER PRIMARY KEY,
        Restaurant_Name TEXT,
        Category TEXT,
        Price_Level TEXT,
        City_ID INTEGER,
        FOREIGN KEY (City_ID) REFERENCES Cities(City_ID)
    )
''')

# Define a function to insert a batch of rows
def insert_batch(data):
    for row in data:
        cur.execute("INSERT INTO Restaurants (Restaurant_Name, Category, Price_Level, City_ID) VALUES (?, ?, ?, ?)",
                     (row["name"], ", ".join(row["categories"]), row["price"], row["city_id"]))
    conn.execute("COMMIT")

# Load the restaurant data
restaurant_data = {
    "Ann Arbor": get_100_restaurants("Ann%20Arbor"),
    "Ypsilanti": get_100_restaurants("Ypsilanti")
}

#print(restaurant_data)

# Insert the data in batches of 25
batch_size = 25
for city, restaurants in restaurant_data.items():
    city_id = cur.execute("SELECT City_ID FROM Cities WHERE City_Name = ?", (city,)).fetchone()[0]
    rows = [{"name": name, "categories": info["categories"], "price": info["price"], "city_id": city_id} for name, info in restaurants.items()]
    for i in range(0, len(rows), batch_size):
        insert_batch(rows[i:i+batch_size])

# Define the data
race_data = {
    "Ann Arbor": aa_race_pop,
    "Ypsilanti": ypsi_race_pop
}

income_data = {
    "Ann Arbor": aa_median_income,
    "Ypsilanti": ypsi_median_income
}

income_distribution = {
    "Ann Arbor": aa_income_distribution,
    "Ypsilanti": ypsi_income_distribution
}

print(race_data)
print(income_data)

for city, data in race_data.items():
    city_id = cur.execute("SELECT City_ID FROM Cities WHERE City_Name = ?", (city,)).fetchone()[0]
    for race, population in data.items():
        if race != "Total":
            median_income = income_data[city][race]
            cur.execute("INSERT OR IGNORE INTO Race (City_ID, Race, Population, Median_Income) VALUES (?, ?, ?, ?)", (city_id, race, int(population), int(median_income)))

# Insert the income data into the Income table
for city, data in income_distribution.items():
    city_id = cur.execute('SELECT City_ID FROM Cities WHERE City_Name = ?', (city,)).fetchone()[0]
    for income_range, value in data.items():
        if income_range not in ("Total", "Median income", "Mean income"):
            cur.execute("INSERT OR IGNORE INTO Income (City_ID, Household_Income_Range, Percentage) VALUES (?, ?, ?)", (city_id, income_range, value))
        

# Commit the changes and close the connection
conn.commit()
conn.close()