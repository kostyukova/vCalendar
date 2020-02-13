import { Component, Inject } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { DialogData } from './calendar.component';


@Component({
  selector: 'app-calendar-event-dialog',
  templateUrl: 'calendar-event-dialog.html',
})
export class CalendarEventDialogComponent {
  dataForm: FormGroup;
  constructor(
    private formBuilder: FormBuilder,
    public dialogRef: MatDialogRef<CalendarEventDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData) {
    this.dataForm = this.formBuilder.group({
      action: [data.action, null],
      event: [data.event, null],
      id: [data.event.meta.id, null],
      employee_id: [data.event.meta.employee_id, Validators.required],
      leave_days: [data.event.meta.leave_days, [Validators.required, Validators.pattern('[1-9][0-9]?')]],
      start_date: [data.event.meta.start_date, Validators.required],
      end_date: [data.event.meta.end_date, Validators.required]
    });
  }

  doAction() {
    // break if form is invalid
    if (this.dataForm.invalid) {
      return;
    }
    const leaveDays = {
      id: this.dataForm.controls.id.value,
      employee_id: parseInt(this.dataForm.controls.employee_id.value, 10),
      leave_days: parseInt(this.dataForm.controls.leave_days.value, 10),
      start_date: this.dataForm.controls.start_date.value,
      end_date: this.dataForm.controls.end_date.value
    };
    this.dialogRef.close({ event: 'Update', data: leaveDays });
  }

  closeDialog(): void {
    this.dialogRef.close({ event: 'Cancel' });
  }

}
