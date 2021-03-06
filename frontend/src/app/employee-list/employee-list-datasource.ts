import { DataSource } from '@angular/cdk/collections';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { BehaviorSubject, Observable, of } from 'rxjs';
import { catchError, finalize } from 'rxjs/operators';
import { EmployeeService } from '../api_client/api/employee.service';
import { Employee } from '../api_client/model/employee';
import { TeamPipe } from '../_services/team-pipe';
import { YesnoPipe } from '../_services/Yesno-pipe';
import { AlertService } from '../alert/alert.service';

/**
 * Data source for the EmployeeList view. This class should
 * encapsulate all logic for fetching and manipulating the displayed data
 * (including sorting, pagination, and filtering).
 */
export class EmployeeListDataSource extends DataSource<Employee> {

  private dataSubject = new BehaviorSubject<Employee[]>([]);
  public dataLength = new BehaviorSubject<number>(0);
  private loadingSubject = new BehaviorSubject<boolean>(false);

  public loading$ = this.loadingSubject.asObservable();
  public paginator: MatPaginator;
  public sort: MatSort;

  constructor(
    private apiClient: EmployeeService, private alertService: AlertService,
    private teamPipe: TeamPipe, private yesnoPipe: YesnoPipe) {
    super();
  }

  /**
   * Connect this data source to the table. The table will only update when
   * the returned stream emits new items.
   * @returns A stream of the items to be rendered.
   */
  connect(): Observable<Employee[]> {
    return this.dataSubject.asObservable();
  }

  /**
   *  Called when the table is being destroyed. Use this function, to clean up
   * any open connections or free any held resources that were set up during connect.
   */
  disconnect() {
    this.dataSubject.complete();
    this.loadingSubject.complete();
  }

  loadData(fullName?: string, position?: string, specialization?: string, expert?: boolean, teamId?: number, email?: string) {
    this.loadingSubject.next(true);
    this.apiClient.findEmployeesBy(fullName, position, specialization, expert, teamId, email).pipe(
      catchError((error) => {
        this.alertService.error(error.message);
        return of([]);
      }),
      finalize(() => this.loadingSubject.next(false))
    ).subscribe(data => {
      data.forEach(item => {
        item.team_name = this.teamPipe.transform(item.team_id);
        item.expert_value = this.yesnoPipe.transform(item.expert);
      });
      this.dataSubject.next(data);
      this.dataLength.next(data.length);
    });
  }
}
