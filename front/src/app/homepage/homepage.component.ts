import { Component } from '@angular/core';

import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatToolbarModule } from '@angular/material/toolbar';
import { RouterOutlet } from '@angular/router';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatListModule } from '@angular/material/list';
import { Router } from '@angular/router';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-homepage',
  imports: [
    RouterOutlet,
    MatIconModule,
    MatButtonModule,
    MatToolbarModule,
    MatSidenavModule,
    MatListModule,
    RouterLink,
  ],
  templateUrl: './homepage.component.html',
  styleUrl: './homepage.component.css',
})
export class HomepageComponent {}
