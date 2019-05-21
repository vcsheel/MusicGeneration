import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-samples',
  templateUrl: './samples.component.html',
  styleUrls: ['./samples.component.css']
})
export class SamplesComponent implements OnInit {

  currentlist = []

  constructor() {
    this.currentlist = JSON.parse(localStorage.getItem('Filelist'))
    console.log(JSON.stringify(this.currentlist))
   }

  ngOnInit() {
  }

}
