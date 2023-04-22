import sqlite3
import matplotlib.pyplot as plt

'''
Plotting the restaurants data
'''

connection = sqlite3.connect('restaurant_data.db')
cursor = connection.cursor()
cursor.execute("SELECT Category FROM Restaurants WHERE City_ID = 1")
rows = cursor.fetchall()
aa_categories_raw = []
ypsi_categories_raw = []
for row in rows:
    aa_categories_raw.append(row[0])

cursor.execute("SELECT Category FROM Restaurants WHERE City_ID = 2")
rows = cursor.fetchall()
for row in rows:
    ypsi_categories_raw.append(row[0])

cursor.close()
connection.close()

aa_categories = []
for item in aa_categories_raw:
    l = item.split(",")
    aa_categories.append(l[0])

# print the categories list
print(aa_categories)

ypsi_categories = []
for item in ypsi_categories_raw:
    l = item.split(",")
    ypsi_categories.append(l[0])


def draw_bar_chart(categories):
# Convert categories to lowercase and count occurrences
    category_counts = {}
    for category in categories:
        category_lower = category.lower()
        if category_lower in category_counts:
            category_counts[category_lower] += 1
        else:
            category_counts[category_lower] = 1

# Sort categories by count in descending order
    sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)

# Extract top 50 categories (actually there are less than 50 categories) and counts
    top_categories = [category[0] for category in sorted_categories[:50]]
    top_counts = [category[1] for category in sorted_categories[:50]]

    fig, ax = plt.subplots()
    ax.bar(top_categories, top_counts)
    ax.set_xlabel('Category')
    ax.set_ylabel('Count')
    ax.set_title('All Restaurant Categories')
    plt.xticks(rotation=45, ha='right')
    plt.show()

#draw_bar_chart(aa_categories)
#draw_bar_chart(ypsi_categories)

'''
Now studying price levels of restaurants 
'''

connection = sqlite3.connect('restaurant_data.db')
cursor = connection.cursor()
cursor.execute("SELECT Price_Level FROM Restaurants WHERE City_ID = 1")
rows = cursor.fetchall()
aa_price = []
ypsi_price = []
for row in rows:
    aa_price.append(row[0])
cursor.execute("SELECT Price_Level FROM Restaurants WHERE City_ID = 2")
rows = cursor.fetchall()
for row in rows:
    ypsi_price.append(row[0])
cursor.close()
connection.close()

def price_level_to_number(price_list):
    output = []
    for i in range(len(price_list)):
        if price_list[i] == "$":
            output.append(1)
        elif price_list[i] == "$$":
            output.append(2)
        elif price_list[i] == "$$$":
            output.append(3)
        elif price_list[i] == "$$$$":
            output.append(4)
    return output

print(aa_price)
print(ypsi_price)

aa_price_levels = price_level_to_number(aa_price)
ypsi_price_levels = price_level_to_number(ypsi_price)

print(aa_price_levels)
print(ypsi_price_levels)

aa_price_count = [aa_price_levels.count(level) for level in [1, 2, 3, 4]]
ypsi_price_count = [ypsi_price_levels.count(level) for level in [1, 2, 3, 4]]

print(aa_price_count)

labels = ["\$", "\$\$", "\$\$\$", "\$\$\$\$"]

# Create the pie chart
fig, ax = plt.subplots()
ax.pie(aa_price_count, labels=labels, autopct='%1.1f%%')
ax.set_title("Ann Arbor Restaurants Price Levels")
plt.show()

fig, ax = plt.subplots()
ax.pie(ypsi_price_count, labels=labels, autopct='%1.1f%%')
ax.set_title("Ypsilanti Restaurants Price Levels")
plt.show()

aa_avg_price = sum(aa_price_levels) / len(aa_price_levels)
ypsi_avg_price = sum(ypsi_price_levels) / len(ypsi_price_levels)

# Draw the bar chart of average prices
plt.bar(["Ann Arbor", "Ypsilanti"], [aa_avg_price, ypsi_avg_price])
plt.xlabel('City')
plt.ylabel('Average Price Level')
plt.title('Average Price Level in the Two Cities')
plt.show()

# Write the calculation file
with open("avg_prices.txt", "w") as fh:
    fh.write(f"AA restaurants average price level: {aa_avg_price}\n")
    fh.write(f"Ypsilanti restaurants average price level: {ypsi_avg_price}")

'''
Now plotting the income data
'''

connection = sqlite3.connect('restaurant_data.db')
cursor = connection.cursor()
cursor.execute("SELECT Household_Income_Range FROM Income WHERE City_ID = 1")
rows = cursor.fetchall()
income_ranges = []
aa_income_distribution = []
ypsi_income_distribution = []
for row in rows:
    income_ranges.append(row[0])

cursor.execute("SELECT Percentage FROM Income WHERE City_ID = 1")
rows = cursor.fetchall()
for row in rows:
    aa_income_distribution.append(row[0])

cursor.execute("SELECT Percentage FROM Income WHERE City_ID = 2")
rows = cursor.fetchall()
for row in rows:
    ypsi_income_distribution.append(row[0])

cursor.close()
connection.close()

plt.bar(income_ranges, aa_income_distribution)


plt.xlabel('Income Ranges')
plt.ylabel('Percentage')
plt.title('Income Distribution of Ann Arbor')
plt.xticks(rotation=30)

plt.show()

plt.bar(income_ranges, ypsi_income_distribution)

plt.xlabel('Income Ranges')
plt.ylabel('Percentage')
plt.title('Income Distribution of Ypsilanti')
plt.xticks(rotation=30)

plt.show()

'''
Race data
'''

connection = sqlite3.connect('restaurant_data.db')
cursor = connection.cursor()
cursor.execute("SELECT Race FROM Race WHERE City_ID = 1")
rows = cursor.fetchall()
races = []
aa_race_pop = []
ypsi_race_pop = []
aa_income_by_race = []
ypsi_income_by_race = []
for row in rows:
    races.append(row[0])

cursor.execute("SELECT Population FROM Race WHERE City_ID = 1")
rows = cursor.fetchall()
for row in rows:
    aa_race_pop.append(row[0])

cursor.execute("SELECT Population FROM Race WHERE City_ID = 2")
rows = cursor.fetchall()
for row in rows:
    ypsi_race_pop.append(row[0])

cursor.execute("SELECT Median_Income FROM Race WHERE City_ID = 1")
rows = cursor.fetchall()
for row in rows:
    aa_income_by_race.append(row[0])

cursor.execute("SELECT Median_Income FROM Race WHERE City_ID = 2")
rows = cursor.fetchall()
for row in rows:
    ypsi_income_by_race.append(row[0])

cursor.close()
connection.close()

fig, ax = plt.subplots()
ax.pie(aa_race_pop, labels=races, autopct='%1.1f%%')
ax.set_title("Race Distribution of Ann Arbor")
plt.show()

fig, ax = plt.subplots()
ax.pie(ypsi_race_pop, labels=races, autopct='%1.1f%%')
ax.set_title("Race Distribution of Ypsilanti")
plt.show()

plt.bar(races, aa_income_by_race)

plt.xlabel('Races')
plt.ylabel('Median Income')
plt.title('Median Income by Race in Ann Arbor')
plt.xticks(rotation=10)
plt.show()

plt.bar(races, ypsi_income_by_race)
plt.xlabel('Races')
plt.ylabel('Median Income')
plt.title('Median Income by Race in Ypsilanti')
plt.xticks(rotation=10)
plt.show()