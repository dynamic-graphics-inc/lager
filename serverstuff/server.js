// Import packages
const express = require('express')
const morgan = require('morgan')
// App
const app = express()
// Morgan
app.use(morgan('tiny'))
// First route
app.get('/', (req, res) => {
    res.json({ message: 'Hello world' })
})
app.all('/pood*', (request, response) =>{
    console.log(request.originalUrl);
    // console.log(response);
    const reqPath = request.originalUrl;
    const n = reqPath.replace('/pood/', '');
    response.json({message: parseInt(n)*2})
})
// Starting server
app.listen('3001')