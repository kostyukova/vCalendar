import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { Component } from '@angular/core';
import { Observable } from 'rxjs';
import { map, shareReplay } from 'rxjs/operators';

@Component({
  selector: 'app-navigation',
  templateUrl: './navigation.component.html',
  styleUrls: ['./navigation.component.css']
})
export class NavigationComponent {
  routes = [
    { url: 'home', linkName: 'Home' },
    { url: 'calendar', linkName: 'Calendars' },
    { url: 'employee-list', linkName: 'Employees' },
    { url: 'user-list', linkName: 'Users' },
    { url: 'address-form', linkName: 'Sample address form' },
    { url: 'table', linkName: 'Sample table' },
    { url: 'dashboard', linkName: 'Sample dashboard' }
  ];

  isHandset$: Observable<boolean> = this.breakpointObserver.observe(Breakpoints.Handset)
    .pipe(
      map(result => result.matches),
      shareReplay()
    );

  constructor(private breakpointObserver: BreakpointObserver) { }

}
