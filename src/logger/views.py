from flask import request, render_template

from src import app
from src.logger.models import LoggerModel


@app.route('/', methods=['GET'])
def logs():
    sort_by = request.args.get('sort_by', 'date_and_time')
    order = request.args.get('order', 'desc')
    search = request.args.get('search', '')

    if order == 'asc':
        order_by = sort_by
    else:
        order_by = f'-{sort_by}'

    logs = LoggerModel.objects(message__icontains=search).order_by(order_by)
    return render_template('index.html', logs=logs, sort_by=sort_by, order=order, search=search)
