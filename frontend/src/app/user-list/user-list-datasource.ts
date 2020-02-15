import { DataSource } from '@angular/cdk/collections';
import { BehaviorSubject, Observable, of } from 'rxjs';
import { catchError, finalize } from 'rxjs/operators';
import { AlertService } from '../alert/alert.service';
import { User } from '../api_client/model/user';
import { UserService } from '../api_client/api/user.service';

/**
 * Data source for the UserList view. This class should
 * encapsulate all logic for fetching and manipulating the displayed data
 * (including sorting, pagination, and filtering).
 */
export class UserListDataSource extends DataSource<User> {

  private dataSubject = new BehaviorSubject<User[]>([]);
  private loadingSubject = new BehaviorSubject<boolean>(false);

  public loading$ = this.loadingSubject.asObservable();

  constructor(private apiClient: UserService, private alertService: AlertService) {
    super();
  }

  /**
   * Connect this data source to the table. The table will only update when
   * the returned stream emits new items.
   * @returns A stream of the items to be rendered.
   */
  connect(): Observable<User[]> {
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

  loadData(username?: string, email?: string, roles?: string) {
    this.loadingSubject.next(true);
    this.apiClient.findBy(username, email, roles).pipe(
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
