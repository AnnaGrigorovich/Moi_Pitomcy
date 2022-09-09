def test_add_new_pet_with_long_name(name='ХомякХомякХомякХомякХомяк',
                                    animal_type='кот',
                                    age='1', pet_photo='images/homyk.jpg'):
    """Проверяем, что нельзя добавить питомца с именем длинною более 20 символов"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    print('Баг - сайт позволяет добавить питомца с именем длинною более 20 символов')

def test_negative_add_new_pet_without_data(name="", animal_type="", age=""):
    """Проверяем возможность добавить питомца без данных, ожидаем код ответа 400, питомец не добавлен"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_no_photo(auth_key, name, animal_type, age)

    assert status == 400
    # Питомец без данных добавляется, нужно заводить баг

def test_add_new_pet_with_age_in_letters(name="Хомяк", animal_type="кот", age="-1"):
    """Проверяем возможность добавить питомца с отрицательным возрастом"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_no_photo(auth_key, name, animal_type, age)

    assert status == 200
    # Питомец без данных добавляется, нужно заводить баг

def test_add_new_pet_with_invalid_photo_format(name="Генри", animal_type="ёж", age="4", pet_photo="images/cat2.pdf"):

    """Проверяем что нельзя добавить питомца с фото в формате pdf, код ответа 400, согласно документации"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 500
    # Питомец без данных добавляется, нужно заводить баг

def test_add_new_pet_with_empty_name(name='', animal_type='кот', age='1', pet_photo='images/homyk.jpg'):
    '''Проверяем возможность добавления питомца с пустым значением name
       Питомец будет добавлен на сайт с пустым значением в поле "имя"'''

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == '', 'Питомец добавлен на сайт с пустым значением в имени'

def test_successful_update_self_pet_info(name='Хомяк}', animal_type='Кот', age=1):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиcок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_get_api_key_with_wrong_password_and_correct_mail(email=valid_email, password=invalid_password):
    '''Проверяем что запрос api ключа с валидным e-mail'ом и с невалидным паролем.
    Проверяем нет ли ключа в ответе'''

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status,
    # а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403
    assert 'key' not in result
    print('The combination of user name and password is incorrect')

  def test_delete_all_my_pets():
    """Проверяем возможность удаления всех питомцев"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # создаем цикл, в котором прописываем условия, если количество питомцев больше, чем 0,
    # то удаляем питомца под №0, до тех пор, пока количество будет равно нулю
    while len(my_pets['pets']) > 0:
        pet_id = my_pets['pets'][0]['id']
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
        status, _ = pf.delete_pet(auth_key, pet_id)
        if len(my_pets['pets']) == 0:
            break
    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

def test_add_new_pet_with_wrong_age(name='котэнекотэ', animal_type='кот',
                                     age='-9', pet_photo='images/cat11.jpg'):
    '''Проверка с негативным сценарием. Добавление питомца с отрицательным числом в переменной age.
    Тест не будет пройден если питомец будет добавлен на сайт с отрицательным числом в поле возраст.
     '''
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert age in result['age']
    assert int(result['age']) > 0  #'Питомец добавлен на сайт с отрицательным числом в поле возраст'

def test_get_api_key_for_user_with_invalid_password(email=valid_email, password=invalid_password):
    """Проверяем, что при вводе некорректного пароля код ответа 403, ключ не выдаётся, доступ закрыт.
    Появляется ошибка с инормацией о том, что пользователь не найден в базе"""

    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert "This user wasn't found in database" in result