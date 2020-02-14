import { DataSource } from '@angular/cdk/collections';
import { MatPaginator } from '@angular/material/paginator';
import { MatSort } from '@angular/material/sort';
import { BehaviorSubject, Observable, of } from 'rxjs';
import { catchError, finalize } from 'rxjs/operators';
import { EmployeeService } from '../api_client/api/employee.service';
import { Team } from '../api_client/model/team';
import { TeamService } from '../api_client/api/team.service';
import { AlertService } from '../alert/alert.service';

/**
 * Data source for the TeamList view. This class should
 * encapsulate all logic for fetching and manipulating the displayed data
 * (including sorting, pagination, and filtering).
 */
export class TeamListDataSource extends DataSource<Team> {

  private dataSubject = new BehaviorSubject<Team[]>([]);
  private loadingSubject = new BehaviorSubject<boolean>(false);

  public loading$ = this.loadingSubject.asObservable();

  constructor(private apiClient: TeamService, private alertService: AlertService) {
    super();
  }

  /**
   * Connect this data source to the table. The table will only update when
   * the returned stream emits new items.
   * @returns A stream of the items to be rendered.
   */
  connect(): Observable<Team[]> {
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

  loadData(name?: string) {
    this.loadingSubject.next(true);
    this.apiClient.findTeamBy(name).pipe(
      catchError(error => {
        this.alertService.error(error.message);
        return of([]);
      }),
      finalize(() => this.loadingSubject.next(false))
    ).subscribe(data => {
      this.dataSubject.next(data);
    });
  }
}
