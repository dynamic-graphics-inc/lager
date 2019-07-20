const https = require('http')



for (let i = 1; i < 10; i ++){


const options = {
  hostname: 'localhost',
  port: 3001,
  path: '/pood/' + i,
  method: 'GET'
}
const req = https.request(options, (res) => {
  console.log(`statusCode: ${res.statusCode}`)

  res.on('data', (d) => {
    process.stdout.write(d)
  })
})

req.on('error', (error) => {
  console.error(error)
})

req.end()
}