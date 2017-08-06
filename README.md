<p><img src="http://www.ruggedy.io/img/logo_final_skyblue.png"></p>

## About Ruggedy Limited

Ruggedy Limited is a New Zealand-based company founded by [Francois Marais](https://github.com//francois-ruggedy) and [Gareth Lawson](https://github.com/garethlawson). Our passion can be summed up as *"automation through technology that helps people in their day-to-day jobs and lives"*. Francois is an Information Security specialist and Gareth is a Software Developer. Each have more than 15 years of experience in their areas of expertise and have embarked on a journey to see how they can bring these two specialities together to create a "security as code" solution. You can read more on our website: [www.ruggedy.io](http://www.ruggedy.io).

## About Ruggedy Nikto Microservice Docker POC

This is a Proof of Concept to create an API service for common InfoSec Tools.

In the simplest terms, the application does the following:
- Run a nikto scan against a target.
- Import the data to a sqlite database.
- Send report data to the JIRA API.
- Run a local API service to extract the report data in JSON.

## Requirements

- Docker

## Setup and Installation

- Run git clone https://github.com/Ruggedy-Limited/ruggedy-nikto-microservice-poc.git
- It is REQUIRED that you open the /Files/parse.py file in an editor of your choice and configure your JIRA URL, project, username and password.
- It is REQUIRED that you open the /Files/target.txt file in an editor of your choice and configure the selected targets.
- The cron job is disabled by default. This can be enabled by removing the # in Files/crontab.

Now run the following commands from your shell while in the directory where the git repository was cloned: 
- Run `sudo docker build -t ruggedy/ruggedy .`
- Run `sudo docker run -it -p5000:5000 ruggedy/ruggedy`
- Run `sudo docker exec -it yourContainerId bash`
- Run `python /usr/bin/parse.py` in the docker container.

If all the correct data has been provided in the target.txt and parse.py files, you will see the entries in JIRA.

The API is accessible on http://yourIP:5000. Note that the API services only starts after the initial scan is completed.

## Development Roadmap

- Run a dedicated REST API service
- Interact with the application through the API (i.e. stop and start scans, update the target files and enable token authentication.)

## Contributing

Thank you for considering contributing to Ruggedy! Feel free to submit a pull request against the master branch, but if you do, all we ask is that you first check out a topic branch from master before making any commits, e.g.  
`git checkout master && git checkout -b my-new-topic`

Alternatively you can send an email to [hello@ruggedy.io](mailto:hello@ruggedy.io) if you want to discuss specific contributions.

## Security Vulnerabilities

If you discover security vulnerabilities in the application please send an email with a detailed description and proof of concept to [hello@ruggedy.io](mailto:hello@ruggedy.io).

## License

The Ruggedy application is open-sourced software licensed under the [MIT license](http://opensource.org/licenses/MIT).
