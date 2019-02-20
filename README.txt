-- Run JSONparser -- 
To use:
1. Run from command line using: 
python3 JSONparser.py <file_name.json>
2. <file_name.json> is optional, if ommitted, program will prompt you a series of input strings. 

-- Run Unit Tests --  
To run unittests.py from command line, ensure both in the same directory and run:
python3 -m unittest unittests.py 

-- Comments -- 
Was fun to make, albeit very hard to read through the documentation when you haven't touched the material in classes. After reading through multiple docs and guides, finally understood the official documentation! It was fun in terms of how it seems so elegant. 

My first time implementing unit-testing too, and to be honest, I'm not too sure what is the extent and how robust should my unit-testing be in the future, i.e.

    1. Create unit tests for every possible scenario?
    2. Create unit tests for most common scenarios - a few edge cases - and for caught bugs too?

I think my answer for this is 2., as there must be a tradeoff between the time spent making unit tests and other important work. What I meant for 'for caught bugs' were that I read somewhere the best kind of unit tests are the ones where you had a bug before, as they tend to either be common mistakes, or special kinds of scenarios where you overlooked!

