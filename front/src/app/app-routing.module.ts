import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomepageComponent } from './homepage/homepage.component'; // Replace with your actual component paths
import { Page2Component } from './page2/page2.component'; // Replace with your actual component paths
import { Page1Component } from './page1/page1.component'; // Replace with your actual component paths

const routes: Routes = [
  { path: '', redirectTo: '/homepage', pathMatch: 'full' },
  { path: '/page1', component: Page1Component },
  { path: '/page2', component: Page2Component },
  { path: '/homepage', component: HomepageComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
