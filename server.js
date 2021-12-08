const https = require('https');
const fs = require('fs');
var http = require('http');
const express = require("express");
const bodyParser = require("body-parser");

const app = express();

// parse requests of content-type - application/json
app.use(bodyParser.json());

// parse requests of content-type - application/x-www-form-urlencoded
app.use(bodyParser.urlencoded({ extended: true }));

// simple route
app.get("/", (req, res) => {
  res.json({ message: "API Active ." });
});

require("./app/routes/customer.routes.js")(app);

var options = {
	key: fs.readFileSync('ssl key file'),
	cert: fs.readFileSync('ssl cert file')
}

const httpsServer = https.createServer(options, app);
httpsServer.listen("port number specified",'ipaddress')