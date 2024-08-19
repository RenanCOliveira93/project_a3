from dataframes import df, df_rating

dict_fillna = {
    'Title': 'Título não informado',
    'Descrição': 'Descrição não informada',
    'Autores': 'Autores não informados',
    'Imagens': 'Imagens não informadas',
    'Link': 'Link não informado',
    'Editora': 'Editora não informada',
    'Data_publicação': 'Data de publicação não informada',
    'infoLink': 'Informações do Link não informadas',
    'Categoria': 'Categoria não informada',
    'Avaliação': 0,
    'Id': 'Id não informado',
    'Preço': 0,
    'User_id': 'Id do usuário não informado',
    'Nome_perfil': 'Nome do perfil não informado',
    'Summary': 'Sumário não informado',
    'Texto': 'Texto adicional não informado'    
}

df['Title'] = df['Title'].fillna(dict_fillna['Title'])
df['description'] = df['description'].fillna(dict_fillna['Descrição'])
df['authors'] = df['authors'].fillna(dict_fillna['Autores'])
df['image'] = df['image'].fillna(dict_fillna['Imagens'])
df['previewLink'] = df['previewLink'].fillna(dict_fillna['Link'])
df['publisher'] = df['publisher'].fillna(dict_fillna['Editora'])
df['publishedDate'] = df['publishedDate'].fillna(dict_fillna['Data_publicação'])
df['infoLink'] = df['infoLink'].fillna(dict_fillna['infoLink'])
df['categories'] = df['categories'].fillna(dict_fillna['Categoria'])
df['ratingsCount'] = df['ratingsCount'].fillna(dict_fillna['Avaliação'])

df_rating['Id'] = df_rating['Id'].fillna(dict_fillna['Id'])
df_rating['Title'] = df_rating['Title'].fillna(dict_fillna['Title'])
df_rating['Price'] = df_rating['Price'].fillna(dict_fillna['Preço'])
df_rating['User_id'] = df_rating['User_id'].fillna(dict_fillna['User_id'])
df_rating['profileName'] = df_rating['profileName'].fillna(dict_fillna['Nome_perfil'])
df_rating['summary'] = df_rating['summary'].fillna(dict_fillna['Summary'])
df_rating['text'] = df_rating['text'].fillna(dict_fillna['Texto'])


df_rating1 = df_rating.query("text != 'Texto adicional não informado' ")
df_rating2 = df_rating1.query("Title != 'Título não informado' ")
df_rating3 = df_rating2.query("summary != 'Sumário não informado' ")
df_rating4 = df_rating3.query("score > 0")

df1 = df.query("Title != 'Título não informado' ")
df2 = df1.query("authors != 'Autores não informados' ")
df3 = df2.query("publisher != 'Editora não informada' ")
df4 = df3.query("categories != 'Categoria não informada' ")


