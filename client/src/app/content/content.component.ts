import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { timeout, catchError, count } from 'rxjs/operators';
import { WaveSurfer } from './wavesurfer.js'

@Component({
  selector: 'app-content',
  templateUrl: './content.component.html',
  styleUrls: ['./content.component.css']
})
export class ContentComponent implements OnInit {


  headers = new HttpHeaders();
  baseURL = 'http://localhost:3000';
  frontendURl = 'http://localhost:4000';
  private JSObject: Object = Object;
  mysrc = ""

  filelist = []
  currentlist = []
  fileno : any = 0;
  counter : number;


  isActive = false;
  isPlayerVisible = false;
  isLowerDivActive = false;
  isDisabled = false;
  currentInput = ""
  filename = "No File Selected"
  ranNumber: 0
  sequence: 0
  bpm: 0

  localUrl: any;
  filepath: string;
  file: any;

  
  testfunction() {
    let options = { headers: this.headers, withCredentials: true };
    this.http.get(this.baseURL + "/test", options).subscribe(res => {

      console.log("response:" + JSON.stringify(res));
      

    }, error => {
      console.log("error:" + JSON.stringify(error));
    })
  }
  



  myFunc() {
    this.counter++;
    localStorage.setItem('fileno',this.counter.toString()); //save the increased counter

    this.isPlayerVisible = false;
    this.isLowerDivActive = true;
    this.isDisabled = true;
    this.isActive = true;

    let req = {}  //used for sending data to server
    req['number'] = this.ranNumber
    req['sequence'] = this.sequence
    req['bpm'] = this.bpm
    req['num'] = 1;
    req['counter'] = this.counter
    console.log("Count: "+this.counter)

    console.log("num: ", this.ranNumber)

    let options = { headers: this.headers, withCredentials: true };

    this.http.post(this.baseURL + "/name", req, options)
      .pipe(timeout(300000))
      .subscribe(res => {

        console.log("File generated")
        console.log(JSON.stringify(res));  //server response

        this.isActive = false
        this.isDisabled = false
        this.isPlayerVisible = true;
        this.mysrc = "../../assets/Music/genMusic"+this.counter+".wav";
        
        if(localStorage.getItem('Filelist')){

          this.currentlist = JSON.parse(localStorage.getItem('Filelist'))

          this.filelist = this.currentlist
          this.filelist.push(this.mysrc)

          console.log("Current List : "+JSON.stringify(this.currentlist))

          console.log("Total List : "+ JSON.stringify(this.filelist))

          localStorage.setItem('Filelist',JSON.stringify(this.filelist));

        }else{
          this.filelist.push(this.mysrc)
          localStorage.setItem('Filelist',JSON.stringify(this.filelist));
        }


      }, error => {
        this.isActive = false
        this.isDisabled = false
        console.log(JSON.stringify(error))
      })
  }


  constructor(private http : HttpClient) {

  //   var wavesurfer = WaveSurfer.create({
  //     container: '#waveform',
  //     waveColor: 'violet',
  //     progressColor: 'purple'
  // });
  
  // wavesurfer.load('../../assets/Music/genMusic12.wav');

    this.headers.append('Access-Control-Allow-Headers', 'Content-Type,Origin');
    this.headers.append('Access-Control-Allow-Methods', 'POST, GET, OPTIONS');
    this.headers.append('Access-Control-Allow-Origin', '*');

    if(localStorage.getItem('fileno')){
      this.counter = parseInt(localStorage.getItem('fileno'));
      
    }else{
      localStorage.setItem('fileno',"1")
    }

   }

  ngOnInit() {
  }

  

}
