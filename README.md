# Coding assignment

This coding assigment is used to evaluate applicants to the Data Engineer position at Trustly.

## Instructions
We want you to help us process some data on airports and flights. Write a small Python program that parses one or many of the attached files and outputs the number of domestic and international flights for each country according to this format: `country,domestic_flights,international_flights`, e.g.
```
Austria,2380,1220
[...]
United Kingdom,12371,2899
[...]
```
The output should be written to a file, the name of which is passed as an argument from the command line, example:
```
$ python flights.py output.txt
```
Please send us your code, either as zip-file attached to an email or if you fork this repo, a link to the fork. (Do not push to this repo, thanks!) We will get back to you with some feedback, either written or as a follow-up interview where we ask some questions and give you the opportunity to explain your design choices. We do not expect you to spend more than a few hours on the assignment. If there are unclarities, you can of course reach out to us and ask questions but even better would be that you made some reasonable assumptions and presented those assumptions together with the code.

__Note__: while you are, of course, free to use a Jupyter Notebook or similar when trying out your solution we want the submission to us to be in the form of a Python program that can be executed from command line or - theoretically - as the basis of a service we deploy to the cloud.

## Evaluation
As a Data Engineer at Trustly you will be responsible for developing and operating one of the future core assets of our company. This puts high requirements on being able to develop code and systems that are robust, maintainable, extensible and testable. Getting the correct output for this assignment is of course important but we will also put serious attention to the code quality, e.g

* Would we understand this code if we looked at it 6 months from now?
* Does it have the right abstraction level given the task at hand?
* Have you used the Python standard library where possible instead of (as an example) cooking your own sort function?
* Would it be easy/possible to test it?

## Source data
[airlines.dat](input_data/airlines.dat)
[airports.dat](input_data/airports.dat)
[planes.dat](input_data/planes.dat)
[routes.dat](input_data/routes.dat)

Documentation and links to the original files can be found at [openflights.org](https://openflights.org/data.html)
