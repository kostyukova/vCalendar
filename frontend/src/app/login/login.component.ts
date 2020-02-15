import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { first } from 'rxjs/operators';
import { AlertService } from '../alert/alert.service';
import { AuthenticationService } from '../_services/authentication.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  loginForm: FormGroup;
  returnRoute;

  constructor(
    private formBuilder: FormBuilder, private route: ActivatedRoute, private router: Router,
    private authService: AuthenticationService, private alertService: AlertService) { }

  ngOnInit() {
    this.loginForm = this.formBuilder.group({
      username: [null, Validators.required],
      password: [null, Validators.required]
    });
    this.returnRoute = this.route.snapshot.queryParams['returnUrl'] || '/';
  }

  onSubmit($event: any): void {
    // break if form is invalid
    if (this.loginForm.invalid) {
      return;
    }

    const username = this.loginForm.controls.username.value;
    const password = this.loginForm.controls.password.value;
    this.authService.login(username, password)
      .pipe(first())
      .subscribe(
        () => this.router.navigate([this.returnRoute]),
        error => this.alertService.error(error.message)
      );
  }
}
