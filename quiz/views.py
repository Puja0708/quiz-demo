import json
import os
from . import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from itertools import groupby

json_data = open(os.path.join(settings.BASE_DIR, 'famous_scientists.json'))
data1 = json.load(json_data) 
data2 = json.dumps(data1) 
players_data = data1['players']
questions_data = data1['questions']
response_data = data1['responses']


def detail(request):
	players_array = []
	questions_array = []	
	total_questions = len(data1['questions'])

	for player in players_data:
		player_name = player['id']
		number_of_correct_responses = 0
		number_of_incorrect_responses = 0
		for response in response_data:
			if response['playerId'] == player_name and response['ic']  :
				number_of_correct_responses += 1
			elif response['playerId'] == player_name and not response['ic'] :
				number_of_incorrect_responses += 1
		percentage = number_of_correct_responses*100/(number_of_correct_responses + number_of_incorrect_responses )
		current_player_data = ['Player Name : ' + player_name, 'Correct responses : ' + str(number_of_correct_responses), 'Incorrect responses : ' +str(number_of_incorrect_responses), 'Percentage : ' + str(percentage)]
		players_array.append(current_player_data)


	for question in questions_data:
		question_number = question['_id']
		question_text = question['questionText']
		number_of_correct_responses = 0
		number_of_incorrect_responses = 0
		for response in response_data:
			if response['questionId'] == question_number and response['ic']  :
				number_of_correct_responses += 1
			elif response['questionId'] == question_number and not response['ic'] :
				number_of_incorrect_responses += 1
		percentage = number_of_correct_responses*100/(number_of_correct_responses + number_of_incorrect_responses )
		current_question_data = ['Question Number : ' + question_number,  'Question Test : ' +question_text, 'Correct responses : ' + str(number_of_correct_responses), 'Incorrect responses : ' +str(number_of_incorrect_responses), 'Percentage : ' + str(percentage)]
		questions_array.append(current_question_data)

	return render_to_response('detail.html', { 'players': players_array, 'questions' : questions_array})

def table(request):
	player_names = []
	question_ids = []
	for player in players_data:
		player_names.append(player['id'])
	for question in questions_data:
		question_ids.append(question['_id'])
	final_array = []
	total_players = len(player_names)
	print 'aaaaaaaaaaaaaaaaaa',total_players
	count = 0
	diff = len(question_ids) - total_players if len(question_ids)>total_players else 0
	for i in xrange(total_players):
		count += 1
		responses = []
		responses.append(question_ids[i])
		for question in question_ids:
			for response in response_data:
				if response['questionId'] == question  and response['playerId'] == player_names[i] and response['ic'] :
					# print 1
					answer = 1
					responses.append(answer)
				elif response['questionId'] == question  and response['playerId'] == player_names[i] and not response['ic'] :
					# print 0
					answer = 0
					responses.append(answer)
		if diff>0:
			responses = responses[0:len(responses)-diff]
		final_array.append( responses)

	return render_to_response('table.html', { 'players_data': player_names, 'questions_data' : final_array})

def charts(request):
	question_array = []
	players_array = []
	for question in questions_data:
		number_of_correct_responses = 0
		for response in response_data:
			if response['questionId'] == question['_id'] and response['ic']  :
					number_of_correct_responses += 1
		question_array.append([str(question['_id']).split("'")[0],number_of_correct_responses])
	for player in players_data:
		number_of_correct_responses = 0
		for response in response_data:
			if response['playerId'] == player['id'] and response['ic']  :
					number_of_correct_responses += 1
		player_name =  unicode(str(player['id']).split("'")[0], "utf-8") 
		players_array.append([player_name,number_of_correct_responses])
	print players_array
	print question_array
	return render_to_response('charts.html', { 'players_data': players_array, 'questions_data' : question_array})

