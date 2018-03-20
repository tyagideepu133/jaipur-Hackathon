import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { HttpModule } from "@angular/http";

import { AppRoutingModule } from "./app-routing.module";
import { AgmCoreModule } from '@agm/core';

import { AppComponent } from './app.component';
import { LoginComponent } from "./login/login.component";
import { DashboardComponent } from "./dashboard/dashboard.component";

import { FlaskService } from "./flask.service";

@NgModule({
  declarations: [
    AppComponent, LoginComponent, DashboardComponent
  ],
  imports: [
    BrowserModule, AppRoutingModule,AgmCoreModule.forRoot({
      apiKey: 'AIzaSyAcXrL1ag0b0f0CW5rQ_dGyh5ZhsMNTUc0'
    }),HttpModule
  ],
  providers: [FlaskService],
  bootstrap: [AppComponent]
})
export class AppModule { }
