import { Injectable } from '@angular/core';
import { BehaviorSubject, of, Observable } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { UserService } from '../api_client/api/user.service';
import { CurrentUser } from '../_model/current-user';

@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {
  private currentUserSubject: BehaviorSubject<CurrentUser>;

  constructor(private apiClient: UserService) {
    this.currentUserSubject = new BehaviorSubject(JSON.parse(localStorage.getItem('currentUser')));
  }

  public get currentUser(): CurrentUser {
    return this.currentUserSubject.value;
  }

  login(username: string, password: string): Observable<CurrentUser> {
    return this.apiClient.authenticateUser(username, password)
    .pipe(map(token => {
        const user = new CurrentUser(username, null, token);
        localStorage.setItem('currentUser', JSON.stringify(user));
        this.currentUserSubject.next(user);
        return user;
      }));
  }

  logout() {
    // remove user from local storage to log user out
    localStorage.removeItem('currentUser');
    this.currentUserSubject.next(null);
  }
}
