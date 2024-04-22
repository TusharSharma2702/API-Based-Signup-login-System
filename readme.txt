API-BASED SIGNUP/LOGIN SYSTEM

Steps to set up and run the chat bots: 

1) Setup a virtual Environment

	Virtual Environment is a tool that helps to keep dependencies required by different projects separate by setting up an isolated 	virtual environment for them.

	Open terminal use command – “conda create -p virtual_ environment _name python == 3.10”

	This command sets up a virtual environment with python version specified for this particular project we are going to use 	version 	3.10 or greater.

	Once the virtual environment is set up use command “conda actvate virtual_ environment _name” to activate your virtual 	environment.

 

2) Install all the dependencies listed in requirements.txt

	Requirement.txt contains all the required dependencies list that are required for the execution of the program smoothly so it 	is important to install all the required library into your virtual environment. 
      
	Use command – “pip install -r requirements.txt”

3) Opening the flask Application

	Open your editor and run "app.py"

      	You can view the Flask app in your local browser at http://127.0.0.1:5000

4) User Registration
	
	Provide details to register as a user through "/signup" endpoint 
	
	click on the submit button after entering the details.

5) Login
	
	Users can login through the "/login" endpoint by providing the necessary details.
	
	User credentials are matched with those that were provided during registration time if match user is granted the access to 	website content
