import pandas as pd
import matplotlib.pyplot as plt

# Escolher uma base de dados da sua preferência, através de sites como Kaggle, UCI, etc.

print(
    'Skyrim_Weapons.csv from https://www.kaggle.com/datasets/elmartini/skyrim-weapons-dataset'
)
df_weapons = pd.read_csv('Skyrim_Weapons.csv')
'''
Informação das colunas

Name: nome da arma
Damage: dano base causado pela arma
Weight: peso da arma
Gold: preço base da arma
Upgrade: material necessário para melhoria da arma
Perk: vantagem de ferraria necessária para melhoria da arma
Type: tipo da arma
Category: categoria da arma
Speed: velocidade da arma (apenas para armas do tipo arco)
'''

# Cada um dos requisitos abaixo deve vir acompanhado de uma pergunta. Por exemplo, "quantos meninos que tiraram nota acima de 5 existem na turma?"

# Utilizar as seguintes funções pelo menos uma vez:
# fillna, drop ou dropna;
# apply;
# rename;

# Renomeia col. Upgrade -> Upgrade material, Perk -> Smithing perk, Gold -> Value
col_dic = {
    'Upgrade': 'Upgrade material',
    'Perk': 'Smithing perk',
    'Gold': 'Value'
}
df_weapons = df_weapons.rename(columns=col_dic)

# Preenche NaN com N/A nas col. Upgrade material, Speed e com None na col. Smithing perk
df_weapons.fillna(
    {
        'Upgrade material': 'N/A',
        'Speed': 'N/A',
        'Smithing perk': 'None'
    },
    inplace=True)

# Substitui - por N/A na col. Smithing perk
df_weapons['Smithing perk'].apply(lambda x: x.replace('-', 'N/A'))

#
# Realizar duas manipulações aritméticas necessárias na base de dados (soma, multiplicação, divisão, etc.);

print(
    '\nQual a proporção das espadas, em relação ao dano, na categoria One-Handed?'
)

total_damage = df_weapons.loc[df_weapons["Category"] == 'One-Handed',
                              "Damage"].sum()
swords_damage = df_weapons.loc[df_weapons["Type"] == 'Sword', "Damage"].sum()

print(f'{swords_damage / total_damage * 100 :.2f}%')

#
# Criar duas novas colunas, que venham a partir de alguma estatística (mean, median, max, etc.);

print('\nQuais os desvios da média em relação a valor e peso?')

# Coluna de desvios em relação ao valor médio das armas
value_mean = df_weapons["Value"].mean()
df_weapons['Value deviation'] = (df_weapons['Value'] -
                                 value_mean).apply(lambda x: round(x, 2))

# Coluna de desvios em relação ao peso médio das armas
weight_mean = df_weapons["Weight"].mean()
df_weapons['Weight deviation'] = (df_weapons['Weight'] -
                                  weight_mean).apply(lambda x: round(x, 2))

print(df_weapons.head())

#
# Filtrar dados que sejam relevantes (filtros, query ou where);

print('\nQual espada possui maior dano?')

swords = df_weapons.query("Type == 'Sword'")
maximo = swords['Damage'].max()
print(swords.query("Damage == @maximo"))

#
# Utilizar o groupby, gerando alguma constatação estatística interessante;

print('\nQuais são os danos mínimo, máximo e médio por categoria?')

d = {'Damage': ['min', 'max', 'mean']}
print(df_weapons.groupby('Category').agg(d))

#
# Exportar um dataframe para um CSV, desde que não seja igual ao original;

print('\nQuais armas possuem maior dano por tipo?')
df_weapons.drop(['Value deviation', 'Weight deviation'], axis=1, inplace=True)

best_weapons = []
for tipo in set(df_weapons['Type']):
  df_tipo = df_weapons.query("Type == @tipo")
  best_weapons.append(df_tipo[df_tipo['Damage'] == df_tipo['Damage'].max()])

df_best_weapons = pd.concat(best_weapons, ignore_index=True)
df_best_weapons.to_csv("Skyrim_Best_Weapons.csv")

print(df_best_weapons.head())

## EXTRA (200XP):

#
# Utilizar o pd.qcut ou o pd.cut.

print('\nClassificar os danos em níveis (baixo, médio, alto)')

df_weapons['Damage level'] = pd.qcut(df_weapons['Damage'],
                                     3,
                                     labels=['Low', 'Medium', 'High'])
print(df_weapons.head())

#
# Gerar um gráfico a partir de qualquer dataframe utilizado no programa (matplotlib);

print('\nQual a distribuição dos materiais de melhoria?')

weapons_types = df_weapons.groupby('Upgrade material').count()['Name']
weapons_types = weapons_types.drop(['N/A', 'None required'])

plt.barh(weapons_types.index, weapons_types.values, color='violet')
plt.title('Materiais necessários para melhoria de armas')
plt.ylabel('Material')
plt.xlabel('Número de armas')

plt.show(block=False)
