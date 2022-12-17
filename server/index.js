const express = require('express')
var path = require('path');
const app = express()
const port = 80

app.get('/latest-html', (req, res) => {
    var fileName = `/srv/bot/cron/tmp/latest-html.html`;
    console.log(fileName)
    res.download(fileName);
})

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})

