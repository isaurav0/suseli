const express = require('express')
const router = express.Router()

router.get('/', (req, res)=>{
    console.log('hello')
    res.send("Hello")
    // res.sendFile('../../../data/1.mp3')
})

module.exports = router