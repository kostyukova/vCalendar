import { DatePipe } from '@angular/common';
import { ChangeDetectionStrategy, Component, OnInit } from '@angular/core';
import { CalendarEvent, CalendarView } from 'angular-calendar';
import { addMonths, endOfDay, endOfMonth, startOfDay, startOfMonth, subMonths } from 'date-fns';
import { Observable, of } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { LeaveDaysService } from '../api_client/api/leaveDays.service';
import { LeaveDays } from '../api_client/model/leaveDays';


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

  constructor(private dataPipe: DatePipe, private apiClient: LeaveDaysService) { }

  ngOnInit(): void {
    this.fetchEvents();
  }

  fetchEvents(): void {
    this.events$ = this.apiClient.findLeaveDaysBy(null,
      this.dataPipe.transform(startOfMonth(this.viewDate), 'yyyy-MM-dd'),
      this.dataPipe.transform(endOfMonth(this.viewDate), 'yyyy-MM-dd')
    ).pipe(
      map((data: LeaveDays[]) => {
        console.log(data);
        return data.map((leavedays: LeaveDays) => {
          return {
            title: 'Leave days for employee' + leavedays.employee_id,
            start: startOfDay(new Date(leavedays.start_date)),
            end: endOfDay(new Date(leavedays.end_date)),
            color: this.getNextColor(),
            allDay: true,
            meta: leavedays
          };
        });
      }),
      catchError(() => of([]))
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
}
