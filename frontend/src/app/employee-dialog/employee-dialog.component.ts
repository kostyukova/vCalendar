import { Component, OnInit, Optional, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { Employee } from '../api_client/model/employee';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-employee-dialog',
  templateUrl: './employee-dialog.component.html',
  styleUrls: ['./employee-dialog.component.css']
})
export class EmployeeDialogComponent {

  dataForm: FormGroup;

  constructor(
    private formBuilder: FormBuilder,
    public dialogRef: MatDialogRef<EmployeeDialogComponent>,
    @Optional() @Inject(MAT_DIALOG_DATA) public data: Employee | any) {

    console.log(data);
    this.dataForm = this.formBuilder.group({
      full_name: [data.full_name, Validators.required],
      position: [data.position, Validators.required],
      specialization: [data.specialization, null],
      action: [data.action, null]
    });
  }

  get positions() {
    return Employee.PositionEnum;
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
