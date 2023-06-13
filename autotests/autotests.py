import pytest
import requests

url = 'https://jsonplaceholder.typicode.com'

# Данные ниже взяты из руководства к https://jsonplaceholder.typicode.com
posts_total = 100
posts_per_user = 10
comments_per_post = 5

# Валидные тестовые данные:
test_data_post_id = [1, 50, 99, 100]
test_data_user_id = [1, 5, 9, 10]

# Некорректные тестовые данные:
# (валидные несуществующие значения)
test_data_post_id_non_existent = [0, 101, 435]
test_data_user_id_non_existent = [0, 11, 43]
# (невалидные значения)
test_data_post_id_invalid = ['a', '!']
test_data_user_id_invalid = ['a', '!']


#
# ПОЗИТИВНЫЕ ПРОВЕРКИ
#
# GET

def test_get_all_posts_check_status_is_200():
    """Проверка: запрос GET к /posts успешен"""
    response = requests.get(f'{url}/posts')
    assert response.status_code == 200


def test_get_all_posts_check_all_posts_returned():
    """Проверка: запрос GET к /posts действительно возвращает все посты"""
    response = requests.get(f'{url}/posts')
    response_body = response.json()
    assert len(response_body) == posts_total


@pytest.mark.parametrize('user_id', test_data_user_id)
def test_get_all_posts_with_filter_status_is_200(user_id):
    """Проверка: запрос GET к /posts с фильтром по валидному userId успешен"""
    response = requests.get(f'{url}/posts?userId={user_id}')
    assert response.status_code == 200


@pytest.mark.parametrize('user_id', test_data_user_id)
def test_get_all_posts_with_filter_correctly(user_id):
    """Проверка: запрос GET к /posts с фильтром по валидному userId возвращает искомые посты"""
    response = requests.get(f'{url}/posts?userId={user_id}')
    response_body = response.json()

    user_check = 0
    for element in response_body:
        if element['userId'] == user_id:
            user_check += 1
        else:
            continue

    assert user_check == posts_per_user


@pytest.mark.parametrize('post_id', test_data_post_id)
def test_get_exact_post_status_is_200(post_id):
    """Проверка: запрос GET к /posts/id по валидному id возвращает искомый пост"""
    response = requests.get(f'{url}/posts/{post_id}')
    assert response.status_code == 200


@pytest.mark.parametrize('post_id', test_data_post_id)
def test_get_exact_post_content_type_is_correct(post_id):
    """Проверка: запрос GET к /posts/id по валидному id возвращает ответ в верном формате"""
    response = requests.get(f'{url}/posts/{post_id}')
    assert response.headers['Content-Type'] == 'application/json; charset=utf-8'


@pytest.mark.parametrize('post_id', test_data_post_id)
def test_get_exact_post_body_is_correct(post_id):
    """Проверка: запрос GET к /posts/id по валидному id возвращает корректное тело поста"""
    response = requests.get(f'{url}/posts/{post_id}')
    response_body = response.json()
    assert \
        len(response_body) == 4 and \
        'userId' in response_body and \
        'id' in response_body and \
        'title' in response_body and \
        'body' in response_body


@pytest.mark.parametrize('post_id', test_data_post_id)
def test_get_comments_for_exact_post_status_is_200(post_id):
    """Проверка: запрос GET к /posts/id/comments по валидному id успешен"""
    response = requests.get(f'{url}/posts/{post_id}/comments')
    assert response.status_code == 200


@pytest.mark.parametrize('post_id', test_data_post_id)
def test_get_comments_for_exact_post_correctly(post_id):
    """Проверка: запрос GET к /posts/id/comments по валидному id возвращает искомые комментарии"""
    response = requests.get(f'{url}/posts/{post_id}/comments')
    response_body = response.json()

    post_check = 0
    for element in response_body:
        if element['postId'] == post_id:
            post_check += 1
        else:
            continue

    assert post_check == comments_per_post


# DELETE

@pytest.mark.parametrize('post_id', test_data_post_id)
def test_delete_post_status_is_200(post_id):
    """Проверка: запрос DELETE к posts/id по валидному id успешен"""
    response = requests.delete(f'{url}/posts/{post_id}')
    assert response.status_code == 200


# POST

def test_post_create_new_post_with_valid_body_status_is_201():
    """Проверка: запрос POST с заголовком и валидными данными успешен"""
    response = requests.post(f'{url}/posts', json={"title": "foo", "body": "bar", "userId": 1})
    assert response.status_code == 201


def test_post_create_new_post_with_valid_body_response_is_correct():
    """Проверка: запрос POST с заголовком и валидными данными возвращает верные данные"""
    response = requests.post(f'{url}/posts', json={"title": "foo", "body": "bar", "userId": 1})
    response_body = response.json()
    assert \
        len(response_body) == 4 and \
        response_body['userId'] == 1 and \
        response_body['title'] == 'foo' and \
        response_body['body'] == 'bar' and \
        'id' in response_body


#
# НЕГАТИВНЫЕ ПРОВЕРКИ
#
# GET

