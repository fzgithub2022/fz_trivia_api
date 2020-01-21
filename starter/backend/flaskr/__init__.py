import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app)

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    categories = Category.query.all()
    formatted_categories = [category.format() for category in categories]
    return jsonify({'categories':formatted_categories})

  @app.route('/add_category', methods=['POST'])
  def add_category():
    category = Category(request.args.get('type'))
    category.insert()
    return jsonify({
      'message':'Inserted {} successfully!'.format(category.type)
    })
  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def get_questions():
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * 10
    end = start + 10
    questions = Question.query.order_by(Question.id).all()
    formatted_questions = [question.format() for question in questions]
    total_questions = len(questions)
    current_category = request.args.get('current_category', 1, type=int)
    categories = get_categories()
    return jsonify({
      'questions':formatted_questions[start:end],
      'total_questions':total_questions,
      'categories':categories,
      'current_category':current_category
      })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/del_question', methods=['DELETE'])
  def del_question():
    question_id = request.args.get('qid')
    return jsonify({'message':'DELETED QUESTION {}'.format(question_id)})
  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def add_question():
    #body = request.get_json()
    question = 'great'
    return jsonify({'question':'question is {}'.format(question)})

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/search_questions', methods=['GET'])
  def search_questions():
    term = request.args.get('term')
    term2 = request.args.get('term2')
    return jsonify({'message':'You searched {} and {}'.format(term,term2)})
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/questions/<int:q_id>')
  def get_question(q_id):
    question = Question.query.filter(Question.id == q_id).one_or_none()
    if question is None:
      return jsonify({'question':'None question with id {}'.format(q_id)})
    else:
      return jsonify({'question':question.format()})
  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/post_question', methods=['POST'])
  def post_question():
    category = request.args.get('category')
    prev_question = request.args.get('prev')
    return jsonify({'message':'You searched {} and {}'.format(category,prev_question)})
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'status':'Not Found',
      'error':404,
      'message': 'resource not found'
    })
  
  @app.errorhandler(422)
  def not_processed(error):
    return jsonify({
      'status':'Unprocessable Entity',
      'error':422,
      'message': 'type and syntax ok but could not process'
    })

  
  return app

    