import os
import redis
from flask import Flask, render_template, redirect, request, url_for, make_response

r = redis.Redis(host='redis-10385.c15.us-east-1-4.ec2.cloud.redislabs.com', port='10385', password='ol2PPKvWdReZQXu2')

app = Flask(__name__)

@app.route('/')
def survey():
	resp = make_response(render_template('survey.html'))
	return resp

@app.route('/suthankyou.html', methods=['POST'])
def suthankyou():

    ## This is how you grab the contents from the form
	entity = request.form['entity']
	state = request.form['state']
	f = request.form['feedback']
    ## Now you can now do someting with variable "f"
##	r.rpush('mylist', entity)
##	r.rpush('mylist', state)
##	r.rpush('mylist', f)
	r.hset('myhash',{'entity': entity, 'state': state, 'feedback': f })	
#### Display the length of the list
	resp = """
    <h3> - THANKS FOR TAKING THE SURVEY - </h3>
    <a href="/"><h3>Back to main menu</h3></a>
    <a href="/dump"><h3>Dump Data</h3></a>
    	"""
	
	return resp
		
@app.route('/dump')
def dump():
	number = r.llen('mylist')	
	data = r.lrange('mylist',0,-1)
	data_string = "<br>"
	for i in data:
		data_string = data_string + str(i) + "<br>"
		
	resp = """
	<h3> DATA SO FAR </h3>
	<br>
	{} Items in the database.<br>
	{}
	""".format(number, data_string)
	
	return resp
	
	
if __name__ == "__main__":
	app.run(debug=False, host='0.0.0.0', \
                port=int(os.getenv('PORT', '5000')), threaded=True)
