import pandas as pd
import matplotlib.pyplot as plt

##import seaborn as sns

##import_file_path = filedialog.askopenfilename()
##df = pd.read_excel (import_file_path)
##print (df)
plt.style.use('seaborn')
file= pd.ExcelFile("test.xlsx")
df=file.parse(0)

charge=df['batterie']
print(charge[0])

##df1= pd.DataFrame(df, columns= ['charge'])
##print (df1)

fig1, ax1 = plt.subplots()

##df.head(10).plot(kind='line',x='temps',y='Charge')
##df.head(10).plot(kind='kde',x='temps',y='Charge')

##df.head(10)['charge'].plot(kind='kde')
##print (df)

##sns.kdeplot(charge,shade=True)

ax1.plot(charge,label='charge')
ax1.legend()

##plt.xlim(0, 10)
##plt.ylim(0, 100)

ax1.set_title('courbe de charge')
ax1.set_xlabel('temps')
ax1.set_ylabel('charge')

plt.tight_layout()

plt.show()
fig1.savefig('fig1.png')
