with open('./problematic_df.txt', encoding='UTF8') as f:
    data = f.read()
    # get the length of the data
    number_of_characters = len(data)
    print('Number of characters in text file :', number_of_characters)