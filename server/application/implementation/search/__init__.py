from datetime import date
from flask import request, jsonify, make_response
from application import app, db
from application.common.templates import SEARCH_PUBLICATIONS
from application.common.helpers import parse_date, get_publication_format
from application.common.const import ERROR_MESSANGES, RESPONSE_CODES


@app.route('/api/search/', methods=['GET'])
def search():
    data = request.json
    keywords = data.get('keywords')
    enterprise = data.get('enterprise')
    date_from = parse_date(data.get('date_from')) if data.get('date_from') else date(year=1, month=1, day=1)
    date_to = parse_date(data.get('date_to')) if data.get('date_to') else date.today()

    if not all([data, keywords, enterprise]):
        return make_response(ERROR_MESSANGES['bad_params'], RESPONSE_CODES['bad_request'])

    test = db.session.execute(
        SEARCH_PUBLICATIONS.format(
            keywords=str(keywords).replace('[', '{').replace(']', '}'),
            enterprise=enterprise,
            date_from=date_from,
            date_to=date_to
        )
    ).fetchall()
    return jsonify([get_publication_format(elem) for elem in test])
