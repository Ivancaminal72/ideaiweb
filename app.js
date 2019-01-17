var express = require('express');
var app = express();
const fs = require('fs');
var papa = require('papaparse');
const file = fs.createReadStream('/home/ivan/Dropbox/1-Work/ideai/databases/PRP.csv', {encoding: "utf8"});

// Configure jade to be our rendering engine
app.set('view engine', 'jade');
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
		data[i][field] = result.data.flat();
	}
	return data;
}

function readyToRender(results) {
	// Render frontpage
	app.get('/', function (req, res) {
		res.render('portada',{
			data: results.data
		});
	});
}

app.use(express.static('.'));

app.listen(3000, function () {
	console.log('Example app listening on port 3000!');
});
