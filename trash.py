'''
    form_category_2 = CategoryForm()
    form_question_2_1 = QuestionForm()
    form_question_2_2 = QuestionForm()
    form_question_2_3 = QuestionForm()
    form_question_2_4 = QuestionForm()
    form_question_2_5 = QuestionForm()

    form_category_3 = CategoryForm()
    form_question_3_1 = QuestionForm()
    form_question_3_2 = QuestionForm()
    form_question_3_3 = QuestionForm()
    form_question_3_4 = QuestionForm()
    form_question_3_5 = QuestionForm()

    form_category_4 = CategoryForm()
    form_question_4_1 = QuestionForm()
    form_question_4_2 = QuestionForm()
    form_question_4_3 = QuestionForm()
    form_question_4_4 = QuestionForm()
    form_question_4_5 = QuestionForm()

    form_category_5 = CategoryForm()
    form_question_5_1 = QuestionForm()
    form_question_5_2 = QuestionForm()
    form_question_5_3 = QuestionForm()
    form_question_5_4 = QuestionForm()
    form_question_5_5 = QuestionForm()

    form_category_6 = CategoryForm()
    form_question_6_1 = QuestionForm()
    form_question_6_2 = QuestionForm()
    form_question_6_3 = QuestionForm()
    form_question_6_4 = QuestionForm()
    form_question_6_5 = QuestionForm()
    '''
    '''
        data['categories'][1]['name'] = form_category_2.category.data
        data['categories'][1]['description'] = form_category_2.description.data

        data['categories'][1]['questions'][0]['text'] = form_question_2_1.text.data
        data['categories'][1]['questions'][0]['par'] = form_question_2_1.par.data
        data['categories'][1]['questions'][0]['correct_answers'] = form_question_2_1.answers.data.split(', ')
        data['categories'][1]['questions'][0]['answer_time'] = form_question_2_1.time.data

        data['categories'][1]['questions'][1]['text'] = form_question_2_2.text.data
        data['categories'][1]['questions'][1]['par'] = form_question_2_2.par.data
        data['categories'][1]['questions'][1]['correct_answers'] = form_question_2_2.answers.data.split(', ')
        data['categories'][1]['questions'][1]['answer_time'] = form_question_2_2.time.data

        data['categories'][1]['questions'][2]['text'] = form_question_2_3.text.data
        data['categories'][1]['questions'][2]['par'] = form_question_2_3.par.data
        data['categories'][1]['questions'][2]['correct_answers'] = form_question_2_3.answers.data.split(', ')
        data['categories'][1]['questions'][2]['answer_time'] = form_question_2_3.time.data

        data['categories'][1]['questions'][3]['text'] = form_question_2_4.text.data
        data['categories'][1]['questions'][3]['par'] = form_question_2_4.par.data
        data['categories'][1]['questions'][3]['correct_answers'] = form_question_2_4.answers.data.split(', ')
        data['categories'][1]['questions'][3]['answer_time'] = form_question_2_4.time.data

        data['categories'][1]['questions'][4]['text'] = form_question_2_5.text.data
        data['categories'][1]['questions'][4]['par'] = form_question_2_5.par.data
        data['categories'][1]['questions'][4]['correct_answers'] = form_question_2_5.answers.data.split(', ')
        data['categories'][1]['questions'][4]['answer_time'] = form_question_2_5.time.data

        data['categories'][2]['name'] = form_category_3.category.data
        data['categories'][2]['description'] = form_category_3.description.data

        data['categories'][2]['questions'][0]['text'] = form_question_3_1.text.data
        data['categories'][2]['questions'][0]['par'] = form_question_3_1.par.data
        data['categories'][2]['questions'][0]['correct_answers'] = form_question_3_1.answers.data.split(', ')
        data['categories'][2]['questions'][0]['answer_time'] = form_question_3_1.time.data

        data['categories'][2]['questions'][1]['text'] = form_question_3_2.text.data
        data['categories'][2]['questions'][1]['par'] = form_question_3_2.par.data
        data['categories'][2]['questions'][1]['correct_answers'] = form_question_3_2.answers.data.split(', ')
        data['categories'][2]['questions'][1]['answer_time'] = form_question_3_2.time.data

        data['categories'][2]['questions'][2]['text'] = form_question_3_3.text.data
        data['categories'][2]['questions'][2]['par'] = form_question_3_3.par.data
        data['categories'][2]['questions'][2]['correct_answers'] = form_question_3_3.answers.data.split(', ')
        data['categories'][2]['questions'][2]['answer_time'] = form_question_3_3.time.data

        data['categories'][2]['questions'][3]['text'] = form_question_3_4.text.data
        data['categories'][2]['questions'][3]['par'] = form_question_3_4.par.data
        data['categories'][2]['questions'][3]['correct_answers'] = form_question_3_4.answers.data.split(', ')
        data['categories'][2]['questions'][3]['answer_time'] = form_question_3_4.time.data

        data['categories'][2]['questions'][4]['text'] = form_question_3_5.text.data
        data['categories'][2]['questions'][4]['par'] = form_question_3_5.par.data
        data['categories'][2]['questions'][4]['correct_answers'] = form_question_3_5.answers.data.split(', ')
        data['categories'][2]['questions'][4]['answer_time'] = form_question_3_5.time.data

        data['categories'][3]['name'] = form_category_4.category.data
        data['categories'][3]['description'] = form_category_4.description.data

        data['categories'][3]['questions'][0]['text'] = form_question_4_1.text.data
        data['categories'][3]['questions'][0]['par'] = form_question_4_1.par.data
        data['categories'][3]['questions'][0]['correct_answers'] = form_question_4_1.answers.data.split(', ')
        data['categories'][3]['questions'][0]['answer_time'] = form_question_4_1.time.data

        data['categories'][3]['questions'][1]['text'] = form_question_4_2.text.data
        data['categories'][3]['questions'][1]['par'] = form_question_4_2.par.data
        data['categories'][3]['questions'][1]['correct_answers'] = form_question_4_2.answers.data.split(', ')
        data['categories'][3]['questions'][1]['answer_time'] = form_question_4_2.time.data

        data['categories'][3]['questions'][2]['text'] = form_question_4_3.text.data
        data['categories'][3]['questions'][2]['par'] = form_question_4_3.par.data
        data['categories'][3]['questions'][2]['correct_answers'] = form_question_4_3.answers.data.split(', ')
        data['categories'][3]['questions'][2]['answer_time'] = form_question_4_3.time.data

        data['categories'][3]['questions'][3]['text'] = form_question_4_4.text.data
        data['categories'][3]['questions'][3]['par'] = form_question_4_4.par.data
        data['categories'][3]['questions'][3]['correct_answers'] = form_question_4_4.answers.data.split(', ')
        data['categories'][3]['questions'][3]['answer_time'] = form_question_4_4.time.data

        data['categories'][3]['questions'][4]['text'] = form_question_4_5.text.data
        data['categories'][3]['questions'][4]['par'] = form_question_4_5.par.data
        data['categories'][3]['questions'][4]['correct_answers'] = form_question_4_5.answers.data.split(', ')
        data['categories'][3]['questions'][4]['answer_time'] = form_question_4_5.time.data

        data['categories'][4]['name'] = form_category_5.category.data
        data['categories'][4]['description'] = form_category_5.description.data

        data['categories'][4]['questions'][0]['text'] = form_question_5_1.text.data
        data['categories'][4]['questions'][0]['par'] = form_question_5_1.par.data
        data['categories'][4]['questions'][0]['correct_answers'] = form_question_5_1.answers.data.split(', ')
        data['categories'][4]['questions'][0]['answer_time'] = form_question_5_1.time.data

        data['categories'][4]['questions'][1]['text'] = form_question_5_2.text.data
        data['categories'][4]['questions'][1]['par'] = form_question_5_2.par.data
        data['categories'][4]['questions'][1]['correct_answers'] = form_question_5_2.answers.data.split(', ')
        data['categories'][4]['questions'][1]['answer_time'] = form_question_5_2.time.data

        data['categories'][4]['questions'][2]['text'] = form_question_5_3.text.data
        data['categories'][4]['questions'][2]['par'] = form_question_5_3.par.data
        data['categories'][4]['questions'][2]['correct_answers'] = form_question_5_3.answers.data.split(', ')
        data['categories'][4]['questions'][2]['answer_time'] = form_question_5_3.time.data

        data['categories'][4]['questions'][3]['text'] = form_question_5_4.text.data
        data['categories'][4]['questions'][3]['par'] = form_question_5_4.par.data
        data['categories'][4]['questions'][3]['correct_answers'] = form_question_5_4.answers.data.split(', ')
        data['categories'][4]['questions'][3]['answer_time'] = form_question_5_4.time.data

        data['categories'][4]['questions'][4]['text'] = form_question_5_5.text.data
        data['categories'][4]['questions'][4]['par'] = form_question_5_5.par.data
        data['categories'][4]['questions'][4]['correct_answers'] = form_question_5_5.answers.data.split(', ')
        data['categories'][4]['questions'][4]['answer_time'] = form_question_5_5.time.data

        data['categories'][5]['name'] = form_category_6.category.data
        data['categories'][5]['description'] = form_category_6.description.data

        data['categories'][5]['questions'][0]['text'] = form_question_6_1.text.data
        data['categories'][5]['questions'][0]['par'] = form_question_6_1.par.data
        data['categories'][5]['questions'][0]['correct_answers'] = form_question_6_1.answers.data.split(', ')
        data['categories'][5]['questions'][0]['answer_time'] = form_question_6_1.time.data

        data['categories'][5]['questions'][0]['text'] = form_question_6_2.text.data
        data['categories'][5]['questions'][0]['par'] = form_question_6_2.par.data
        data['categories'][5]['questions'][0]['correct_answers'] = form_question_6_2.answers.data.split(', ')
        data['categories'][5]['questions'][0]['answer_time'] = form_question_6_2.time.data

        data['categories'][5]['questions'][0]['text'] = form_question_6_3.text.data
        data['categories'][5]['questions'][0]['par'] = form_question_6_3.par.data
        data['categories'][5]['questions'][0]['correct_answers'] = form_question_6_3.answers.data.split(', ')
        data['categories'][5]['questions'][0]['answer_time'] = form_question_6_3.time.data

        data['categories'][5]['questions'][0]['text'] = form_question_6_4.text.data
        data['categories'][5]['questions'][0]['par'] = form_question_6_4.par.data
        data['categories'][5]['questions'][0]['correct_answers'] = form_question_6_4.answers.data.split(', ')
        data['categories'][5]['questions'][0]['answer_time'] = form_question_6_4.time.data

        data['categories'][5]['questions'][0]['text'] = form_question_6_5.text.data
        data['categories'][5]['questions'][0]['par'] = form_question_6_5.par.data
        data['categories'][5]['questions'][0]['correct_answers'] = form_question_6_5.answers.data.split(', ')
        data['categories'][5]['questions'][0]['answer_time'] = form_question_6_5.time.data
        '''
        '''
form_category_2=form_category_2,
form_question_2_1=form_question_2_1,
form_question_2_2=form_question_2_2,
form_question_2_3=form_question_2_3,
form_question_2_4=form_question_2_4,
form_question_2_5=form_question_2_5,
form_category_3=form_category_3,
form_question_3_1=form_question_3_1,
form_question_3_2=form_question_3_2,
form_question_3_3=form_question_3_3,
form_question_3_4=form_question_3_4,
form_question_3_5=form_question_3_5,
form_category_4=form_category_4,
form_question_4_1=form_question_4_1,
form_question_4_2=form_question_4_2,
form_question_4_3=form_question_4_3,
form_question_4_4=form_question_4_4,
form_question_4_5=form_question_4_5,
form_category_5=form_category_5,
form_question_5_1=form_question_5_1,
form_question_5_2=form_question_5_2,
form_question_5_3=form_question_5_3,
form_question_5_4=form_question_5_4,
form_question_5_5=form_question_5_5,
form_category_6=form_category_6,
form_question_6_1=form_question_6_1,
form_question_6_2=form_question_6_2,
form_question_6_3=form_question_6_3,
form_question_6_4=form_question_6_4,
form_question_6_5=form_question_6_5
'''
