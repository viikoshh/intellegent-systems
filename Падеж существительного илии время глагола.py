import pymorphy2

"""a = input('Введите 1, если хотите просклонять существительное по падежам 
(не работает с числительными, и 0, если хотите изменить глагол по временам: \n')"""

a = 1

morph = pymorphy2.MorphAnalyzer()
word = input('Введите слово: ')
p = morph.parse(word)[0]


if a == 1:
    gender = {'masc': 'Мужской', 
            'femn': 'Женский',
            'neut':'Средний'}
    
    a = p.tag.gender
    print(f'{gender[a]} род')
    
    if 'NOUN' in p.tag.POS:
        print('Единственное число:')
        print('Именительный падеж:', p.inflect({'nomn'})[0])
        print('Родительный падеж:', p.inflect({'gent'})[0])
        print('Дательный падеж:', p.inflect({'datv'})[0])
        print('Винительный падеж:', p.inflect({'accs'})[0])
        print('Творительный падеж:', p.inflect({'ablt'})[0])
        print('Предложный падеж:', p.inflect({'loct'})[0])
        print()
        print('Множественное число:')
        print('Именительный падеж:', p.inflect({'nomn', 'plur'})[0])
        print('Родительный падеж:', p.inflect({'gent', 'plur'})[0])
        print('Дательный падеж:', p.inflect({'datv', 'plur'})[0])
        print('Винительный падеж:', p.inflect({'accs', 'plur'})[0])
        print('Творительный падеж:', p.inflect({'ablt', 'plur'})[0])
        print('Предложный падеж:', p.inflect({'loct', 'plur'})[0])
    else:
        print('Не существительное')

else:
    CASES = {
        ('past', 'Прошедшее время:'): [
            {'masc'}, {'femn'}, {'neut'}, {'plur'}
        ],
        ('pres', 'Настоящее время:'): [
            {'1per', 'sing'},
            {'1per', 'plur'},
            {'2per', 'sing'},
            {'2per', 'plur'},
            {'3per', 'sing'},
            {'3per', 'plur'}
        ]
    }
    
    if p.tag.POS in {'INFN', 'VERB'}:
        for key, val in CASES.items():
            print(key[1])
            for cases in val:
                cases.add(key[0])
                w = p.inflect(cases)[0]
                print(w)
    
    else:
        print('Не глагол')    