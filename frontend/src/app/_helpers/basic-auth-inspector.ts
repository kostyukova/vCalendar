import { Injectable } from '@angular/core';
import { HttpRequest, HttpHandler, HttpEvent, HttpInterceptor } from '@angular/common/http';
import { Observable } from 'rxjs';

import { AuthenticationService } from '../_services/authentication.service';
import { CurrentUser } from '../_model/current-user';

@Injectable()
export class BasicAuthInspector implements HttpInterceptor {

    constructor(private authenticationService: AuthenticationService) { }

    intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
        // add authorization header with basic auth credentials if available
        const currentUser: CurrentUser = this.authenticationService.currentUser;
        if (currentUser && currentUser.token) {
            request = request.clone({
                setHeaders: {
                    Authorization: `Bearer: ${currentUser.token}`
                }
            });
        }

        return next.handle(request);
    }
}
