const { execSync } = require('child_process')
const express = require('express')
const fs = require('fs')
const app = express()

app.get('/pdf/:url/:name', (req, res) => {
  execSync(`npx electron-pdf  ${req.params.url} out.pdf`)
  res.send(fs.readFileSync(`${__dirname}/out.pdf`))
})

app.listen(8080, () => console.info('Ready on port 8080'))
