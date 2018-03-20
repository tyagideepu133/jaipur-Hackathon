import { Component, OnInit, AfterViewInit } from "@angular/core";
import {Router} from "@angular/router"

@Component({
  selector: "app-login",
  templateUrl: "./login.component.html",
  styleUrls: ["./login.component.css"]
})

export class LoginComponent implements OnInit,AfterViewInit {
  constructor(private router:Router) { 

  }

  ngOnInit() {
    let msg = document.getElementById("welcomeMessage");
    setTimeout(()=>{
      msg.innerText = "Please insert your card"
      this.pleaseWait(msg)
      setTimeout(()=>{
        msg.innerText = "Place your Thumb"
        this.pleaseWait(msg)
        this.successMsg(msg)
      },7000)
    }, 3000)
  }

  pleaseWait(msg) {
    setTimeout(()=>{
      msg.innerText = "Please Wait..."
    },3000)
  }

  successMsg(msg){
    setTimeout(()=>{
      msg.innerText = "Starting Dashboard"
      setTimeout(()=>{
        this.router.navigate(["dashboard"])
      },3000)
    },7000)
  }

  ngAfterViewInit(){
  }
}
