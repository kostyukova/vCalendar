import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpHandler, HttpRequest } from '@angular/common/http';
import { AuthenticationService } from '../_services/authentication.service';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';


@Injectable()
export class ErrorInterceptor implements HttpInterceptor {
  constructor(private authenticationService: AuthenticationService) { }

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<any> {
    return next.handle(request).pipe(catchError(error => {
      console.log(error);
      // FIXME process 401 HTTP status
      // if (err.status === 401) {
      //   // auto logout if 401 response returned from api
      //   this.authenticationService.logout();
      //   location.reload(true);
      // }
      const errorObj = error.error.message ? error.error : { message: error.statusText };
      return throwError(errorObj);
    }));
  }
}
