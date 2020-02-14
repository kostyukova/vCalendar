import { AfterViewInit, Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatTable } from '@angular/material/table';
import { fromEvent } from 'rxjs';
import { debounceTime, distinctUntilChanged, tap } from 'rxjs/operators';
import { AlertService } from '../alert/alert.service';
import { TeamService } from '../api_client/api/team.service';
import { Team } from '../api_client/model/team';
import { TeamDialogComponent } from '../team-dialog/team-dialog.component';
import { TeamListDataSource } from './team-list-datasource';

@Component({
  selector: 'app-team-list',
  templateUrl: './team-list.component.html',
  styleUrls: ['./team-list.component.css']
})
export class TeamListComponent implements AfterViewInit, OnInit {
  @ViewChild(MatTable, { static: false }) table: MatTable<Team>;
  @ViewChild('inputName', { static: false }) inputName: ElementRef;

  dataSource: TeamListDataSource;
  displayedColumns = ['team_id', 'name', 'action'];

  constructor(
    private apiClient: TeamService, private alertService: AlertService,
    private dialog: MatDialog) { }

  ngOnInit() {
    this.dataSource = new TeamListDataSource(this.apiClient, this.alertService);
    this.dataSource.loadData('');
  }

  ngAfterViewInit() {
    this.table.dataSource = this.dataSource;
    // server-side search
    fromEvent(this.inputName.nativeElement, 'keyup')
      .pipe(
        debounceTime(300),
        distinctUntilChanged(),
        tap(() => this.loadData())
      ).subscribe();
  }

  loadData() {
    this.dataSource.loadData(
      this.inputName.nativeElement.value);
  }

  openDialog(action, row) {
    row.action = action;
    const dialogRef = this.dialog.open(TeamDialogComponent, {
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

  addRowData(row: Team) {
    console.log(row);
    row.team_id = 0;
    this.apiClient.addTeam(row).subscribe(() => {
      this.loadData();
      this.table.renderRows();
      this.alertService.success('Team has been added');
    }, error => this.alertService.error(error.message));
  }

  updateRowData(row: Team) {
    console.log(row);
    this.apiClient.updateTeamById(row.team_id, row).subscribe(() => {
      this.loadData();
      this.table.renderRows();
      this.alertService.success('Team has been updated');
    }, error => this.alertService.error(error.message));
  }

  deleteRowData(row: Team) {
    console.log(row);
    this.apiClient.deleteTeam(row.team_id).subscribe(() => {
      this.loadData();
      this.table.renderRows();
      this.alertService.success('Team has been deleted');
    }, error => this.alertService.error(error.message));
  }
}
