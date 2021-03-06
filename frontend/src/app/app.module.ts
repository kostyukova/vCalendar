import { LayoutModule } from '@angular/cdk/layout';
import { DatePipe } from '@angular/common';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { FlexLayoutModule } from '@angular/flex-layout';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatDialogModule } from '@angular/material/dialog';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatListModule } from '@angular/material/list';
import { MatMenuModule } from '@angular/material/menu';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatRadioModule } from '@angular/material/radio';
import { MatSelectModule } from '@angular/material/select';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatSortModule } from '@angular/material/sort';
import { MatTableModule } from '@angular/material/table';
import { MatToolbarModule } from '@angular/material/toolbar';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { CalendarModule, DateAdapter } from 'angular-calendar';
import { adapterFactory } from 'angular-calendar/date-adapters/date-fns';
import { environment } from '../environments/environment';
import { AlertDialogComponent } from './alert/alert-dialog.component';
import { AlertComponent } from './alert/alert.component';
import { AlertService } from './alert/alert.service';
import { BASE_PATH } from './api_client';
import { ApiModule } from './api_client/api.module';
import { EmployeeService } from './api_client/api/employee.service';
import { LeaveDaysService } from './api_client/api/leaveDays.service';
import { TeamService } from './api_client/api/team.service';
import { TotalDaysService } from './api_client/api/totalDays.service';
import { UserService } from './api_client/api/user.service';
import { Configuration, ConfigurationParameters } from './api_client/configuration';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { CalendarEventDialogComponent } from './calendar/calendar-event.component';
import { CalendarComponent } from './calendar/calendar.component';
import { EmployeeDialogComponent } from './employee-dialog/employee-dialog.component';
import { EmployeeListComponent } from './employee-list/employee-list.component';
import { LoginComponent } from './login/login.component';
import { NavigationComponent } from './navigation/navigation.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { UserListComponent } from './user-list/user-list.component';
import { BasicAuthInspector } from './_helpers/basic-auth-inspector';
import { ErrorInterceptor } from './_helpers/error-intersepror';
import { AuthenticationService } from './_services/authentication.service';
import { TeamCache } from './_services/team-cache';
import { TeamPipe } from './_services/team-pipe';
import { YesnoPipe } from './_services/Yesno-pipe';
import { TeamListComponent } from './team-list/team-list.component';
import { TeamDialogComponent } from './team-dialog/team-dialog.component';
import { UserDialogComponent } from './user-dialog/user-dialog.component';

export function apiConfigFactory(): Configuration {
  const params: ConfigurationParameters = {
    apiKeys: {}
  };
  return new Configuration(params);
}

@NgModule({
  declarations: [
    AppComponent,
    NavigationComponent,
    PageNotFoundComponent,
    EmployeeListComponent,
    CalendarComponent,
    CalendarEventDialogComponent,
    LoginComponent,
    AlertComponent,
    TeamPipe,
    YesnoPipe,
    UserListComponent,
    AlertDialogComponent,
    EmployeeDialogComponent,
    TeamListComponent,
    TeamDialogComponent,
    UserDialogComponent
  ],
  entryComponents: [
    CalendarComponent,
    CalendarEventDialogComponent,
    AlertDialogComponent,
    TeamDialogComponent,
    EmployeeDialogComponent,
    UserDialogComponent
  ],
  imports: [
    ApiModule.forRoot(apiConfigFactory),
    BrowserModule,
    HttpClientModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule,
    MatSelectModule,
    MatRadioModule,
    MatCardModule,
    ReactiveFormsModule,
    FormsModule,
    LayoutModule,
    MatToolbarModule,
    MatSidenavModule,
    MatListModule,
    MatTableModule,
    MatPaginatorModule,
    MatSortModule,
    MatGridListModule,
    MatMenuModule,
    MatProgressSpinnerModule,
    MatDialogModule,
    MatExpansionModule,
    MatAutocompleteModule,
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
    { provide: HTTP_INTERCEPTORS, useClass: BasicAuthInspector, multi: true },
    { provide: HTTP_INTERCEPTORS, useClass: ErrorInterceptor, multi: true },
    TeamPipe,
    YesnoPipe,
    DatePipe
  ],
  bootstrap: [AppComponent]
})

export class AppModule { }
