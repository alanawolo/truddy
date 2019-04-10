import matplotlib
import matplotlib.pyplot as plt
import sqlite3 # for reading data from DB 


conn = sqlite3.connect("Weather.sqlite")
cur = conn.cursor()

cur.execute('SELECT * from Weather')
# create weather something list or dict idk - Dictionary to hold temps max and min.

# Get the data that needs to be plotted on x-axis

# Get the data that needs to be plotted on y-axis
yvals = [year_dict['Freshman'], year_dict['Sophomore'], year_dict['Junior'], year_dict['Senior']]

#2. plot the bar chart with xvals and yvals. Align the bars in center and assign a color to each bar.
plt.bar(xvals, yvals, align='center', color=['magenta', 'yellow', 'indigo', 'pink'])
#3.Give ylabel to the plot
plt.ylabel('Amount of Students')
#4.Give xlabel to the plot
plt.xlabel('Year')
#5.Give the title to the plot
plt.title('Amount of Students in Each Year')
#6.Save the plot as a .png file
plt.savefig('example_plot.png')
#7.Show the plot
plt.show()


##### Part 2: Make a histogram of midterm grade and Save result as .png
# 1. Use cur object to execute a SQL query to select midterm grades from students table
conn = sqlite3.connect("Restaurant.sqlite")
cur = conn.cursor()

cur.execute('SELECT * from Restaurant')
# create weather something list or dict idk - Dictionary to hold ratings and resturant names.
for x in 

# Get the data that needs to be plotted on x-axis
#xvals = [names idk]
# Get the data that needs to be plotted on y-axis
yvals = [year_dict['name'], year_dict['name'], year_dict['name'], year_dict['name']]

#2. plot the bar chart with xvals and yvals. Align the bars in center and assign a color to each bar.
plt.bar(xvals, yvals, align='center', color=['magenta', 'yellow', 'indigo', 'pink'])
#3.Give ylabel to the plot
plt.ylabel('Rating')
#4.Give xlabel to the plot
plt.xlabel('Restaurant Name')
#5.Give the title to the plot
plt.title('Ratings of Certain Restaurants')
#6.Save the plot as a .png file
#plt.savefig('')
#7.Show the plot
plt.show()


##### Part 3: Scatterplot of midterm grade vs. final grade. Save result as .png
# 1. Use the cur object to execute a SQL query to select midterm and final grades from students table
cur.execute('SELECT midterm, final from students')
# Copy the data into two different lists
midterms=[]
finals=[]
for row in cur:
	midterms.append(row[0])
	finals.append(row[1])

# 2. plot the scatter plots with midterm grades on x-axis and final grades on y-axis
plt.scatter(midterms, finals)
# 3. Give the xlabel to the plot
plt.xlabel('Midterm Grades')
# 4. Give the ylabel to the plot
plt.ylabel('Final Grades')
# 5. Give the title to the plot
plt.title('Midterm and Final Grades')
# 6. Save the plot
plt.savefig('scatter_example.png')
# Show the plot
plt.show()