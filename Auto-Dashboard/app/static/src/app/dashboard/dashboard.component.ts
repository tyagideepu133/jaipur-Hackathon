import { Component, OnInit, ViewChild, ElementRef } from "@angular/core";
import { FlaskService } from "../flask.service";

@Component({
  selector: "app-dashboard",
  templateUrl: "./dashboard.component.html",
  styleUrls: ["./dashboard.component.css"]
})

export class DashboardComponent implements OnInit {

  ec_lat:any
  ec_lon:any
  ec_number:any
  ec_id:any
  lat: number = 22;
  lng: number = 77;
  markers = []
  my_lat: number
  my_lng: number
  emergency_switch:boolean = false
  victims = []
  show_victims:boolean = false
  show_markers:boolean = false
  constructor(private elementRef: ElementRef, private flaskService: FlaskService) {

  }

  ngOnInit() {
    this.flaskService.getLocation().subscribe((location: any) => {
      this.my_lat = location.lat
      this.my_lng = location.lon
      this.lat = location.lat
      this.lng = location.lon
      // console.log(location)
    })
    this.flaskService.getEmergency().subscribe((emergency: any) => {
      // this.markers = emergency.map
      if (emergency.length) {
        this.show_markers = true
        for (let i = 0; i < emergency.length; i++) {
          let final_emergency = emergency[i]
          final_emergency.car_lat = parseFloat(emergency[i].car_lat)
          final_emergency.car_lon = parseFloat(emergency[i].car_lon)
          this.markers[i] = final_emergency
        }
      }
      else{
        this.markers = []
      }
    })
    this.flaskService.getVictimCar().subscribe((emergency:any)=>{
      console.log(emergency)
      if (emergency.length) {
        this.show_victims = true
        for (let i = 0; i < emergency.length; i++) {
          let final_emergency = emergency[i]
          final_emergency.vc_current_lat = parseFloat(emergency[i].vc_current_lat)
          final_emergency.vc_current_lon = parseFloat(emergency[i].vc_current_lon)
          final_emergency.ec_current_lat = parseFloat(emergency[i].ec_current_lat)
          final_emergency.ec_current_lon = parseFloat(emergency[i].ec_current_lon)
          this.victims[i] = final_emergency
        }
      }
      else{
        this.victims = []
      }
    })
  }

  markerClicked(lat,lon,number,id) {
    this.ec_lat = lat
    this.ec_lon = lon
    this.ec_number = number
    this.ec_id = id
    var modalButton = document.getElementById("modalLauncher");
    modalButton.click();
  }
  disconnectServer() {
    this.flaskService.disconnectSocketLocation()
    window.top.close()
  }
  needEmergency(){
    let data = {
      "car_lat":this.ec_lat,
      "car_lon":this.ec_lon,
      "car_number":this.ec_number,
      "car_driver_id":this.ec_id
    }
    this.flaskService.sendEmergency(data).then(
      (data)=>{
        console.log(data)
      }
    ).catch((err)=>{
      console.log(err)
    })
    this.emergency_switch = true
  }
}
