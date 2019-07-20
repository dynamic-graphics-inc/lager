var app = require('express')();
var server = require('http')(app);
var io = require('socket.io')(server);
var fs = require('fs');



app.get('/', (req, res) => {
    res.sendFile(__dirname+'/index.html')
});

io.on('connection', (sock) => {
    fs.readFile(__dirname+'/logs.json', {encoding: 'json'}, (err, data) => {
        if (!err) console.log(err)
        else {
            console.log(data);
        }
    } )
    // sock.emit('sup', {sup: 'sup'})
})
