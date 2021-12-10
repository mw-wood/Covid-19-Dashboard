Web Based Coronavirus Update Dashboard

[Description]

This application is designed to retrieve both up-to-date coronavirus data from the Government's API
as well as the top news articles from global sources. These are then displayed on your web browser
where you can schedule updates for both coronavirus data and/or news articles occur at a specifiied
time. These updates can be repeated to occur daily, or can be cancelled at any time. Furthermore,
news articles can be removed from the dashboard through the user interface and will be blacklisted
from appearing again.

This application makes use of the FLASK module which provides a web host service which allows the
user the enter form data through a web based interface which is processed by a python backend.

In the future, I would hope to impliment an object oriented approach to make better use of the methods
used within the program such as the scheduled updates as it seems more appropriate.

[Installation and Use]

1. Firstly, it is necessary to sign up to create an account with newsapi in order to access up to date
news articles. This requires an email address.

https://newsapi.org/

You will recieve an 'API Key' when you complete your signup.

2. Next, You will need to access the 'config.py' file and execute it.
This will create a 'config.json' file which can be used to customise
the features within the application.

In order to access news articles, you will need to navigate under the
'user information' header within the config.json and replace the following:

'(Your API Key)' --> 'x876f6s8876s0a8f8d9s0a9s814fasd5'

{note: this is not a real API key, Your API key must fill the entire space between the speech marks}

3. Next, navigate under the user_locations header and replace the following values with your location
within the United Kingdom:

'England' --> 'YourCountry' {Where YourCountry is one of the following:
								England,
								Wales,
								Scotland,
								Northern Ireland
								
								If you live in England you can skip this step
							}

'Exeter' --> 'YourRegion' {Where YourRegion is your local authority area.
						   This can be found at:
						   https://geoportal.statistics.gov.uk/datasets/967a3660c4aa49819731ceefe4008d76/explore
						   
						   If you live in Exeter you can skip this step and the following step						
						  }
						  
'ltla' --> 'YourRegion's Area Type' {You can find Your region's area type at the previous website}

4. Lastly, you need to execute the main.py file. This starts the flask web service.

You can access the dashboard within your browser by navigating to:

	127.0.0.1:5000/index
	
You may recieve an error if the python file did not execute correctly. However, you can take these steps to troubleshoot:

-Confirming your region and API key are correct.
-Navigating to the log.log file within the project folder and finding the relevent Error message.
	-If the Error message provided is related to the source code,
	 Please contact the program Author @ https://github.com/MatthewWood-Github
	 
5. This next section will outline the use of the web application itself.

On the right on the interface you will find the news headlines column.
This will display five of the top articles from global sources.
Each article can be removed by left clicking the 'x' in the top right
corner of each article.
This will refresh the page and replace the removed article.
Removed articles will not re-appear.

In the middle of the interface, coronavirus data related to your local
and national regions. 
Below this, you can schedule updates to the interface
which will retrieve new covid data and/or news articles. The user can
choose to repeat this daily.
The user can choose which parameters they wish to assign their updates by
checking each wanted field.
A name and time must be assigned to each update otherwise the update will
not be scheduled

When an update is scheduled it will appear in the left column of the interface.
They can be cancelled in the same way as the news articles.
The website is automatically updated every 60 seconds since launching the website.

[Credits]

This was created by Matthew Wood for a university programming project.

Author's Github Page:
https://github.com/MatthewWood-Github

See project hosted on Github here:

