import { AfterViewInit, Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatTable } from '@angular/material/table';
import { fromEvent } from 'rxjs';
import { debounceTime, distinctUntilChanged, tap } from 'rxjs/operators';
import { AlertService } from '../alert/alert.service';
import { UserService } from '../api_client/api/user.service';
import { User } from '../api_client/model/user';
import { UserDialogComponent } from '../user-dialog/user-dialog.component';
import { UserListDataSource } from './user-list-datasource';

@Component({
  selector: 'app-user-list',
  templateUrl: './user-list.component.html',
  styleUrls: ['./user-list.component.css']
})
export class UserListComponent implements AfterViewInit, OnInit {
  @ViewChild(MatTable, { static: false }) table: MatTable<User>;
  @ViewChild('inputUsername', { static: false }) inputUsername: ElementRef;
  @ViewChild('inputEmail', { static: false }) inputEmail: ElementRef;

  dataSource: UserListDataSource;
  displayedColumns = ['id', 'username', 'email', 'roles', 'action'];

  constructor(
    private apiClient: UserService, private alertService: AlertService,
    private dialog: MatDialog) { }

  ngOnInit() {
    this.dataSource = new UserListDataSource(this.apiClient, this.alertService);
    this.dataSource.loadData('');
  }

  ngAfterViewInit() {
    this.table.dataSource = this.dataSource;
    // server-side search
    fromEvent(this.inputUsername.nativeElement, 'keyup')
      .pipe(
        debounceTime(300),
        distinctUntilChanged(),
        tap(() => this.loadData())
      ).subscribe();
    fromEvent(this.inputEmail.nativeElement, 'keyup')
      .pipe(
        debounceTime(300),
        distinctUntilChanged(),
        tap(() => this.loadData())
      ).subscribe();
  }

  loadData() {
    this.dataSource.loadData(
      this.inputUsername.nativeElement.value,
      this.inputEmail.nativeElement.value
    );
  }

  openDialog(action, row) {
    row.action = action;
    const dialogRef = this.dialog.open(UserDialogComponent, {
      width: '400px',
      data: row
    });

    dialogRef.afterClosed().subscribe(result => {
      if (!result) {
        return;
      }
      switch (result.event) {
        case 'Add':
          this.addRowData(result.data);
          break;
        case 'Update':
          this.updateRowData(result.data);
          break;
        case 'Delete':
          this.deleteRowData(result.data);
          break;
        case 'Setpass':
          this.setPassword(result.data);
          break;
      }
    });
  }

  addRowData(row: User) {
    console.log(row);
    row.id = 0;
    this.apiClient.createUser(row).subscribe(() => {
      this.loadData();
      this.table.renderRows();
      this.alertService.success('User has been added');
    }, error => this.alertService.error(error.message));
  }

  updateRowData(row: User) {
    console.log(row);
    this.apiClient.updateUser(row.id, row).subscribe(() => {
      this.loadData();
      this.table.renderRows();
      this.alertService.success('User has been updated');
    }, error => this.alertService.error(error.message));
  }

  deleteRowData(row: User) {
    console.log(row);
    this.apiClient.deleteUser(row.id).subscribe(() => {
      this.loadData();
      this.table.renderRows();
      this.alertService.success('User has been deleted');
    }, error => this.alertService.error(error.message));
  }
  setPassword(row: User) {
    console.log(row, 'Set password');
  }
}
