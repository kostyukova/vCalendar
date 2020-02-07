import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthenticationService } from '../_services/authentication.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { first } from 'rxjs/operators';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  loginForm: FormGroup;
  error = '';

  constructor(private formBuilder: FormBuilder, private router: Router, private authService: AuthenticationService) { }

  ngOnInit() {
    this.loginForm = this.formBuilder.group({
      username: [null, Validators.required],
      password: [null, Validators.required]
    });
  }

  onSubmit(): void {
    const username = this.loginForm.controls.username.value;
    const password = this.loginForm.controls.password.value;

    // stop here if form is invalid
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
          // FiXME error message to user
          this.error = error;
          console.error(error);
        });
  }
}
