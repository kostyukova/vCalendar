import { Component, Inject, OnInit, Optional } from '@angular/core';
import { FormBuilder, FormGroup, Validators, FormControl } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { User } from '../api_client/model/user';

@Component({
  selector: 'app-user-dialog',
  templateUrl: './user-dialog.component.html',
  styleUrls: ['./user-dialog.component.css']
})
export class UserDialogComponent implements OnInit {

  dataForm: FormGroup;

  constructor(
    private formBuilder: FormBuilder,
    private dialogRef: MatDialogRef<UserDialogComponent>,
    @Optional() @Inject(MAT_DIALOG_DATA) private data: User | any) {
    const config: {
      [key: string]: any;
    } = {
      id: [data.id, null],
      action: [data.action, null]
    };

    switch (data.action) {
      case 'Add':
        config.password = [null, [Validators.required, Validators.maxLength(20)]];
      // tslint:disable-next-line: no-switch-case-fall-through
      case 'Update':
        config.username = [data.username, [Validators.required, Validators.maxLength(20)]];
        config.email = [data.email, [Validators.required, Validators.maxLength(255)]];
        config.roles = [data.roles, null]; // FIXME roles validator
        break;
      case 'Delete':
        config.username = [data.username, [Validators.required, Validators.maxLength(20)]];
        break;
      case 'Setpass':
        config.password = [null, [Validators.required, Validators.maxLength(20)]];
        config.passconfirm = [null, [Validators.required, Validators.maxLength(20)]]; // FIXME confirm validator
        break;
    }
    this.dataForm = this.formBuilder.group(config);
  }

  ngOnInit() {
  }

  get acceptedRoles() {
    return ['read:users', 'write:users', 'write:teams', 'write:employees', 'write:total_days', 'write:leave_days'];
  }

  validateRoles(control: FormControl) {
    if (!control.value) {
      return null;
    }
    return control.value.split(',').every(
      elem => this.acceptedRoles.indexOf(elem) >= 0) ? null : {
        commaseparated: {
          valid: false
        }
      };
  }

  doAction() {
    // break if form is invalid
    if (this.dataForm.invalid) {
      return;
    }
    const user: { [key: string]: string } = {
      id: this.dataForm.controls.id.value,
      username: '',
      password: '',
      email: '',
      roles: ''
    };

    switch (this.dataForm.controls.action.value) {
      case 'Add':
        user.password = this.dataForm.controls.username.value.trim();
      // tslint:disable-next-line: no-switch-case-fall-through
      case 'Update':
        const roles = this.dataForm.controls.roles.value;
        user.username = this.dataForm.controls.username.value.trim();
        user.email = this.dataForm.controls.username.value.trim();
        user.roles = roles ? roles.trim() : '';
        break;
      case 'Delete':
        break;
      case 'Setpass':
        user.password = this.dataForm.controls.password.value.trim();
        break;
    }

    this.dialogRef.close({ event: this.dataForm.controls.action.value, data: user });
  }

  closeDialog() {
    this.dialogRef.close({ event: 'Cancel' });
  }

}
