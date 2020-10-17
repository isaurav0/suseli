const fs = require('fs');
const path = require('path');
const file = path.join(__dirname, 'data/file.txt')

const readStream = fs.createReadStream(file, 'utf8', { highWaterMark: 128*1024 })

readStream.on('data', (chunk)=>{    
    setTimeout(() => {
        console.log('-------------------------------')
        console.log(chunk)
    }, 1000);
})