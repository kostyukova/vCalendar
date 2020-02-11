import { LayoutModule } from '@angular/cdk/layout';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { FlexLayoutModule } from '@angular/flex-layout';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatListModule } from '@angular/material/list';
import { MatMenuModule } from '@angular/material/menu';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatRadioModule } from '@angular/material/radio';
import { MatSelectModule } from '@angular/material/select';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatSortModule } from '@angular/material/sort';
import { MatTableModule } from '@angular/material/table';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatDialogModule } from '@angular/material/dialog';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { CalendarModule, DateAdapter } from 'angular-calendar';
import { adapterFactory } from 'angular-calendar/date-adapters/date-fns';
import { environment } from '../environments/environment';
import { AddressFormComponent } from './address-form/address-form.component';
import { BASE_PATH } from './api_client';
import { EmployeeService } from './api_client/api/employee.service';
import { LeaveDaysService } from './api_client/api/leaveDays.service';
import { TeamService } from './api_client/api/team.service';
import { TotalDaysService } from './api_client/api/totalDays.service';
import { UserService } from './api_client/api/user.service';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { CalendarComponent, CalendarEventDialog } from './calendar/calendar.component';
import { DashboardComponent } from './dashboard/dashboard.component';
import { EmployeeListComponent } from './employee-list/employee-list.component';
import { HomeComponent } from './home/home.component';
import { NavigationComponent } from './navigation/navigation.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { TableComponent } from './table/table.component';
import { DatePipe } from '@angular/common';
import { LoginComponent } from './login/login.component';
import { BasicAuthInspector } from './_helpers/basic-auth-inspector';
import { AuthenticationService } from './_services/authentication.service';
import { AlertComponent } from './alert/alert.component';
import { AlertService } from './alert/alert.service';
import { ErrorInterceptor } from './_helpers/error-intersepror';
import { UserListComponent } from './user-list/user-list.component';
import { TeamCache } from './_services/team-cache';
import { TeamPipe } from './_services/team-pipe';


@NgModule({
  declarations: [
    AppComponent,
    AddressFormComponent,
    NavigationComponent,
    TableComponent,
    DashboardComponent,
    HomeComponent,
    PageNotFoundComponent,
    EmployeeListComponent,
    CalendarComponent,
    CalendarEventDialog,
    LoginComponent,
    AlertComponent,
    TeamPipe,
    UserListComponent
  ],
  entryComponents: [
    CalendarComponent,
    CalendarEventDialog
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatInputModule,
    MatButtonModule,
    MatSelectModule,
    MatRadioModule,
    MatCardModule,
    ReactiveFormsModule,
    FormsModule,
    LayoutModule,
    MatToolbarModule,
    MatSidenavModule,
    MatIconModule,
    MatListModule,
    MatTableModule,
    MatPaginatorModule,
    MatSortModule,
    MatGridListModule,
    MatMenuModule,
    MatProgressSpinnerModule,
    MatDialogModule,
    FlexLayoutModule,
    CalendarModule.forRoot({ provide: DateAdapter, useFactory: adapterFactory })
  ],
  providers: [
    { provide: BASE_PATH, useValue: environment.API_BASE_PATH },
    EmployeeService,
    LeaveDaysService,
    TeamService,
    TotalDaysService,
    UserService,
    AlertService,
    TeamCache,
    AuthenticationService,
    { provide: HTTP_INTERCEPTORS, useClass: BasicAuthInspector, multi: true},
    { provide: HTTP_INTERCEPTORS, useClass: ErrorInterceptor, multi: true},
    TeamPipe,
    DatePipe
  ],
  bootstrap: [AppComponent]
})

export class AppModule { }
