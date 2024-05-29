# Example of a light planning spec for my sketch

(I've copy/pasted the instructions below, my examples are between the two dashed lines ...)



### General description of the project (2 pts)
- start with your sketch and enhance it.
- should be about a half page (3 - 5 paragraphs) and introduce your project to a extend that outsiders, like you classmates, can get the gist of the project. 
- Mention, if applicable, what external mechanisms (major packages, API, email, twitter, etc.) you will use
- What GUI would it ideally use? Could it minimally run with a command line interface (CLI).
- Could this also have a "remote" control, e.g. offer some form of API?


-----------------------------------------------------------------------------------------
- The app will show the most severe historical quake activity at a user given location and within a user given radius. 
- I envision a map of the area with quake locations shown as point markers and date and magnitude as number labels. 
- By default the most severe quakes (up to 100) from 1900 - present would be shown. Each marker could visualize additional quake properties. 
- The user should be able to filter/refine this by setting ranges for date, magnitude and depth and overall number. 
- Additionally, users can request a statistics table and plot (graph, non-map!) of these quakes. 
--------------------------------------------------------------------------------------

### Task Vignettes (User activity "flow") (4 pts)
- For each major task write a short vignette that illustrates it. Again, it's OK to just assume a lot of things ... like that your user really needs to perform a task (although you don't actually know) or that the task will be performed magically (to be solved later).
- The order of your task should make sense. It's OK to bundle several tasks into a vignette if they are naturally related 
- I expect 1-3 paragraphs per vignette
- After each vignette, list technical details as bullet points. This includes anything that the user may not be aware of but that could be potentially important for the implementation.

- If you can, add crude design mockups or wire frames (hand drawn or simple power point diagrams) that capture the user interaction. You can re-use mockups created for the sketches. However, these are __not a must!__  For now, just articulate what actions happen and what data flows where. 
- You don't have to design a GUI for the spec, although for many that's a natural way to articulate the activity and you're welcome to use it as a "graphical language". Just know that for your version 1, you may actually end up implementing the data flow as a command line interface!

------------------------------------------------------------------------------------------
1) User input (location and radius)

Bob knows that Southern California is prone to earthquakes. He want to know more about the area around LA. He opens the app and is shown a map of the US and a UI element (button) that reads NEW. (Other buttons may be shown below but will be greyed out at the beginning ...)

Clicking on NEW opens a dialog box with UI elements and a text explanation. A text box (split text field: latitude:      longitude:   ), 2 sliders and OK button below the text field. The explanation  reads: Click on the map to select a location, select a radius and a number of quakes within it, then click OK to start.

Once clicked a star is dropped on the map and the lat/long of the location is shown in the 2 text fields. (Note: if user location is tracked by browser, the location (star, lat/lng would default to it)

The first slider (radius) defaults to 70 km (range 20 - 100 in km steps). The second slider ranges from 10 to 100 (default 20).

Bob leaves both sliders at default and then clicks on OK. Some magic happens ....

Details/ideas for later: 
- use km or miles dependent on localization or user preference?
- if location is known, show a very zoomed out map around it by default. Or: define initial map by localization?
- Maybe make lat/long active input fields, update the star?
- Its possible that there are less than the requested number of quakes within the requested radius. Inform user?
- optional feature (if possible): add place search functionality  


2) Map result and optional statistics page
The map is populated by 20 dots around the star. Each dot shows a data and a magnitude, the largest magnitude is highlighted (color?)
(Note: map should zoom out to the requested radius!)

Clicking on a quake shows additional details (date, depth, etc.) as a pop-up box

In addition, Bob sees 2 new buttons (STATS and URL) with another explanation: CLick STATS to see additional statistics about these quakes. Click URL to copy the URL for the current map to the clipboard. Bob clicks on STAT and is show a table and a plot (instead of current map or in pop-up dialog or on separate page?)

3) Refinement
Bob decides to refine his input. He changes the radius to 100 km, the quake number to 100 and again clicks on OK. The map changes accordingly.

4) Get "current" URL
Bob clicks on the URL button, then opens a email to his friend and pastes the URL into it. With the URL, his friend will see the same quake map.

--------------------------------------------------------------------

### Technical "flow" (3 pts)
- Now that you've described the user tasks, you should look at the flow from a more technical side. Strictly speaking this goes deeper that a high-level spec would typically require, but I think it's a valuable exercise to go through before beginning to code!  
- Depending on your programming experience, this may be tricky for you ... as usual, just do your best, I will reward demonstrated effort.  
- I find it best to think in terms of ___data flow___ (i.e. input/output) but if you know OOP and plan to use it, you might do a bit of early class design here instead
- Describe the overall “flow” of data, either with words (see example) and/or by creating a simple diagram on paper, with PowerPoint or with an online drawing app such as https://app.diagrams.net/ If you do it on paper, just hand in a snapshot of it.
- Jot down what blocks you think you’ll need and maybe try to group them into larger blocks.
- Name the blocks by what they do (this will help with names for classes/functions/modules later!)
- Use arrows to show which blocks need to generate/receive/exchange data (flow)
- Separately jot down the types of the data in that flow (list, dictionary, array, compounds, classes?)
- Note which blocks involve user interaction and of what kind (input? Output?)



------------------------------------------------------------------
- All quake data will be requested in real time from USGS query portal: http://earthquake.usgs.gov/fdsnws/event/1/query
- User input (lat/long, radius, max number of quakes) will be used as part of the query. Each time the user input changes a new query is performed
- query will return a csv file (save as temp file or keep a stream buffer)
- each quake (row) will have a date, lat, long and magnitude (maybe also depth?)
- quakes in the csv file will already be sorted by magnitude (part of the query)
- each quake will be plotted on a basemap using folium, using size, symbol and color
- at a minimum, hardcoded (simulated) user input must result in a static web map (see main_test_for_v1.py)

- Version 2 will be implemented as a web app using Flask
- (Somewhat) unknowns:
    - what will the GUI workflow be?
    - where/how will the statistics plot be shown? (separate page or side-by-side with the web map?) 
------------------------------------------------------------
