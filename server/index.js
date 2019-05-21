let {PythonShell} = require('python-shell')
const express = require('express')
const bodyParser = require('body-parser')
const multipart = require('connect-multiparty');  
const fs = require('fs');
const util = require('util');
const multipartMiddleware = multipart({  
    uploadDir: './'
});

const app = express()
const port = 3000

app.use(function (req, res, next) {
  res.header("Access-Control-Allow-Origin", "http://localhost:4000");
  res.header("Access-Control-Allow-Credentials", true);
  res.header("Access-Control-Allow-Origin: *");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  next();
});

app.use(bodyParser.json())
app.use(
  bodyParser.urlencoded({
    extended: true,
  })
)




app.get('/test', (request, response) => {
  response.status(200).json({ mydata: "hello" })

})

app.post('/testPost', (request, response) => {

  //get the data sent from front end here
  var name = request.body.name;
  var data = request.body.data;
  console.log(name + " " + data)

  var a = name + " " + data
  //send back response
  response.status(200).json({ mydata: a })

})

app.get('/audio', (request,response) => {
  var filePath = '../client/src/assets/genMusic.wav';
  var stat = fs.statSync(filePath);

  response.writeHead(200, {
    'Content-Type':'audio/mpeg',
    'Content-Length':stat.size
  });

  // var readStream = fs.createReadStream(filePath);
  // util.pump(readStream, response);

  fs.createReadStream(filePath,).pipe(response);
});

app.get('/audio12', (request,response)=>{
  const fileSize = stat.size;
  const range = request.headers.range;
  if (range) {
    const parts = range.replace(/bytes=/, "").split("-");
    const start = parseInt(parts[0], 10);
    const end = parts[1] 
      ? parseInt(parts[1], 10)
      : fileSize - 1;
    const chunksize = (end - start) + 1;
    const readStream = fs.createReadStream(filePath, { start, end });
    const head = {
      'Content-Range': `bytes ${start}-${end}/${fileSize}`,
      'Accept-Ranges': 'bytes',
      'Content-Length': chunksize,
      'Content-Type': 'video/mp4',
    };
    response.writeHead(206, head);
    readStream.pipe(response);
  } else {
    const head = {
      'Content-Length': fileSize,
      'Content-Type': 'video/mp4',
    };
    response.writeHead(200, head);
    fs.createReadStream(filePath).pipe(response);
  }
})


app.post('/name', runMain); 

app.post('/sendfile',multipartMiddleware, (req,res) => {
  runMain1(req,res);
});
  

function runPy(request){
  let op = request.body.num;
  let num = request.body.number;
  let counter = request.body.counter;
  console.log("counter : "+counter)
  let seq = request.body.sequence;
  let bpm = request.body.bpm;
  console.log("Received : "+num)
  console.log("Received: "+num+" "+" "+seq+" "+bpm)

  return new Promise(async function(resolve, reject){
        let options = {
        mode: 'text',
        pythonOptions: ['-u'],
        scriptPath: './',//Path to your script
        args: [op,num,seq,bpm,counter]//Approach to send JSON as when I tried 'json' in mode I was getting error.
       };

        await PythonShell.run('c.py', options, function (err, results) {
        //On 'results' we get list of strings of all print done in your py scripts sequentially. 
        if (err) throw err;
        console.log('results: ');
        for(let i of results){
              console.log(i, "---->")
        }
    resolve(results[1])//I returned only JSON(Stringified) out of all string I got from py script
   });
 })
} 

function runMain(request,response){
  console.log("In here")
  return new Promise(async function(resolve, reject){
      let r =  await runPy(request)
      console.log(JSON.parse(JSON.stringify(r.toString())), "Done...!@")//Approach to parse string to JSON.
      response.send({text:"done"})
    })
}



function runPy1(request){
 
  return new Promise(async function(resolve, reject){
        let options = {
        mode: 'text',
        pythonOptions: ['-u'],
        scriptPath: './',//Path to your script
        args: []//Approach to send JSON as when I tried 'json' in mode I was getting error.
       };

        await PythonShell.run('c.py', options, function (err, results) {
        //On 'results' we get list of strings of all print done in your py scripts sequentially. 
        if (err) throw err;
        console.log('results: ');
        for(let i of results){
              console.log(i, "---->")
        }
    resolve(results[1])//I returned only JSON(Stringified) out of all string I got from py script
   });
 })
} 

function runMain1(request,response){
  console.log("In here")
  return new Promise(async function(resolve, reject){
      let r =  await runPy1(request)
      console.log(JSON.parse(JSON.stringify(r.toString())), "Done...!@")//Approach to parse string to JSON.
      response.send({text:"done"})
    })
}



  //write get or post api here function here

  app.listen(port, () => {
    console.log(`App running on port ${port}.`)
  })
