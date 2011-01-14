
/**
 * Module dependencies.
 */

var express = require('express');
var spawn = require('child_process').spawn;

var app = module.exports = express.createServer();

// Configuration

app.configure(function(){
  app.set('views', __dirname + '/views');
  app.set('view engine', 'jade');
  app.use(express.bodyDecoder());
  app.use(express.methodOverride());
  app.use(app.router);
  app.use(express.staticProvider(__dirname + '/public'));
});

app.configure('development', function(){
  app.use(express.errorHandler({ dumpExceptions: true, showStack: true })); 
});

app.configure('production', function(){
  app.use(express.errorHandler()); 
});

// Routes

app.get('/', function(req, res){
  res.render('index', {
      title: 'Express'
  });
});


// Todo:  Create an upload form instead of specifying a file here
app.get('/test', function(req, res) {
	var script = spawn('python',['scripts/script.py','input/input.gpx']);

	script.stdout.on('data', function (data) {
		res.send(data, {'Content-Type': 'text/plain'}, 200);
	});

	script.stderr.on('data', function (data) {
		console.log("Error from python script: " + data);
	});

	script.on('exit', function (code) {
		console.log("child process exited with code " + code);
	});

});

// Only listen on $ node app.js

if (!module.parent) {
  app.listen(3713);
  console.log("Express server listening on port %d", app.address().port)
}
