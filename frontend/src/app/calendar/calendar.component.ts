import { DatePipe } from '@angular/common';
import { ChangeDetectionStrategy, Component, OnInit, ViewChild } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { CalendarEvent, CalendarView } from 'angular-calendar';
import { addMonths, endOfDay, endOfMonth, startOfDay, startOfMonth, subMonths } from 'date-fns';
import { Observable, of, Subject } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { LeaveDaysService } from '../api_client/api/leaveDays.service';
import { LeaveDays } from '../api_client/model/leaveDays';
import { CalendarEventDialogComponent } from './calendar-event.component';
import { AlertService } from '../alert/alert.service';
import { MatMenuTrigger } from '@angular/material/menu';

export interface DialogData {
  action: string;
  event: CalendarEvent;
}

@Component({
  selector: 'app-calendar',
  changeDetection: ChangeDetectionStrategy.OnPush,
  templateUrl: './calendar.component.html',
  styleUrls: ['./calendar.component.css']
})
export class CalendarComponent implements OnInit {
  view: CalendarView = CalendarView.Month;
  viewDate: Date = new Date();

  events$: Observable<Array<CalendarEvent<LeaveDays>>>;
  refresh: Subject<any> = new Subject();

  @ViewChild(MatMenuTrigger, { static: false })
  contextMenu: MatMenuTrigger;
  contextMenuPosition = { x: '0px', y: '0px' };

  colors: any = [
    {
      primary: '#C71585', // medium violet
      secondary: '#EFBCDC'
    },
    {
      primary: '#1e90ff', // blue
      secondary: '#D1E8FF'
    },
    {
      primary: '#e3bc08', // yellow
      secondary: '#FDF1BA'
    },
    {
      primary: '#228B22', // green
      secondary: '#BFDDBF'
    },
    {
      primary: '#FF4500', // orange red
      secondary: '#FFC9B6'
    },
    {
      primary: '#4682B4', // steel blue
      secondary: '#AFC9DE'
    }
  ];

  constructor(
    private dataPipe: DatePipe, private apiClient: LeaveDaysService,
    private modal: MatDialog, private alertService: AlertService) { }

  ngOnInit(): void {
    this.fetchEvents();
  }

  fetchEvents(): void {
    this.events$ = this.apiClient.findLeaveDaysBy(null,
      this.formatDate(startOfMonth(this.viewDate)),
      this.formatDate(endOfMonth(this.viewDate))
    ).pipe(
      map((data: LeaveDays[]) => {
        console.log(data);
        return data.map((leavedays: LeaveDays) => {
          return {
            title: 'Leave days for employee ' + leavedays.employee_id,
            start: startOfDay(new Date(leavedays.start_date)),
            end: endOfDay(new Date(leavedays.end_date)),
            color: this.getNextColor(),
            allDay: true,
            meta: leavedays
          };
        });
      }),
      catchError((error) => {
        this.alertService.error(error);
        return of([]);
      })
    );
  }

  getNextColor(): any {
    const color: any = this.colors.shift();
    this.colors.push(color);
    return color;
  }

  increment(): void {
    this.changeDate(addMonths(this.viewDate, 1));
  }

  decrement(): void {
    this.changeDate(subMonths(this.viewDate, 1));
  }

  today(): void {
    this.changeDate(new Date());
  }

  changeDate(date: Date): void {
    this.viewDate = date;
    this.fetchEvents();
  }

  onContextMenu(event: MouseEvent, date: Date) {
    event.preventDefault();
    this.contextMenuPosition.x = event.clientX + 'px';
    this.contextMenuPosition.y = event.clientY + 'px';
    this.contextMenu.menuData = { item: date };
    this.contextMenu.menu.focusFirstItem('mouse');
    this.contextMenu.openMenu();
  }

  onContextMenuAdd(date: Date) {
    const formated = this.formatDate(date);
    this.handleEvent('Add', {
      start: date,
      title: 'Add leave days for an employee',
      allDay: true, meta: {
        start_date: formated,
        end_date: formated
      }
    });
  }

  handleEvent(calendarAction: string, calendarEvent: CalendarEvent): void {
    const dialogRef = this.modal.open(CalendarEventDialogComponent, {
      width: '800px',
      height: '460px',
      data: { action: calendarAction, event: calendarEvent }
    });

    dialogRef.afterClosed().subscribe(result => {
      // result data from dialog
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

  private refreshCalendarView(): void {
    // emit refresh event
    this.refresh.next();
  }

  private addRowData(row: LeaveDays | any) {
    console.log(row);
    row.id = 0;
    row.employee_id = row.employee.employee_id;
    delete row.employee;
    this.apiClient.addLeaveDays(row).subscribe(result => {
      this.fetchEvents();
      this.refreshCalendarView();
      this.alertService.success('Employee leave days has been added');
    }, error => this.alertService.error(error));
  }

  private updateRowData(row: LeaveDays | any) {
    console.log(row);
    row.employee_id = row.employee.employee_id;
    delete row.employee;
    this.apiClient.updateLeaveDaysById(row.id, row).subscribe(result => {
      this.fetchEvents();
      this.refreshCalendarView();
      this.alertService.success('Employee leave days has been updated');
    }, error => this.alertService.error(error));
  }

  private deleteRowData(row: LeaveDays) {
    console.log(row);
    this.apiClient.deleteLeaveDays(row.id).subscribe(result => {
      this.fetchEvents();
      this.refreshCalendarView();
      this.alertService.success('Employee leave days has been deleted');
    }, error => this.alertService.error(error));
  }

  private formatDate(date: Date) {
    return this.dataPipe.transform(date, 'yyyy-MM-dd');
  }
}
