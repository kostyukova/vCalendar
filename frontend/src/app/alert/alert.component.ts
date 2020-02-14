import { Component, OnDestroy, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { Subscription } from 'rxjs';
import { AlertDialogComponent } from './alert-dialog.component';
import { Alert, AlertService } from './alert.service';

@Component({
  selector: 'app-alert',
  templateUrl: './alert.component.html',
  styleUrls: ['./alert.component.css']
})
export class AlertComponent implements OnInit, OnDestroy {
  private subscription: Subscription;
  message: Alert;

  constructor(private alertService: AlertService, private dialog: MatDialog) { }

  ngOnInit() {
    this.subscription = this.alertService.getMessage().subscribe(message => {
      this.message = message;
    });
  }

  ngOnDestroy() {
    this.subscription.unsubscribe();
  }

  onClose(event) {
    this.alertService.clear();
  }

  onView(event) {
    if (this.message && this.message.details) {
      this.dialog.open(AlertDialogComponent, {
        width: '600px',
        data: this.message.details
      });
    }
  }
}
