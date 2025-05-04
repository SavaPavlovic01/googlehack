import { NgModule } from '@angular/core'; // Import NgModule correctly
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module'; // Import your routing module
import { AppComponent } from './app.component'; // Import your root component
import { HomepageComponent } from './homepage/homepage.component';
import { Page1Component } from './page1/page1.component';
import { Page2Component } from './page2/page2.component';
import { NavbarComponent } from './navbar/navbar.component';
import { MatListModule } from '@angular/material/list';
import { ReportComponent } from './report/report.component';
import { RouterModule } from '@angular/router';

import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { HttpClient, HttpClientModule } from '@angular/common/http';
@NgModule({
  declarations: [
    AppComponent, // Declare your root component
    HomepageComponent,
    Page1Component,
    Page2Component,
    NavbarComponent,
    ReportComponent,
    // other components go here
  ],
  imports: [
    BrowserModule, // BrowserModule must be imported
    AppRoutingModule, // Your App Routing Module
    MatListModule,
    RouterModule,
    BrowserAnimationsModule,
    FormsModule,
    ReactiveFormsModule,
    MatCheckboxModule,
    MatInputModule,
    MatButtonModule,
    MatFormFieldModule,
    HttpClient,
    // other modules go here
  ],
  providers: [],
  bootstrap: [AppComponent], // Set the bootstrap component
})
export class AppModule {}
