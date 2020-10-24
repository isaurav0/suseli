const express = require('express');
const morgan = require('morgan');
const bodyParser = require('body-parser');
const path = require('path');
const fs = require('fs');

const app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended:false}));
app.use(morgan('combined'));
app.use(express.static('build'));
app.use(express.static('data'))

const PORT = 8081 
//run server 
app.listen(PORT, ()=>{
    console.log("server start on port http://localhost:"+ PORT);
})

app.get("/",(req, res)=>{
	return res.sendFile(__dirname + '/build/index.html')
})

app.route('/api/auth', require('./routes/api/auth/auth'))

app.get('/api/songs/:id/stream', (req, res)=>{

	const file = path.join(__dirname, `data/audio/${req.params["id"]}.mp3`)

	if(!fs.existsSync(file))
		return res.status(404).send('file not found')

	const stat = fs.statSync(file);
	const total = stat.size;
	const range = req.headers.range ? req.headers.range: '0';
	const parts = range.replace(/bytes=/, '').split('-');
	const partialStart = parts[0];
	const partialEnd = parts[1];

	const start = parseInt(partialStart, 10);
	const end = partialEnd ? parseInt(partialEnd, 10) : total - 1;
	// const chunksize = (end - start) + 1;
	const chunksize = 160*1024*8;
	const rstream = fs.createReadStream(file, {start: start, end: end});

	res.writeHead(206, {
		'Content-Range': 'bytes ' + start + '-' + end + '/' + total,
		'Accept-Ranges': 'bytes', 'Content-Length': chunksize,
		'Content-Type': 'audio/mpeg'
	});
	rstream.pipe(res);
})

app.get('/api/songs/download', (req, res)=>{
	const file = path.join(__dirname, 'data/audio/1.mp3')
	res.sendFile(file)
})