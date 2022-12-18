const express = require('express')
var path = require('path');
const app = express()
const port = 3000
const products_all_data = require('/srv/bot/api/json/products-all.json')

app.use(function (req, res, next) {

  // Website you wish to allow to connect
  res.setHeader('Access-Control-Allow-Origin', '*');

  // Request methods you wish to allow
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE');
  next();
})

app.get('/products-all.json', (req, res) => {
  console.log("products-all.json pinged");  
  res.header("Content-Type",'application/json');
  res.send(JSON.stringify(products_all_data));
})

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})

