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
	complete: function(results) {
		console.log("parseFile:", results.data);
		parseAuthors(results);
		}
});

function parseAuthors(results){
	var authors = "";
	var data = results.data;
	for (var i = 0; i < data.length; i++) {
    	authors += data[i][4];
		if( i != data.length-1) {
			authors += '\n'
		}
	}
	console.log("parseAuthors_string:", authors);
	papa.parse(authors, {
		delimiter: ";",
		encoding: "utf-8",
		complete: function(results_a) {
			console.log("parseAuthors:", results_a.data);
			parseCollabs(results, results_a);
			}
	});
}

function parseCollabs(results, results_a){
	var authors = "";
	var data = results.data;
	for (var i = 0; i < data.length; i++) {
    	authors += data[i][8];
		if( i != data.length-1) {
			authors += '\n'
		}
	}
	console.log("parseCollabs_string:", authors);
	papa.parse(authors, {
		delimiter: ";",
		encoding: "utf-8",
		complete: function(results_c) {
			console.log("parseCollabs:", results_c.data);
			readyToRender(results, results_a, results_c);
			}
	});
}


function readyToRender(results, results_a, results_c) {
	// Render frontpage
	app.get('/', function (req, res) {
		res.render('portada',{
			data: results.data,
			authors: results_a.data,
			collabs: results_c.data
		});
	});
}

app.use(express.static('.'));

app.listen(3000, function () {
	console.log('Example app listening on port 3000!');
});
