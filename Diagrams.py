import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

try:
    df = pd.read_csv('writetable.csv', encoding='utf-8')
    print("Ok, файл CSV успішно завантажено.")
except FileNotFoundError:
    print("Помилка: файл CSV не знайдено.")
    exit(1)
except Exception as e:
    print(f"Помилка при завантаженні файлу CSV: {str(e)}")
    exit(1)

def calculate_age(birthdate):
    birthdate = pd.to_datetime(birthdate, format='%d.%m.%Y', errors='coerce')
    if birthdate is not pd.NaT:
        today = pd.to_datetime('today')
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        return age
    else:
        return None

df['Вік'] = df['Дата народження'].apply(calculate_age)
def plot_gender_distribution(df):
    plt.figure(figsize=(8, 6))
    sns.countplot(data=df, x='Стать', label='Стать')
    plt.title("Розподіл за статтю співробітників")
    plt.xlabel("Стать")
    plt.ylabel("Кількість")
    plt.show()

def plot_age_distribution(df):
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x='Вік', bins=20, kde=True, label='Вік')
    plt.title("Розподіл віку співробітників")
    plt.xlabel("Вік")
    plt.ylabel("Кількість")
    plt.legend(title="")
    plt.show()

def plot_gender_age_distribution(df):
    plt.figure(figsize=(12, 8))
    sns.histplot(data=df, x='Вік', hue='Стать', bins=20, kde=True, multiple='stack')
    plt.title("Розподіл співробітників за віковими категоріями\nЧоловіча (синій) та Жіноча (помаранчевий)")
    plt.xlabel("Вік")
    plt.ylabel("Кількість")
    plt.legend(title="")
    plt.show()

gender_distribution = df['Стать'].value_counts()
print("Кількість співробітників чоловічої та жіночої статі:")
print(gender_distribution)

age_bins = [0, 18, 45, 70, 100]
age_labels = ["Молодше 18", "18-45", "45-70", "Старше 70"]
df['Вікова категорія'] = pd.cut(df['Вік'], bins=age_bins, labels=age_labels, right=False)
age_distribution = df['Вікова категорія'].value_counts().sort_index()
print("\nКількість співробітників у кожній віковій категорії:")
print(age_distribution)

gender_age_distribution = df.groupby(['Вікова категорія', 'Стать'], observed=False).size().unstack().fillna(0)
print("\nКількість співробітників жіночої та чоловічої статі у кожній віковій категорії:")
print(gender_age_distribution)

plot_gender_distribution(df)
plot_age_distribution(df)
plot_gender_age_distribution(df)