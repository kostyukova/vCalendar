import { AfterViewInit, Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { MatTable } from '@angular/material/table';
import { fromEvent, Observable } from 'rxjs';
import { debounceTime, distinctUntilChanged, tap } from 'rxjs/operators';
import { AlertService } from '../alert/alert.service';
import { EmployeeService } from '../api_client/api/employee.service';
import { Employee } from '../api_client/model/employee';
import { EmployeeDialogComponent } from '../employee-dialog/employee-dialog.component';
import { TeamCache } from '../_services/team-cache';
import { TeamPipe } from '../_services/team-pipe';
import { YesnoPipe } from '../_services/Yesno-pipe';
import { EmployeeListDataSource } from './employee-list-datasource';

@Component({
  selector: 'app-employee-list',
  templateUrl: './employee-list.component.html',
  styleUrls: ['./employee-list.component.css']
})
export class EmployeeListComponent implements AfterViewInit, OnInit {
  @ViewChild(MatPaginator, { static: false }) paginator: MatPaginator;
  @ViewChild(MatSort, { static: false }) sort: MatSort;
  @ViewChild(MatTable, { static: false }) table: MatTable<Employee>;
  @ViewChild('inputFullName', { static: false }) inputFullName: ElementRef;
  @ViewChild('inputEmail', { static: false }) inputEmail: ElementRef;
  @ViewChild('inputPosition', { static: false }) inputPosition: ElementRef;
  @ViewChild('inputSpecialization', { static: false }) inputSpecialization: ElementRef;
  @ViewChild('inputTeam', { static: false }) inputTeam: ElementRef;
  @ViewChild('inputExpert', { static: false }) inputExpert: ElementRef;

  dataSource: EmployeeListDataSource;
  displayedColumns = ['employee_id', 'full_name', 'position', 'specialization', 'team_id', 'expert', 'action'];

  constructor(
    private apiClient: EmployeeService, private teamCache: TeamCache, private teamPipe: TeamPipe,
    private yesnoPipe: YesnoPipe, private dialog: MatDialog,
    private alertService: AlertService) { }

  ngOnInit() {
    this.dataSource = new EmployeeListDataSource(this.apiClient, this.teamPipe, this.yesnoPipe);
    this.dataSource.loadData('');
  }

  ngAfterViewInit() {
    this.dataSource.sort = this.sort;
    this.dataSource.paginator = this.paginator;
    this.table.dataSource = this.dataSource;
    // server-side search
    fromEvent(this.inputFullName.nativeElement, 'keyup')
      .pipe(
        debounceTime(150),
        distinctUntilChanged(),
        tap(() => this.loadData())
      ).subscribe();
    fromEvent(this.inputEmail.nativeElement, 'keyup')
      .pipe(
        debounceTime(150),
        distinctUntilChanged(),
        tap(() => this.loadData())
      ).subscribe();
    fromEvent(this.inputPosition.nativeElement, 'keyup')
      .pipe(
        debounceTime(150),
        distinctUntilChanged(),
        tap(() => this.loadData())
      ).subscribe();
    fromEvent(this.inputSpecialization.nativeElement, 'keyup')
      .pipe(
        debounceTime(150),
        distinctUntilChanged(),
        tap(() => this.loadData())
      ).subscribe();
    fromEvent(this.inputTeam.nativeElement, 'change')
      .pipe(
        distinctUntilChanged(),
        tap(() => this.loadData())
      ).subscribe();
    fromEvent(this.inputExpert.nativeElement, 'change')
      .pipe(
        distinctUntilChanged(),
        tap(() => this.loadData())
      ).subscribe();
  }

  loadData() {
    this.dataSource.loadData(
      this.inputFullName.nativeElement.value,
      this.inputPosition.nativeElement.value,
      this.inputSpecialization.nativeElement.value,
      this.inputExpert.nativeElement.value ? this.inputExpert.nativeElement.value : null,
      this.inputTeam.nativeElement.value ? this.inputTeam.nativeElement.value : null,
      this.inputEmail.nativeElement.value);
  }

  get teams(): Observable<Map<number, string>> {
    return this.teamCache.getFoundList();
  }

  openDialog(action, row) {
    row.action = action;
    const dialogRef = this.dialog.open(EmployeeDialogComponent, {
      width: '400px',
      data: row
    });

    dialogRef.afterClosed().subscribe(result => {
      if (!result) {
        return;
      }
      if (result.event === 'Add') {
        this.addRowData(result.data);
      } else if (result.event === 'Update') {
        this.updateRowData(result.data);
      } else if (result.event === 'Delete') {
        this.deleteRowData(result.data);
      }
    });
  }

  addRowData(row: Employee) {
    console.log(row);
    row.employee_id = 0;
    this.apiClient.addEmployee(row).subscribe(result => {
      this.loadData();
      this.table.renderRows();
      this.alertService.success('Employee has been added');
    }, error => this.alertService.error(error));
  }

  updateRowData(row: Employee) {
    console.log(row);
    this.apiClient.updateEmployeeById(row.employee_id, row).subscribe(result => {
      this.loadData();
      this.table.renderRows();
      this.alertService.success('Employee has been updated');
    }, error => this.alertService.error(error));
  }

  deleteRowData(row: Employee) {
    console.log(row);
    this.apiClient.deleteEmployee(row.employee_id).subscribe(result => {
      this.loadData();
      this.table.renderRows();
      this.alertService.success('Employee has been deleted');
    }, error => this.alertService.error(error));
  }
}
