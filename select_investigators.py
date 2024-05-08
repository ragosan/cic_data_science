import sqlite3
import matplotlib.pyplot as plt
import math

def convert_to_range(s):
    if s.startswith('>'):
        return float('500000')
    else:
        low, high = map(int, s.replace(',', '').split('-'))
        return (low + high) / 2

con = sqlite3.connect("cic.db")

cur = con.cursor()

resSalaries = cur.execute("SELECT yearly_salary FROM investigators \
                  WHERE yearly_salary IS NOT null \
                  ORDER BY yearly_salary")

salaries = resSalaries.fetchall()

resStudies = cur.execute("SELECT highest_education_level FROM investigators \
                  WHERE yearly_salary IS NOT null \
                  ORDER BY highest_education_level")

education = resStudies.fetchall()

con.close()

sum = 0
salaryCounter = dict()
salaryElements = []

educationCounter = dict()
educationElements = []
educationSum = 0

for i in salaries:
    if i[0] not in salaryElements:
        salaryElements.append(i[0])
        salaryCounter[i[0]] = 1
    else:
        salaryCounter[i[0]] +=  1

for i in education:
    if i[0] not in educationElements:
        educationElements.append(i[0])
        educationCounter[i[0]] = 1
    else:
        educationCounter[i[0]] = educationCounter[i[0]] + 1
    educationSum += educationElements.index(i[0])

educationMean = educationSum/len(education)

print("Yearly Salary Objects: ", salaryElements)
print("Highest Education Level Objects: ", educationElements)
print("Average of education: ", educationElements[math.floor(educationMean)])

salarySorted = {key: salaryCounter[key] for key in sorted(salaryCounter.keys(), key=convert_to_range)}

fig, (ax1, ax2) = plt.subplots(2)

ax1.bar(range(len(salarySorted)), list(salarySorted.values()), align='center')
ax1.set_xticks(range(len(salarySorted)))
ax1.set_xticklabels(list(salarySorted.keys()), rotation=45)
ax1.set_title('Salary Distribution')

ax2.bar(range(len(educationCounter)), list(educationCounter.values()), align='center')
ax2.set_xticks(range(len(educationCounter)))
ax2.set_xticklabels(list(educationCounter.keys()))
ax2.set_title('Education Distribution')

plt.tight_layout()
plt.show()