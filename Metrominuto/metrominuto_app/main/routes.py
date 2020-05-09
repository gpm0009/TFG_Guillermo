"""
    metrominuto_app.main.routes

    This file contains the routes of the main module.
"""
import json
from datetime import datetime
from metrominuto_app import svgfunctions as svg_f, graphs as gph, calculateRoute as Clr
from flask import render_template, request, session, jsonify, redirect, url_for
from config import Config
from metrominuto_app.main.forms import MapForm
import googlemaps
from metrominuto_app.main import main
import os

google_maps = googlemaps.Client(key=Config.GOOGLE_API_KEY)


@main.route("/", methods=['GET', 'POST'])
def set_marks():
    with open('metrominuto_app/static/markers_example1.json') as markers_file:
        new_markers = json.load(markers_file)
    markers = []
    for element in new_markers:
        markers.append(element)
    origins = []
    destinations = []
    form = MapForm()
    if request.method == 'POST':
        mode = form.mode.data
        request_markers = json.loads(request.form['markers'])
        # for mark in request_markers['markers']:
        #     markers.append(mark)
        #     origins.append(mark['position'])
        #     destinations.append(mark['position'])
        central_markers = json.loads(request.form['central_markers'])
        # now = datetime.now()
        # matrix = google_maps.distance_matrix(origins, destinations, 'walking', departure_time=now)
        with open('metrominuto_app/static/distance_matrix_example1.json') as matrix_file:
            matrix = json.load(matrix_file)
        dist = Clr.get_distance_matrix_values(matrix)
        votes = gph.calculate_graph(dist, markers, central_markers['central_markers'], matrix)
        svg_f.draw(votes)
        return redirect(url_for('main.draw_svg'))
    longitude = -3.69
    latitude = 42.34
    return render_template(
        'map_template.html',
        longitude=longitude,
        latitude=latitude, API_KEY=Config.GOOGLE_API_KEY, form=form, positions=json.dumps(markers))  # positions=json.dumps(markers)


@main.route('/graph', methods=['GET', 'POST'])
def draw_svg():
    svg_list = []
    for i in range(0, int(session['max_votes'])):
        graph = gph.connected_graph(i)
        svg_list.append(svg_f.draw(graph))
    return render_template('show_graph.html', max=session['max_votes']-1, min=session['min_votes'], lista=svg_list)


@main.route('/setMode', methods=['POST'])
def set_mode():
    mode = request.form['mode']
    session['mode'] = mode
    if mode:
        return jsonify('OK')
    return jsonify('ERROR')


@main.route('/api/mensaje')
def mensaje():
    # return render_template('vue_template.html')
    return render_template('template.html')


@main.route('/modal')
def prueba():
    return render_template('vue_template.html')
