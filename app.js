var express = require('express');
var app = express();
const fs = require('fs');
var papa = require('papaparse');
const file = fs.createReadStream('./databases/csv/PAP_all_summary.csv', {encoding: "utf8"});

// Configure pug to be our rendering engine
app.set('view engine', 'pug');
app.set('views', __dirname + '/views');

// Our CSS and JS files
app.use("/pub",express.static('public'));

papa.parse(file, {
	encoding: "utf-8",
	header: true,
	complete: async function(results) {
		console.log("parseFile_errors:", results.errors);
		console.log("parseFile_meta:", results.meta);
		//console.log(results.data)
		results.data = await parseField(results.data, "Authors", ";");
		results.data = await parseField(results.data, "PAuthors", ";");
		results.data = await parseField(results.data, "SAuthors", ";");
		results.data = await parseField(results.data, "Collaborators", ";");
		results.data = await parseField(results.data, "SAreas", ",");
		readyToRender(results);
		}
});

async function parseField(data, field, dl){
	for (var i = 0; i < data.length; i++) {
		var result = papa.parse(data[i][field], {
			delimiter: dl,
			encoding: "utf-8",
			complete: function(results) {
				if(results.errors.length != 0){
					console.log("parse_errors:", results.errors);
					console.log("parse_meta:", results.meta);
					}
				}
			});
		data[i][field] = [].concat.apply([], result.data);
	}
	return data;
}

function readyToRender(results) {
	var areas = ["Digital Society", "Wellness",  "Education", "Industry 4.0", "Economy", "Innovation", "Efficient Resources", "ethics", "Talent"];
	var areaRoutes = ["digital", "health-inclusion-wellness", "education", "industry", "economy", "innovation", "resources", "ethics", "talent"];

	app.get('/areas/:area', function (req, res) {
		var areaReq = req.params["area"];
		if(areaRoutes.includes(areaReq)) {
			var idx = areaRoutes.indexOf(areaReq);
			var areaReqTitle = areas[idx];
			var request = "area"

			// Render areas
			res.render('portada',{
				request,
				data: results.data,
				areas,
				areaRoutes,
				areaReq,
				areaReqTitle
				});
		}
		else {

		}
	});

	app.get('/projects', function (req, res) {
		var request = "projects"

		// Render projects
		res.render('portada',{
			request,
			data: results.data,
			areas,
			areaRoutes
		});
	});
}

app.use(express.static('.'));

app.listen(3000, function () {
	console.log('Example app listening on port 3000!');
});
