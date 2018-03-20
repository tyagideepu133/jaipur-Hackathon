import { Injectable } from "@angular/core";
import { Http, Response } from '@angular/http';
import { Headers, RequestOptions } from '@angular/http';
import 'rxjs/add/operator/map';
import * as io from 'socket.io-client';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/toPromise';
/**
 * @description
 * @class
 */
@Injectable()
export class FlaskService {
  private socket;
  private location_url = 'http://localhost:5000/socket/location';
  private emergency_alarm = 'http://localhost:5000/api/emergency'
  constructor(private http:Http) {
    this.socket = io(this.location_url); 
  }
  getLocation(){
    let observable = new Observable(observer => {
      this.socket.on('location', (data) => {
        observer.next(data);    
      }); 
    })     
    return observable;
  }
  getEmergency(){
    let observable = new Observable(observer => {
      this.socket.on('emergency', (data) => {
        observer.next(data);    
      }); 
    })     
    return observable;
  }
  
  disconnectSocketLocation(){
    this.socket.disconnect();
  }
  getVictimCar(){
    let observable = new Observable(observer => {
      this.socket.on('emergency_needed', (data) => {
        observer.next(data);    
      }); 
    })     
    return observable;
  }
  sendEmergency(json){
    let data = JSON.stringify(json)
    let headers = new Headers({ 'Content-Type': 'application/json' });
    let options = new RequestOptions({ headers: headers });
    return this.http.post(this.emergency_alarm,data,options).toPromise()
  }
}
