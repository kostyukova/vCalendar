import { Component, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { DialogData } from '../calendar/calendar.component';


@Component({
  selector: 'app-alert-dialog',
  templateUrl: 'alert-dialog.component.html',
})
export class AlertDialogComponent {

  constructor(
    public dialogRef: MatDialogRef<AlertDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData) { }

  onClose(): void {
    this.dialogRef.close();
  }
}
