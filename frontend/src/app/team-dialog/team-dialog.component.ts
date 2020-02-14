import { Component, Inject, OnInit, Optional } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { Team } from '../api_client/model/team';

@Component({
  selector: 'app-team-dialog',
  templateUrl: './team-dialog.component.html',
  styleUrls: ['./team-dialog.component.css']
})
export class TeamDialogComponent implements OnInit {

  dataForm: FormGroup;

  constructor(
    private formBuilder: FormBuilder,
    private dialogRef: MatDialogRef<TeamDialogComponent>,
    @Optional() @Inject(MAT_DIALOG_DATA) private data: Team | any) {

    this.dataForm = this.formBuilder.group({
      team_id: [data.team_id, null],
      name: [data.name, [Validators.required, Validators.maxLength(255)]],
      action: [data.action, null]
    });
  }

  ngOnInit() {
  }

  doAction() {
    // break if form is invalid
    if (this.dataForm.invalid) {
      return;
    }
    const team = {
      team_id: this.dataForm.controls.team_id.value,
      name: this.dataForm.controls.name.value.trim(),
    };
    this.dialogRef.close({ event: this.dataForm.controls.action.value, data: team });
  }

  closeDialog() {
    this.dialogRef.close({ event: 'Cancel' });
  }
}
