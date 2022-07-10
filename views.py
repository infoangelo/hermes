from flask import (
    flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.utils import redirect
from app import app
from model import Lesson, Exp, db


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/lessons/')
def lessons():
    lessons_list = Lesson.query.all()
    return render_template('lessons_list.html', lessons_list=lessons_list)


@app.route('/lesson/<int:id>')
def lesson(id):
    lesson = Lesson.query.filter_by(id=id).first()
    return render_template('lesson.html', lesson=lesson)


@app.route('/lessonexercise/<int:id>', methods=('GET', 'POST'))
def lesson_exercise(id):
    lesson = Lesson.query.filter_by(id=id).first()
    if request.method == 'POST':
        exercise = request.form['exercise']
        error = None
        level_values = {'easy':10, 'medium':20, 'hard':30}
        lesson_value = level_values[lesson.exp_value]

        if not exercise:
            error = 'Campo exercício é obrigatório.'

        if error is None:
            if exercise.casefold() != lesson.output_exercise.casefold():
                error = 'Sua resposta no exercício não está correta'
            else:
                try:
                    xp = Exp(user_id=g.user.id, lesson_value=lesson_value, lesson_title=lesson.title)
                    db.session.add(xp)
                    db.session.commit()
                    return redirect(url_for("lesson", id=lesson.id + 1))
                except db.IntegrityError:
                    error = f"Não foi possível somar experiência."

        else:
            return redirect(url_for("index"))

        flash(error)

    return render_template('lesson_exercise.html', lesson=lesson)


@app.route('/newlesson/', methods=('GET', 'POST'))
def newlesson():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        content = request.form['content']
        exercise = request.form['exercise']
        input_exercise = request.form['input_exercise']
        output_exercise = request.form['output_exercise']
        level = request.form['level']
        error = None

        if not title:
            error = 'Campo título é obrigatório.'
        elif not description:
            error = 'Campo descrição é obrigatório.'
        elif not content:
            error = 'Campo conteúdo é obrigatório.'
        elif not exercise:
            error = 'Campo exercício é obrigatório.'

        if error is None:
            try:
                lesson = Lesson(title=title, description=description, content=content, exercise=exercise,
                                input_exercise=input_exercise, output_exercise=output_exercise, exp_value=level)
                db.session.add(lesson)
                db.session.commit()
            except db.IntegrityError:
                error = f"Lição {title} já foi registrada."
            else:
                return redirect(url_for("index"))

        flash(error)

    return render_template('createlesson.html')
