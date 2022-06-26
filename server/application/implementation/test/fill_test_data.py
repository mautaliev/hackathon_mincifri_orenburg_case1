import datetime

from flask import make_response
from application import app, db
from application.models import KeyWord, Enterprise, Publication


@app.route('/api/fill_test_data/')
def make_envinronment():
    """
    Заполнить БД вспомогательными тестовыми сущностями
    :return:
    """

    keywords_amount, ir_amount, enterprises_amount = 100, 100, 100
    keywords = [get_keyword(i) for i in range(1, keywords_amount + 1)]
    information_resources = [get_information_resource(i) for i in range(1, ir_amount + 1)]
    enterprises = [get_enterprises(i) for i in range(1, enterprises_amount + 1)]

    dt_now = datetime.datetime.now()

    publication_amount = 100
    publications = [get_publication(i, dt_now) for i in range(1, publication_amount + 1)]

    for keyword in keywords:
        obj = KeyWord(keyword['id'], keyword['name'])
        db.session.add(obj)

    for ir in information_resources:
        obj = InformationResource(ir['id'], ir['name'])
        db.session.add(obj)

    for enterprise in enterprises:
        obj = Enterprise(enterprise['id'], enterprise['name'])
        db.session.add(obj)
    db.session.commit()

    for publication in publications:
        obj = Publication(publication['title'], publication['date_of_publication'],
                          publication['publication_url'], publication['enterprise_id'],
                          publication['informationResource_id'])
        db.session.add(obj)
    db.session.commit()

    for i in range(1, 100):
        for j in range(1, 5):
            db.session.execute(
                f"INSERT INTO public.publication_keyword(publication_id, keyword_id) VALUES ({i}, {j}) on conflict do nothing;")

    db.session.commit()



    return make_response('Записи успешно добавлены', 200)


def get_publication(number, date):
    return {
        'title': f'publication_{number}',
        'date_of_publication': date,
        'publication_url': f'URL-{number}',
        'enterprise_id': number,
        'informationResource_id': number
    }


def get_keyword(number):
    return {
        'id': number,
        'name': f'keyword_{number}'
    }


def get_information_resource(number):
    return {
        'id': number,
        'name': f'information_resource_{number}'
    }


def get_enterprises(number):
    return {
        'id': number,
        'name': f'enterprises_{number}'
    }

