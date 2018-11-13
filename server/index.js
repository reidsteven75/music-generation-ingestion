const express = require('express')
const app = express()
const port = 3000

app.get('/', (req, res) => res.send('working'))

app.post('/pointcloud', (req, res) => {
    console.log("POST:pointcloud");
    res.send('success');
})

app.listen(port, () => console.log(`Example app listening on port ${port}!`))