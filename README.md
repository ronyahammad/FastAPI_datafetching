Introduction:

This fastAPI app has been created to store live data of weather. The place i have selectd to store weather data is:

	Longitude: 7.921066 
	Latitude: 36.9898 

The API points of the app are:

	1) https://historic-weather-data.onrender.com/docs: 
 		swagger-UI frontend to show the points.
 	2) https://historic-weather-data.onrender.com/fetch-weather-data: 
		This API point is the GET method to fetch the data from open-meteo.com API
	3) https://historic-weather-data.onrender.com/get-weather-data: 
 		This API point is the GET method to get the data sored in the database in Firebase Firestore

Fetching the data from open-meteo.com API every hour, i used cron-job.org for task schedule. This firebase database will be acting like one of the sources for a predicting model and is actually part of my masters thesis.

The App has been deployed in render.com in free tier. it is under constant development process
