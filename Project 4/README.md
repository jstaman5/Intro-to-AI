Jared Staman
CS 423: Artifial Intelligence

How to run code:

	(Command Line)
	python main.py -root https://eecs.utk.edu -mode C -verbose T -query henley


	Command line: verbose is optional, query is required

	(Interactive Mode)
	python main.py -root https://eecs.utk.edu -mode I -verbose T

	Interactive mode: verbose is required, query is prohibited

	commands in Interactive mode:
	:exit    - exits interactive mode
	:delete  - deletes the pickle files
	:train   - trains new pickle files

	In interactive mode, once you have pickle files, you can enter any string besides
	the commands to send in as a query. It will then give you the 5 documents that
	relate the most to that query.

	