const express = require('express');
const morgan = require('morgan');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended:false}));
app.use(morgan('combined'));
app.use(express.static('build'));

const PORT = 8081 
//run server 
app.listen(PORT, ()=>{
	console.log("server start on port "+ PORT)
})

app.get("*",(req, res)=>{
	return res.sendFile(__dirname + '/build/index.html')
})
