import { Injectable } from '@angular/core';
import { Subject, Observable } from 'rxjs';
import { Router, NavigationStart } from '@angular/router';

export class Alert {
  constructor(
    public type: 'success' | 'error',
    public message: string,
    public details: object) { }
}

@Injectable({
  providedIn: 'root'
})
export class AlertService {
  private subject = new Subject<Alert>();

  constructor(private router: Router) {
    // clear alert message on route change
    this.router.events.subscribe(event => {
      if (event instanceof NavigationStart) {
        this.clear();
      }
    });
  }

  success(message: string, details: object = null) {
    this.subject.next(new Alert('success', message, details));
  }

  error(message: string, details: object = null) {
    this.subject.next(new Alert('error', message, details));
  }

  getMessage(): Observable<Alert> {
    return this.subject.asObservable();
  }

  clear(): void {
    this.subject.next();
  }
}
