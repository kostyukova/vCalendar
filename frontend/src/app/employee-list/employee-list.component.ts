import { AfterViewInit, Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { MatTable } from '@angular/material/table';
import { EmployeeService } from '../api_client/api/employee.service';
import { Employee } from '../api_client/model/employee';
import { EmployeeListDataSource } from './employee-list-datasource';
import { fromEvent } from 'rxjs';
import { debounceTime, distinctUntilChanged, tap } from 'rxjs/operators';
import { TeamPipe } from '../_services/team-pipe';

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
  @ViewChild('inputPosition', { static: false }) inputPosition: ElementRef;
  @ViewChild('inputSpecialization', { static: false }) inputSpecialization: ElementRef;
  dataSource: EmployeeListDataSource;

  /** Columns displayed in the table. Columns IDs can be added, removed, or reordered. */
  displayedColumns = ['employee_id', 'full_name', 'position', 'specialization', 'team_id', 'expert'];

  constructor(private apiClient: EmployeeService, private teamPipe: TeamPipe) {

  }

  ngOnInit() {
    this.dataSource = new EmployeeListDataSource(this.apiClient, this.teamPipe);
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
        tap(() => {
          this.dataSource.loadData(this.inputFullName.nativeElement.value,
            this.inputPosition.nativeElement.value,
            this.inputSpecialization.nativeElement.value);
        })
      )
      .subscribe();
    fromEvent(this.inputPosition.nativeElement, 'keyup')
      .pipe(
        debounceTime(150),
        distinctUntilChanged(),
        tap(() => {
          this.dataSource.loadData(this.inputFullName.nativeElement.value,
            this.inputPosition.nativeElement.value,
            this.inputSpecialization.nativeElement.value);
        })
      )
      .subscribe();
    fromEvent(this.inputSpecialization.nativeElement, 'keyup')
      .pipe(
        debounceTime(150),
        distinctUntilChanged(),
        tap(() => {
          this.dataSource.loadData(this.inputFullName.nativeElement.value,
            this.inputPosition.nativeElement.value,
            this.inputSpecialization.nativeElement.value);
        })
      )
      .subscribe();
  }

  onRowClicked(row) {
    console.log(row);
  }
}
