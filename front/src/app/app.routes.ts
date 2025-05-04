import { Routes } from '@angular/router';
import { HomepageComponent } from './homepage/homepage.component';
import { Page1Component } from './page1/page1.component';
import { Page2Component } from './page2/page2.component';
import { ReportComponent } from './report/report.component';

export const routes: Routes = [
  { path: '', redirectTo: '/homepage', pathMatch: 'full' },
  { path: 'homepage', component: HomepageComponent },
  { path: 'page1', component: Page1Component },
  { path: 'page2', component: Page2Component },
  { path: 'report', component: ReportComponent },
];
