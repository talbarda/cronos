/**
 * Module dependencies.
 */

var express = require('express')
  , routes = require('./routes')
  , user = require('./routes/user')
  , http = require('http')
  , path = require('path')
  , AWS = require('aws-sdk')
  , EmployeeProvider = require('./employeeprovider').EmployeeProvider;

var app = express();

app.configure(function(){
  app.set('port', process.env.PORT || 3000);
  app.set('views', __dirname + '/views');
  app.set('view engine', 'jade');
  app.set('view options', {layout: false});
  app.use(express.favicon());
  app.use(express.logger('dev'));
  app.use(express.bodyParser());
  app.use(express.methodOverride());
  app.use(app.router);
  app.use(require('stylus').middleware(__dirname + '/public'));
  app.use(express.static(path.join(__dirname, 'public')));
});

app.configure('development', function(){
  app.use(express.errorHandler());
});

var employeeProvider= new EmployeeProvider('localhost', 27017);

var dynamodb = new AWS.DynamoDB({region: 'us-west-2',
                                 accessKeyId: 'AKIAIV7K7XZVVE2O4HSA',
                                 secretAccessKey: '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'});

//Routes

//index
app.get('/', function(req, res){
    console.log("Got message to server");

    var epocTime = (new Date).getTime();

    console.log("---------------------");
    console.log('Got request on: ' + epocTime);
    console.log(req.body);
    console.log("---------------------");
    console.log("pressure: " + req.body.pressure);
    console.log("temperature: " + req.body.temperature);
    console.log("uid: " + req.body.uid);
    console.log("ts: " + req.body.ts);
    console.log("---------------------");

    var params = {
        'Item': {
            epoc : { N: epocTime.toString() },
            pressure : { N: req.body.pressure.toString()},
            temperature: { N: req.body.temperature.toString() },
            uid : { S: req.body.uid.toString() },
            ts: { S: req.body.ts.toString() }
        },
        'TableName' : 'messurments'
    };

    dynamodb.putItem(params, function(err, data) {
        if (err) console.log(err, err.stack); // an error occurred
        else     console.log(data);           // successful response
    });

    console.log("Setting message to DynamoDB");
//    console.log("Got message to server");
//    console.log("---------------------");
//    console.log(req.body);
//    console.log("---------------------");
//    console.log("pressure: " + req.body.pressure);
//    console.log("temperature: " + req.body.temperature);
//    console.log("uid: " + req.body.uid);
//    console.log("ts: " + req.body.ts);
//    console.log("---------------------");
//
    res.send(req.body);
});

    //new employee
    app.get('/putItem', function(req, res) {
        console.log("Got message to server");

        var epocTime = (new Date).getTime();

        console.log("---------------------");
        console.log('Got request on: ' + epocTime);
        console.log(req.body);
        console.log("---------------------");
        console.log("pressure: " + req.body.pressure);
        console.log("temperature: " + req.body.temperature);
        console.log("uid: " + req.body.uid);
        console.log("ts: " + req.body.ts);
        console.log("---------------------");

        var params = {
            'Item': {
                epoc : { N: epocTime.toString() },
                pressure : { N: req.body.pressure.toString()},
                temperature: { N: req.body.temperature.toString() },
                uid : { S: req.body.uid.toString() },
                ts: { S: req.body.ts.toString() }
            },
            'TableName' : 'messurments'
        };

        dynamodb.putItem(params, function(err, data) {
            if (err) console.log(err, err.stack); // an error occurred
            else     console.log(data);           // successful response
        });

        console.log("Setting message to DynamoDB");

        res.send(req.body);

    });

//new employee
app.get('/employee/new', function(req, res) {
    res.render('employee_new', {
        title: 'New Employee'
    });
});

//save new employee
app.post('/employee/new', function(req, res){
    employeeProvider.save({
        title: req.param('title'),
        name: req.param('name')
    }, function( error, docs) {
        res.redirect('/')
    });
});

//update an employee
app.get('/employee/:id/edit', function(req, res) {
	employeeProvider.findById(req.param('_id'), function(error, employee) {
		res.render('employee_edit',
		{ 
			title: employee.title,
			employee: employee
		});
	});
});

//save updated employee
app.post('/employee/:id/edit', function(req, res) {
	employeeProvider.update(req.param('_id'),{
		title: req.param('title'),
		name: req.param('name')
	}, function(error, docs) {
		res.redirect('/')
	});
});

//delete an employee
app.post('/employee/:id/delete', function(req, res) {
	employeeProvider.delete(req.param('_id'), function(error, docs) {
		res.redirect('/')
	});
});

app.listen(process.env.PORT || 3000);
