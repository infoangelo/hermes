from flask import (
    flash, g, render_template, request, url_for
)
from werkzeug.utils import redirect
from app import app
from model import Lesson, Exp, db, Attempts
from auth import login_required
from sqlalchemy import exc

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/lessons/')
def lessons():
    lessons_list = Lesson.query.all()
    return render_template('lessons_list.html', lessons_list=lessons_list, titulo="Lições de Python:")


@app.route('/lesson/<int:id>')
@login_required
def lesson(id):
    lesson = Lesson.query.filter_by(id=id).first()
    if lesson is None:
        return redirect(url_for("lessons"))

    return render_template('lesson.html', lesson=lesson, titulo=lesson.title)


@app.route('/lessonexercise/<int:id>', methods=('GET', 'POST'))
@login_required
def lesson_exercise(id):
    lesson = Lesson.query.filter_by(id=id).first()
    if lesson is None:
        return redirect(url_for("lessons"))

    if request.method == 'POST':
        exercise = request.form['exercise']
        error = None
        level_values = {'easy': 10, 'medium': 20, 'hard': 30}

        if not exercise:
            error = 'Por favor, escreva uma resposta para o exercício.'
            return {
                "message": error,
                "sucesso": False
            }

        if error is None:
            if exercise.strip().casefold() != lesson.output_exercise.strip().casefold():
                error = 'A resposta para o exercício não está correta. Por favor tente novamente.'
                try:
                    attempt = Attempts(user_id=g.user.id, lesson_id=lesson.id)
                    db.session.add(attempt)
                    db.session.commit()
                    return {
                        "message": error,
                        "sucesso": False
                    }
                except exc.SQLAlchemyError:
                    db.session.rollback()
                    return {
                        "message": error,
                        "sucesso": False
                    }                

            else:
                try:
                    xp = Exp(user_id=g.user.id, lesson_id=lesson.id, lesson_value=lesson.exp_value, lesson_title=lesson.title)
                    db.session.add(xp)
                    db.session.commit()
                    return {
                        "message": f'Meus parabéns, sua resposta está correta, você ganhou {level_values[lesson.exp_value]} XP!',
                        "sucesso": True
                    }
                except exc.SQLAlchemyError:
                    error = f"Você já fez essa lição, então não ganha XP."
                    db.session.rollback()
                    return  {
                        "message": error,
                        "sucesso": True
                    }



        flash(error)

    return render_template('lesson_exercise.html', lesson=lesson, titulo=lesson.title)


@app.route('/xp/<int:id>')
@login_required
def xp(id):
    user_lessons_list = Exp.query.filter_by(user_id=id).all()
    level_values = {'easy': 10, 'medium': 20, 'hard': 30}
    return render_template('xp.html', user_lessons_list=user_lessons_list, level_values=level_values, titulo="Lições e experiência de {name}: ".format(name=g.user.name))


@app.route('/newlesson/', methods=('GET', 'POST'))
@login_required
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
                return redirect(url_for("lessons"))

        flash(error)

    return render_template('createlesson.html')
