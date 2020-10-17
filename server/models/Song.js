const mongoose = require("mongoose");

const SongSchema = mongoose.Schema({
    title: {
        type: String
    },
    song_url: {
        type: String,
        unique: true,
        required: true
    },
    release_date{
        type: String
    },
    thumbnail_url: {
        type: String
    },
    artist: {
        type: String
    }
})