import { Component, Inject } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { Observable, of } from 'rxjs';
import { catchError, debounceTime, flatMap, startWith } from 'rxjs/operators';
import { AlertService } from '../alert/alert.service';
import { EmployeeService } from '../api_client/api/employee.service';
import { Employee } from '../api_client/model/employee';
import { DialogData } from './calendar.component';


@Component({
  selector: 'app-calendar-event-dialog',
  templateUrl: 'calendar-event-dialog.html',
})
export class CalendarEventDialogComponent {
  dataForm: FormGroup;
  filteredEmployees: Observable<Employee[]>;

  constructor(
    private apiClient: EmployeeService,
    private alertService: AlertService,
    private formBuilder: FormBuilder,
    public dialogRef: MatDialogRef<CalendarEventDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData) {
    this.dataForm = this.formBuilder.group({
      action: [data.action, null],
      event: [data.event, null],
      id: [data.event.meta ? data.event.meta.id : null, null],
      employee: [null, [Validators.required, this.validateEmployee]],
      leave_days: [data.event.meta ? data.event.meta.leave_days : null, [Validators.required, Validators.pattern('[1-9][0-9]?')]],
      start_date: [data.event.meta ? data.event.meta.start_date : null, Validators.required],
      end_date: [data.event.meta ? data.event.meta.end_date : null, Validators.required]
    });
    this.filteredEmployees = this.dataForm.get('employee').valueChanges
      .pipe(
        debounceTime(300),
        startWith(''),
        flatMap(value => value ? this.filterEmployees(value) : of([]))
      );
    if (data.event.meta && data.event.meta.employee_id) {
      this.apiClient.getEmployeeById(data.event.meta.employee_id).subscribe(
        employee => this.dataForm.controls.employee.setValue(employee),
        error => this.alertService.error(error.mesage)
      );
    }
  }

  doAction() {
    if (this.dataForm.invalid) {
      return;
    }
    const leaveDays = {
      id: this.dataForm.controls.id.value,
      employee: this.dataForm.controls.employee.value,
      leave_days: parseInt(this.dataForm.controls.leave_days.value, 10),
      start_date: this.dataForm.controls.start_date.value,
      end_date: this.dataForm.controls.end_date.value
    };
    this.dialogRef.close({ event: this.dataForm.controls.action.value, data: leaveDays });
  }

  closeDialog(): void {
    this.dialogRef.close({ event: 'Cancel' });
  }

  displayWith(employee: Employee) {
    return employee && employee.full_name ? employee.full_name : '';
  }

  validateEmployee(control: FormControl) {
    if (!control.value) {
      return null;
    }
    const selection: any = control.value;
    return typeof selection === 'object' ? null : {
      notselected: {
        valid: false
      }
    };
  }

  private filterEmployees(value: string): Observable<Employee[]> {
    return this.apiClient.findEmployeesBy(value).pipe(
      catchError(() => of([]))
    );
  }

}
