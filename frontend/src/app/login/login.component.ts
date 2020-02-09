import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
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

  constructor(private formBuilder: FormBuilder, private router: Router, private authService: AuthenticationService, private alertService: AlertService) { }

  ngOnInit() {
    this.loginForm = this.formBuilder.group({
      username: [null, Validators.required],
      password: [null, Validators.required]
    });
  }

  onSubmit(): void {
    const username = this.loginForm.controls.username.value;
    const password = this.loginForm.controls.password.value;

    // break if form is invalid
    if (this.loginForm.invalid) {
      return;
    }

    this.authService.login(username, password)
      .pipe(first())
      .subscribe(
        data => {
          this.router.navigate(['home']);
        },
        error => {
          if (error.error && error.error.message) {
            this.alertService.error(error.error.message);
          }
          console.error(error);
        });
  }
}
