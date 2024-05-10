import sqlite3
import matplotlib.pyplot as plt
import math
from collections import OrderedDict

def convert_to_range(s):
    if s.startswith('>'):
        return float('500000')
    else:
        low, high = map(int, s.replace(',', '').split('-'))
        return (low + high) / 2

con = sqlite3.connect("cic.db")

cur = con.cursor()

# Query to select yearly_salary without null values
resSalaries = cur.execute("SELECT yearly_salary, COUNT(yearly_salary) FROM investigators \
                  WHERE yearly_salary IS NOT null \
                  AND highest_education_level IS NOT null\
                  AND current_country != 'Other'\
                  GROUP BY yearly_salary \
                  ORDER BY yearly_salary")

salaries = resSalaries.fetchall()

# Query to select highest_education_level without null values
resStudies = cur.execute("SELECT highest_education_level, COUNT(highest_education_level) FROM investigators \
                  WHERE yearly_salary IS NOT null \
                  AND highest_education_level IS NOT null\
                  AND current_country != 'Other'\
                  GROUP BY highest_education_level\
                  ORDER BY highest_education_level")

education = resStudies.fetchall()

# Query to select gender without null values
resGender = cur.execute("SELECT gender, COUNT(gender) FROM investigators \
                  WHERE yearly_salary IS NOT null \
                  AND highest_education_level IS NOT null\
                  AND current_country != 'Other'\
                  GROUP BY gender \
                  ORDER BY gender")

genders = resGender.fetchall()

# Query to select current_country without null values
resCountry = cur.execute("SELECT current_country, COUNT(current_country) FROM investigators \
                  WHERE yearly_salary IS NOT null \
                  AND highest_education_level IS NOT null\
                  AND current_country != 'Other'\
                  GROUP BY current_country \
                  ORDER BY current_country")

countries = resCountry.fetchall()

con.close()

print("Genders: ", genders)

countryCounter = dict()
gendersCounter = dict()
salaryCounter = dict()
educationCounter = dict()

salaryElements = []
educationElements = []
educationSum = 0
desiredEducationOrder = ['I prefer not to answer', 'No formal education past high school', 'Some college/university study without earning a Bachelors degree', 'Professional degree', 'Bachelors degree', 'Masters degree', 'Doctoral degree']
graphEducationOrder = ['I prefer not to answer', 'No formal education past high school', 'Some college study without a degree', 'Professional degree', 'Bachelors degree', 'Masters degree', 'Doctoral degree']

for i in countries:
    countryCounter[i[0]] = i[1]

for i in genders:
    gendersCounter[i[0]] = i[1]

for i in salaries:
    salaryCounter[i[0]] =  i[1]

for i in education:
    educationCounter[i[0]] = i[1]
    educationSum += desiredEducationOrder.index(i[0])

orderedEducationLevel = OrderedDict((key, educationCounter[key]) for key in desiredEducationOrder)

salaryAvg = 0
educationAvg = educationSum / len(education)
salarySorted = {key: salaryCounter[key] for key in sorted(salaryCounter.keys(), key=convert_to_range)}
singleSalaryValue = list(map(convert_to_range, salaryCounter.keys()))
salarySum = 0
j = 0

for i in salaryCounter:
    salarySum += salaryCounter[i] * singleSalaryValue[j]
    j += 1

salaryAvg = salarySum / len(salaries)

print("Genders Counter: ", gendersCounter)
print("Yearly Salary Objects: ", salaryElements)
print("Highest Education Level Objects: ", educationElements)
print("Map of salary avg: ", list(map(convert_to_range, salaryCounter.keys())))
print("Average of yearly salary value: ", salaryAvg)
# print("Average of yearly salary: ", min(salarySorted.keys(), key=salaryAvg))
print("Average of education value: ", educationAvg)
print("Average of education: ", desiredEducationOrder[math.floor(educationAvg)])

fig, axs = plt.subplots(2,2)

axs[0,0].bar(range(len(salarySorted)), list(salarySorted.values()), align='center')
axs[0,0].set_xticks(range(len(salarySorted)))
axs[0,0].set_xticklabels(list(salarySorted.keys()), rotation=45)
axs[0,0].set_title('Salary Distribution')

axs[0,1].bar(range(len(orderedEducationLevel)), list(orderedEducationLevel.values()), align='center')
axs[0,1].set_xticks(range(len(orderedEducationLevel)))
axs[0,1].set_xticklabels(graphEducationOrder, rotation=45)
axs[0,1].set_title('Education Distribution')

axs[1,0].bar(range(len(gendersCounter)), list(gendersCounter.values()), align='center')
axs[1,0].set_xticks(range(len(gendersCounter)))
axs[1,0].set_xticklabels(list(gendersCounter.keys()), rotation=45)
axs[1,0].set_title('Gender Distribution')

axs[1,1].bar(range(len(countryCounter)), list(countryCounter.values()), align='center')
axs[1,1].set_xticks(range(len(countryCounter)))
axs[1,1].set_xticklabels(list(countryCounter.keys()), rotation=45)
axs[1,1].set_title('Current Country Distribution')

plt.tight_layout()
plt.show()