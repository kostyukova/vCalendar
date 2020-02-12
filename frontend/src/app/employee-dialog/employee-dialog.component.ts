import { Component, OnInit, Optional, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { Employee } from '../api_client/model/employee';
import { FormBuilder, FormGroup, Validators, FormControl } from '@angular/forms';
import { Observable } from 'rxjs';
import { TeamCache } from '../_services/team-cache';

@Component({
  selector: 'app-employee-dialog',
  templateUrl: './employee-dialog.component.html',
  styleUrls: ['./employee-dialog.component.css']
})
export class EmployeeDialogComponent {

  dataForm: FormGroup;

  constructor(
    private formBuilder: FormBuilder,
    private dialogRef: MatDialogRef<EmployeeDialogComponent>,
    private teamCache: TeamCache,
    @Optional() @Inject(MAT_DIALOG_DATA) private data: Employee | any) {

    console.log(data);
    this.dataForm = this.formBuilder.group({
      full_name: [data.full_name, Validators.required],
      position: [data.position, Validators.required],
      specialization: [data.specialization, this.validateSpecialization],
      team_id: [data.team_id, Validators.required],
      expert: [data.expert, Validators.required],
      email: [data.email, [Validators.required, Validators.email]],
      action: [data.action, null]
    });
  }

  get positions() {
    return Employee.PositionEnum;
  }

  get teams(): Observable<Map<number, string>> {
    return this.teamCache.getFoundList();
  }

  validateSpecialization(control: FormControl) {
    if (!control.value) {
      return null;
    }
    const accepted = ['Core', 'BA', 'OACI', 'O365'];
    return control.value.split(',').every(elem => accepted.indexOf(elem) >= 0) ? null : {
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
    const employee = {
      full_name: this.dataForm.controls.full_name,
      position: this.dataForm.controls.position,
      specialization: this.dataForm.controls.specialization
    };
    this.dialogRef.close({ event: this.dataForm.controls.action.value, data: employee });
  }

  closeDialog() {
    this.dialogRef.close({ event: 'Cancel' });
  }
}