@pytest.mark.parametrize('user_id', test_data_user_id_non_existent)
def test_get_all_posts_with_non_existent_filter_status_is_404(user_id):
    """Проверка: запрос GET к /posts с фильтром по несуществующему userId возвращает ошибку 404"""
    response = requests.get(f'{url}/posts?userId={user_id}')
    assert response.status_code == 404


@pytest.mark.parametrize('user_id', test_data_user_id_invalid)
def test_get_all_posts_with_invalid_filter_status_is_400(user_id):
    """Проверка: запрос GET к /posts с фильтром по невалидному userId возвращает ошибку 400"""
    response = requests.get(f'{url}/posts?userId={user_id}')
    assert response.status_code == 400


@pytest.mark.parametrize('post_id', test_data_post_id_non_existent)
def test_get_exact_post_with_non_existent_id_status_is_404(post_id):
    """Проверка: запрос GET к /posts/id по несуществующему id возвращает ошибку 404"""
    response = requests.get(f'{url}/posts/{post_id}')
    assert response.status_code == 404


@pytest.mark.parametrize('post_id', test_data_post_id_invalid)
def test_get_exact_post_with_invalid_id_status_is_400(post_id):
    """Проверка: запрос GET к /posts/id по невалидному id возвращает ошибку 400"""
    response = requests.get(f'{url}/posts/{post_id}')
    assert response.status_code == 400


@pytest.mark.parametrize('post_id', test_data_post_id_non_existent)
def test_get_comments_for_exact_post_with_non_existent_id_status_is_404(post_id):
    """Проверка: запрос GET к /posts/id/comments по несуществующему id возвращает ошибку 404"""
    response = requests.get(f'{url}/posts/{post_id}/comments')
    assert response.status_code == 404


@pytest.mark.parametrize('post_id', test_data_post_id_invalid)
def test_get_comments_for_exact_post_with_invalid_id_status_is_400(post_id):
    """Проверка: запрос GET к /posts/id/comments по невалидному id возвращает ошибку 400"""
    response = requests.get(f'{url}/posts/{post_id}/comments')
    assert response.status_code == 400


# DELETE

@pytest.mark.parametrize('post_id', test_data_post_id_non_existent)
def test_delete_post_with_non_existent_id_status_is_404(post_id):
    """Проверка: запрос DELETE к posts/id по несуществующему id возвращает ошибку 404"""
    response = requests.delete(f'{url}/posts/{post_id}')
    assert response.status_code == 404


@pytest.mark.parametrize('post_id', test_data_post_id_invalid)
def test_delete_post_with_invalid_id_status_is_404(post_id):
    """Проверка: запрос DELETE к posts/id по невалидному id возвращает ошибку 400"""
    response = requests.delete(f'{url}/posts/{post_id}')
    assert response.status_code == 400


# POST

def test_post_create_new_post_with_empty_body_status_is_400():
    """Проверка: запрос POST к /posts с пустым телом возвращает ошибку 400"""
    response = requests.post(f'{url}/posts')
    assert response.status_code == 400


def test_post_create_new_post_with_only_one_field_status_is_400():
    """Проверка: запрос POST к /posts с лишь одним заполненным полем в теле возвращает ошибку 400"""
    response = requests.post(f'{url}/posts', json={"title": "foo"})
    assert response.status_code == 400


def test_post_create_new_post_with_wrong_field_user_id_status_is_400():
    """Проверка: запрос POST к /posts с неверным типом данных в userId возвращает ошибку 400"""
    response = requests.post(
        f'{url}/posts', json={"title": "foo", "body": "bar", "userId": "a"}
    )
    assert response.status_code == 400


def test_post_create_new_post_with_no_field_user_id_status_is_400():
    """Проверка: запрос POST к /posts без пары ключ:значение для userId возвращает ошибку 400"""
    response = requests.post(
        f'{url}/posts', json={"title": "foo", "body": "bar"}
    )
    assert response.status_code == 400


def test_post_create_new_post_with_wrong_field_title_status_is_400():
    """Проверка: запрос POST к /posts с неверным типом данных в title возвращает ошибку 400"""
    response = requests.post(
        f'{url}/posts', json={"title": 1, "body": "bar", "userId": 1}
    )
    assert response.status_code == 400


def test_post_create_new_post_with_no_field_title_status_is_400():
    """Проверка: запрос POST к /posts без пары ключ:значение для title возвращает ошибку 400"""
    response = requests.post(
        f'{url}/posts', json={"body": "bar", "userId": 1}
    )
    assert response.status_code == 400


def test_post_create_new_post_with_wrong_field_body_status_is_400():
    """Проверка: запрос POST к /posts с неверным типом данных в body возвращает ошибку 400"""
    response = requests.post(
        f'{url}/posts', json={"title": "foo", "body": 1, "userId": 1}
    )
    assert response.status_code == 400


def test_post_create_new_post_with_no_field_body_status_is_400():
    """Проверка: запрос POST к /posts без пары ключ:значение для body возвращает ошибку 400"""
    response = requests.post(
        f'{url}/posts', json={"title": "foo", "userId": 1}
    )
    assert response.status_code == 400
