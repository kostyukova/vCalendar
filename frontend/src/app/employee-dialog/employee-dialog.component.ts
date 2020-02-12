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

    this.dataForm = this.formBuilder.group({
      employee_id: [data.employee_id, null],
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
    const specValue = this.dataForm.controls.specialization.value;
    const employee = {
      employee_id: this.dataForm.controls.employee_id.value,
      full_name: this.dataForm.controls.full_name.value,
      position: this.dataForm.controls.position.value,
      specialization: specValue ? specValue : '',
      team_id: parseInt(this.dataForm.controls.team_id.value, 10),
      expert: !!this.dataForm.controls.expert.value,
      email: this.dataForm.controls.email.value
    };
    this.dialogRef.close({ event: this.dataForm.controls.action.value, data: employee });
  }

  closeDialog() {
    this.dialogRef.close({ event: 'Cancel' });
  }
}
